"""
KoELECTRA 감성분석 API 라우터
영화 리뷰 감성분석을 위한 REST API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import logging

from .koelectra_service import get_sentiment_service
import asyncio
import subprocess
import sys

logger = logging.getLogger(__name__)

router = APIRouter(tags=["koelectra-sentiment"])

# ============================================================================
# Request/Response 모델
# ============================================================================

class SentimentRequest(BaseModel):
    """감성분석 요청 모델"""
    text: str = Field(..., description="감성분석할 텍스트", min_length=1, max_length=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "이 영화는 정말 재미있고 감동적이었어요!"
            }
        }

class BatchSentimentRequest(BaseModel):
    """배치 감성분석 요청 모델"""
    texts: List[str] = Field(..., description="감성분석할 텍스트 리스트", min_items=1, max_items=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "texts": [
                    "이 영화는 정말 재미있어요!",
                    "너무 지루하고 재미없었습니다.",
                    "연기가 훌륭하고 스토리도 좋았어요."
                ]
            }
        }

class SentimentResponse(BaseModel):
    """감성분석 응답 모델"""
    text: str
    sentiment: str
    confidence: float
    probabilities: Dict[str, float]
    model_info: Dict[str, Any]

# ============================================================================
# API 엔드포인트
# ============================================================================

@router.get("/")
async def koelectra_root():
    """KoELECTRA 서비스 루트"""
    return {
        "service": "transformerservice",
        "module": "koelectra",
        "status": "running",
        "description": "KoELECTRA 기반 한국어 감성분석 서비스"
    }

@router.post("/analyze")
async def analyze_sentiment(request: SentimentRequest):
    """
    단일 텍스트 감성분석
    
    - **text**: 감성분석할 텍스트 (최대 1000자)
    - 반환값: 감성(긍정/부정), 신뢰도, 확률 분포
    """
    try:
        service = get_sentiment_service()
        result = service.predict_sentiment(request.text)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result,
                "message": "감성분석이 완료되었습니다"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"감성분석 API 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"감성분석 처리 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/batch")
async def analyze_batch_sentiment(request: BatchSentimentRequest):
    """
    배치 텍스트 감성분석
    
    - **texts**: 감성분석할 텍스트 리스트 (최대 50개)
    - 반환값: 각 텍스트별 감성분석 결과 리스트
    """
    try:
        service = get_sentiment_service()
        results = service.predict_batch(request.texts)
        
        # 에러가 있는 결과 확인
        error_count = sum(1 for result in results if "error" in result)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "results": results,
                    "total_count": len(results),
                    "success_count": len(results) - error_count,
                    "error_count": error_count
                },
                "message": f"{len(results)}개 텍스트 배치 감성분석이 완료되었습니다"
            }
        )
        
    except Exception as e:
        logger.error(f"배치 감성분석 API 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"배치 감성분석 처리 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/quick")
async def quick_analyze(
    text: str = Query(..., description="감성분석할 텍스트", max_length=500)
):
    """
    빠른 감성분석 (GET 요청)
    
    - **text**: 감성분석할 텍스트 (쿼리 파라미터)
    - 간단한 테스트용 엔드포인트
    """
    try:
        service = get_sentiment_service()
        result = service.predict_sentiment(text)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "text": text,
                    "sentiment": result["sentiment"],
                    "confidence": result["confidence"]
                },
                "message": "빠른 감성분석이 완료되었습니다"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"빠른 감성분석 API 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"빠른 감성분석 처리 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/model/info")
async def get_model_info():
    """
    모델 정보 조회
    
    - KoELECTRA 모델의 상세 정보 반환
    """
    try:
        service = get_sentiment_service()
        model_info = service.get_model_info()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": model_info,
                "message": "모델 정보를 성공적으로 조회했습니다"
            }
        )
        
    except Exception as e:
        logger.error(f"모델 정보 조회 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"모델 정보 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    서비스 상태 확인
    
    - 모델 로딩 상태 및 서비스 정상 작동 여부 확인
    """
    try:
        service = get_sentiment_service()
        health_status = service.health_check()
        
        status_code = 200 if health_status["status"] == "healthy" else 503
        
        return JSONResponse(
            status_code=status_code,
            content={
                "success": health_status["status"] == "healthy",
                "data": health_status,
                "message": f"서비스 상태: {health_status['status']}"
            }
        )
        
    except Exception as e:
        logger.error(f"헬스체크 오류: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "data": {"status": "error", "error": str(e)},
                "message": "서비스 상태 확인 중 오류가 발생했습니다"
            }
        )

