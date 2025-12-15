"""
KoELECTRA 영화 리뷰 감성분석 파인튜닝 스크립트
영화 리뷰 데이터를 사용하여 KoELECTRA 모델을 감성분석용으로 파인튜닝
"""

import os
import json
import torch
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from transformers import (
    ElectraTokenizer,
    ElectraForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from torch.utils.data import Dataset
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MovieReviewDataset(Dataset):
    """영화 리뷰 데이터셋 클래스"""
    
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int = 512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        # 토큰화
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

class KoELECTRATrainer:
    """KoELECTRA 파인튜닝 트레이너"""
    
    def __init__(self, model_path: str = "app/koelectra/koelectra_model", data_path: str = "app/koelectra/data"):
        self.model_path = Path(model_path)
        self.data_path = Path(data_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 모델과 토크나이저 로드
        self.tokenizer = ElectraTokenizer.from_pretrained(str(self.model_path))
        self.model = ElectraForSequenceClassification.from_pretrained(
            str(self.model_path),
            num_labels=2,  # 긍정/부정 이진 분류
            ignore_mismatched_sizes=True
        )
        
        logger.info(f"모델 로드 완료: {self.model_path}")
        logger.info(f"디바이스: {self.device}")
    
    def load_and_preprocess_data(self) -> Tuple[List[str], List[int]]:
        """JSON 파일들에서 데이터 로드 및 전처리"""
        logger.info("데이터 로드 시작...")
        
        all_reviews = []
        all_labels = []
        
        # 모든 JSON 파일 처리
        json_files = list(self.data_path.glob("*.json"))
        logger.info(f"총 {len(json_files)}개 JSON 파일 발견")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    review = item.get('review', '').strip()
                    rating = int(item.get('rating', 0))
                    
                    # 빈 리뷰 제외
                    if not review or len(review) < 5:
                        continue
                    
                    # 평점을 이진 분류로 변환
                    # 1-5점: 부정(0), 6-10점: 긍정(1)
                    if rating >= 1 and rating <= 5:
                        label = 0  # 부정
                    elif rating >= 6 and rating <= 10:
                        label = 1  # 긍정
                    else:
                        continue  # 잘못된 평점 제외
                    
                    all_reviews.append(review)
                    all_labels.append(label)
                    
            except Exception as e:
                logger.warning(f"파일 처리 오류 {json_file}: {str(e)}")
                continue
        
        logger.info(f"총 {len(all_reviews)}개 리뷰 로드 완료")
        
        # 레이블 분포 확인
        positive_count = sum(1 for label in all_labels if label == 1)
        negative_count = len(all_labels) - positive_count
        logger.info(f"긍정 리뷰: {positive_count}개 ({positive_count/len(all_labels)*100:.1f}%)")
        logger.info(f"부정 리뷰: {negative_count}개 ({negative_count/len(all_labels)*100:.1f}%)")
        
        return all_reviews, all_labels
    
    def create_datasets(self, texts: List[str], labels: List[int], test_size: float = 0.2):
        """훈련/검증 데이터셋 생성"""
        logger.info("데이터셋 분할 중...")
        
        # 훈련/검증 분할
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            texts, labels, test_size=test_size, random_state=42, stratify=labels
        )
        
        logger.info(f"훈련 데이터: {len(train_texts)}개")
        logger.info(f"검증 데이터: {len(val_texts)}개")
        
        # 데이터셋 객체 생성
        train_dataset = MovieReviewDataset(train_texts, train_labels, self.tokenizer)
        val_dataset = MovieReviewDataset(val_texts, val_labels, self.tokenizer)
        
        return train_dataset, val_dataset
    
    def compute_metrics(self, eval_pred):
        """평가 메트릭 계산"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        
        accuracy = accuracy_score(labels, predictions)
        
        return {
            'accuracy': accuracy,
        }
    
    def train(self, epochs: int = 5, batch_size: int = 16, learning_rate: float = 2e-5):
        """모델 훈련"""
        logger.info("=== KoELECTRA 파인튜닝 시작 ===")
        
        # 데이터 로드
        texts, labels = self.load_and_preprocess_data()
        
        if len(texts) == 0:
            raise ValueError("훈련할 데이터가 없습니다!")
        
        # 데이터셋 생성
        train_dataset, val_dataset = self.create_datasets(texts, labels)
        
        # 훈련 인자 설정
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"app/koelectra/fine_tuned_model_{timestamp}"
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=500,
            weight_decay=0.01,
            learning_rate=learning_rate,
            logging_dir=f'{output_dir}/logs',
            logging_steps=100,
            evaluation_strategy="steps",
            eval_steps=500,
            save_strategy="steps",
            save_steps=1000,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            greater_is_better=True,
            report_to=None,  # 외부 로깅 비활성화
            save_total_limit=2,  # 최대 2개 체크포인트만 유지
        )
        
        # 트레이너 생성
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self.compute_metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
        )
        
        # 훈련 시작
        logger.info(f"훈련 시작 - Epochs: {epochs}, Batch Size: {batch_size}, Learning Rate: {learning_rate}")
        trainer.train()
        
        # 최종 평가
        logger.info("최종 평가 중...")
        eval_results = trainer.evaluate()
        logger.info(f"최종 검증 정확도: {eval_results['eval_accuracy']:.4f}")
        
        # 모델 저장
        final_model_path = "app/koelectra/koelectra_model_finetuned"
        trainer.save_model(final_model_path)
        self.tokenizer.save_pretrained(final_model_path)
        
        logger.info(f"파인튜닝된 모델 저장 완료: {final_model_path}")
        
        return {
            "final_accuracy": eval_results['eval_accuracy'],
            "model_path": final_model_path,
            "training_samples": len(train_dataset),
            "validation_samples": len(val_dataset),
            "epochs": epochs
        }
    
    def test_model(self, model_path: str = "app/koelectra/koelectra_model_finetuned"):
        """파인튜닝된 모델 테스트"""
        logger.info("파인튜닝된 모델 테스트 중...")
        
        # 파인튜닝된 모델 로드
        model = ElectraForSequenceClassification.from_pretrained(model_path)
        tokenizer = ElectraTokenizer.from_pretrained(model_path)
        model.eval()
        
        # 테스트 문장들
        test_sentences = [
            "이 영화는 정말 재미있고 감동적이었어요!",
            "너무 지루하고 재미없었습니다.",
            "연기가 훌륭하고 스토리도 완벽했어요.",
            "시간 낭비였습니다. 추천하지 않아요.",
            "최고의 영화 중 하나예요!",
            "스토리가 뻔하고 연기도 어색했어요."
        ]
        
        results = []
        for sentence in test_sentences:
            inputs = tokenizer(
                sentence,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )
            
            with torch.no_grad():
                outputs = model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_class = torch.argmax(probabilities, dim=-1).item()
                confidence = probabilities[0][predicted_class].item()
            
            sentiment = "긍정" if predicted_class == 1 else "부정"
            results.append({
                "text": sentence,
                "sentiment": sentiment,
                "confidence": confidence
            })
            
            logger.info(f"'{sentence}' -> {sentiment} ({confidence:.4f})")
        
        return results

def main():
    """메인 실행 함수"""
    try:
        # 트레이너 초기화
        trainer = KoELECTRATrainer()
        
        # 모델 훈련 (5 epochs)
        training_results = trainer.train(epochs=5, batch_size=8, learning_rate=2e-5)
        
        logger.info("=== 훈련 완료 ===")
        logger.info(f"최종 정확도: {training_results['final_accuracy']:.4f}")
        logger.info(f"훈련 샘플: {training_results['training_samples']}")
        logger.info(f"검증 샘플: {training_results['validation_samples']}")
        
        # 모델 테스트
        test_results = trainer.test_model()
        
        logger.info("=== 파인튜닝 완료 ===")
        return training_results
        
    except Exception as e:
        logger.error(f"훈련 중 오류 발생: {str(e)}")
        raise

if __name__ == "__main__":
    main()
