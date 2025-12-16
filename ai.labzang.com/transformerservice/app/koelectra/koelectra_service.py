"""
KoELECTRA 감성분석 서비스
한국어 영화 리뷰 감성분석을 위한 KoELECTRA 모델 서비스
"""

import os
import torch
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import numpy as np
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    ElectraTokenizer,
    ElectraForSequenceClassification
)
import json

logger = logging.getLogger(__name__)

class KoELECTRASentimentService:
    """KoELECTRA 기반 감성분석 서비스"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 파인튜닝된 모델이 있으면 우선 사용, 없으면 기본 모델 사용
        self.finetuned_model_path = "app/koelectra/koelectra_model_finetuned"
        self.base_model_path = "app/koelectra/koelectra_model"
        
        if Path(self.finetuned_model_path).exists():
            self.model_path = self.finetuned_model_path
            logger.info("파인튜닝된 모델을 사용합니다")
        else:
            self.model_path = self.base_model_path
            logger.info("기본 모델을 사용합니다")
            
        self.max_length = 512
        
        # 감성 레이블 매핑
        self.label_mapping = {
            0: "부정",
            1: "긍정"
        }
        
        logger.info(f"KoELECTRA 서비스 초기화 - 디바이스: {self.device}")
    
    def load_model(self) -> bool:
        """KoELECTRA 모델과 토크나이저 로드"""
        try:
            model_path = Path(self.model_path)
            
            if not model_path.exists():
                logger.error(f"모델 경로가 존재하지 않습니다: {model_path}")
                return False
            
            logger.info(f"모델 로딩 시작: {model_path}")
            
            # 토크나이저 로드
            self.tokenizer = ElectraTokenizer.from_pretrained(
                str(model_path),
                do_lower_case=False
            )
            
            # 모델 로드 (감성분석용으로 수정)
            # 기본 ELECTRA 모델을 감성분석용으로 변환
            from transformers import ElectraConfig
            
            config = ElectraConfig.from_pretrained(str(model_path))
            config.num_labels = 2  # 긍정/부정 이진 분류
            
            # 감성분석용 모델 생성
            self.model = ElectraForSequenceClassification(config)
            
            # 사전 훈련된 가중치 로드 (분류 헤드 제외)
            pretrained_dict = torch.load(
                model_path / "pytorch_model.bin", 
                map_location=self.device
            )
            
            # 모델 상태 딕셔너리 가져오기
            model_dict = self.model.state_dict()
            
            # 사전 훈련된 가중치 중 모델과 일치하는 것만 필터링
            filtered_dict = {
                k: v for k, v in pretrained_dict.items() 
                if k in model_dict and model_dict[k].shape == v.shape
            }
            
            # 가중치 업데이트
            model_dict.update(filtered_dict)
            self.model.load_state_dict(model_dict, strict=False)
            
            # 분류 헤드 초기화 (랜덤 가중치)
            if hasattr(self.model, 'classifier'):
                torch.nn.init.normal_(self.model.classifier.weight, std=0.02)
                torch.nn.init.zeros_(self.model.classifier.bias)
            
            self.model.to(self.device)
            self.model.eval()
            
            logger.info("✅ KoELECTRA 모델 로딩 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ 모델 로딩 실패: {str(e)}")
            return False
    
    def preprocess_text(self, text: str) -> str:
        """텍스트 전처리"""
        if not text:
            return ""
        
        # 기본 정리
        text = text.strip()
        
        # 과도한 공백 제거
        import re
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def predict_sentiment(self, text: str) -> Dict[str, Any]:
        """단일 텍스트 감성분석"""
        try:
            if not self.model or not self.tokenizer:
                if not self.load_model():
                    return {"error": "모델 로딩 실패"}
            
            # 텍스트 전처리
            processed_text = self.preprocess_text(text)
            
            if not processed_text:
                return {"error": "빈 텍스트입니다"}
            
            # 토크나이징
            inputs = self.tokenizer(
                processed_text,
                return_tensors="pt",
                max_length=self.max_length,
                padding=True,
                truncation=True
            )
            
            # 디바이스로 이동
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # 추론
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                
                # 소프트맥스로 확률 계산
                probabilities = torch.nn.functional.softmax(logits, dim=-1)
                predicted_class = torch.argmax(probabilities, dim=-1).item()
                confidence = probabilities[0][predicted_class].item()
            
            # 결과 구성
            result = {
                "text": text,
                "sentiment": self.label_mapping[predicted_class],
                "confidence": round(confidence, 4),
                "probabilities": {
                    "부정": round(probabilities[0][0].item(), 4),
                    "긍정": round(probabilities[0][1].item(), 4)
                },
                "model_info": {
                    "model_type": "KoELECTRA",
                    "device": str(self.device)
                }
            }
            
            logger.info(f"감성분석 완료 - 텍스트: '{text[:50]}...', 결과: {result['sentiment']}")
            return result
            
        except Exception as e:
            logger.error(f"감성분석 실패: {str(e)}")
            return {"error": f"감성분석 실패: {str(e)}"}
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """배치 텍스트 감성분석"""
        try:
            if not self.model or not self.tokenizer:
                if not self.load_model():
                    return [{"error": "모델 로딩 실패"} for _ in texts]
            
            results = []
            
            for text in texts:
                result = self.predict_sentiment(text)
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"배치 감성분석 실패: {str(e)}")
            return [{"error": f"배치 감성분석 실패: {str(e)}"} for _ in texts]
    
    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보 반환"""
        return {
            "model_name": "KoELECTRA",
            "model_path": self.model_path,
            "device": str(self.device),
            "max_length": self.max_length,
            "labels": list(self.label_mapping.values()),
            "loaded": self.model is not None and self.tokenizer is not None
        }
    
    def health_check(self) -> Dict[str, Any]:
        """서비스 상태 확인"""
        try:
            # 간단한 테스트 문장으로 확인
            test_result = self.predict_sentiment("이 영화는 정말 재미있어요!")
            
            return {
                "status": "healthy" if "error" not in test_result else "error",
                "model_loaded": self.model is not None,
                "tokenizer_loaded": self.tokenizer is not None,
                "device": str(self.device),
                "test_prediction": test_result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "model_loaded": False,
                "tokenizer_loaded": False
            }


# 싱글톤 인스턴스
_service_instance: Optional[KoELECTRASentimentService] = None

def get_sentiment_service() -> KoELECTRASentimentService:
    """KoELECTRA 감성분석 서비스 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = KoELECTRASentimentService()
    return _service_instance
