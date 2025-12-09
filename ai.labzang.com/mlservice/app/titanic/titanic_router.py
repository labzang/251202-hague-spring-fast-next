"""
타이타닉 관련 라우터
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

# 공통 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.titanic.titanic_service import TitanicService
from common.utils import create_response, create_error_response

router = APIRouter(prefix="/titanic", tags=["titanic"])

# 서비스 인스턴스 생성 (싱글톤 패턴)
_service_instance: Optional[TitanicService] = None


def get_service() -> TitanicService:
    """TitanicService 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = TitanicService()
    return _service_instance


@router.get("/")
async def titanic_root():
    """타이타닉 서비스 루트"""
    return create_response(
        data={"service": "mlservice", "module": "titanic", "status": "running"},
        message="Titanic Service is running"
    )


@router.get("/health")
async def health_check():
    """헬스 체크"""
    try:
        service = get_service()
        service.load_train_data()
        return create_response(
            data={"status": "healthy", "service": "titanic"},
            message="Titanic service is healthy"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")


@router.get("/preprocess")
async def preprocess_data():
    """
    타이타닉 데이터 전처리 실행
    - 피처 삭제, 인코딩, 결측치 처리 등 전체 전처리 파이프라인 실행
    """
    try:
        service = get_service()
        result = service.preprocess()
        return create_response(
            data=result,
            message="데이터 전처리가 완료되었습니다"
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"데이터 파일을 찾을 수 없습니다: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"전처리 중 오류가 발생했습니다: {str(e)}"
        )