# ============================================================================
# 예제 엔드포인트
# ============================================================================

@router.get("/examples")
async def get_examples():
    """
    감성분석 예제 텍스트
    
    - 테스트용 예제 문장들 반환
    """
    examples = {
        "positive_examples": [
            "이 영화는 정말 재미있고 감동적이었어요!",
            "연기가 훌륭하고 스토리도 완벽했습니다.",
            "최고의 영화 중 하나예요. 강력 추천합니다!",
            "웃음과 감동을 동시에 주는 멋진 작품이었어요.",
            "배우들의 연기가 너무 자연스럽고 좋았습니다."
        ],
        "negative_examples": [
            "너무 지루하고 재미없었습니다.",
            "스토리가 뻔하고 연기도 어색했어요.",
            "시간 낭비였습니다. 추천하지 않아요.",
            "기대했는데 너무 실망스러웠습니다.",
            "졸면서 봤어요. 정말 재미없었습니다."
        ],
        "neutral_examples": [
            "그냥 평범한 영화였어요.",
            "나쁘지도 좋지도 않은 영화입니다.",
            "볼만은 하지만 특별하지는 않았어요."
        ]
    }
    
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": examples,
                "message": "감성분석 예제 텍스트를 제공합니다"
            }
        )

@router.post("/train")
async def train_model():
    """
    KoELECTRA 모델 파인튜닝
    
    - 영화 리뷰 데이터를 사용하여 모델을 5 epochs 동안 훈련
    - 훈련 완료 후 새로운 모델로 자동 전환
    """
    try:
        logger.info("KoELECTRA 모델 파인튜닝 시작...")
        
        # 백그라운드에서 훈련 실행
        process = await asyncio.create_subprocess_exec(
            sys.executable, 
            "app/koelectra/run_training.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="/app"
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            logger.info("모델 훈련 완료")
            
            # 서비스 인스턴스 재초기화 (새로운 모델 로드)
            global _service_instance
            _service_instance = None
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "KoELECTRA 모델 파인튜닝이 완료되었습니다",
                    "data": {
                        "epochs": 5,
                        "status": "completed",
                        "output": stdout.decode('utf-8') if stdout else "",
                    }
                }
            )
        else:
            error_msg = stderr.decode('utf-8') if stderr else "알 수 없는 오류"
            logger.error(f"훈련 실패: {error_msg}")
            
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "모델 훈련 중 오류가 발생했습니다",
                    "error": error_msg
                }
            )
            
    except Exception as e:
        logger.error(f"훈련 API 오류: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "훈련 실행 중 오류가 발생했습니다",
                "error": str(e)
            }
        )

@router.get("/training/status")
async def get_training_status():
    """
    훈련 상태 확인
    
    - 현재 사용 중인 모델 정보 반환
    - 파인튜닝된 모델 존재 여부 확인
    """
    try:
        from pathlib import Path
        
        base_model_path = Path("app/koelectra/koelectra_model")
        finetuned_model_path = Path("app/koelectra/koelectra_model_finetuned")
        
        status = {
            "base_model_exists": base_model_path.exists(),
            "finetuned_model_exists": finetuned_model_path.exists(),
            "current_model": "finetuned" if finetuned_model_path.exists() else "base",
            "data_files_count": len(list(Path("app/koelectra/data").glob("*.json"))) if Path("app/koelectra/data").exists() else 0
        }
        
        if finetuned_model_path.exists():
            # 파인튜닝된 모델의 수정 시간
            import os
            modified_time = os.path.getmtime(finetuned_model_path)
            from datetime import datetime
            status["finetuned_model_date"] = datetime.fromtimestamp(modified_time).isoformat()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": status,
                "message": "훈련 상태 정보를 성공적으로 조회했습니다"
            }
        )
        
    except Exception as e:
        logger.error(f"훈련 상태 조회 오류: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "훈련 상태 조회 중 오류가 발생했습니다",
                "error": str(e)
            }
        )
