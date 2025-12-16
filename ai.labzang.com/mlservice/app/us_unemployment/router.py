"""
미국 실업률 관련 라우터
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import Dict, Any, Optional
from pathlib import Path
import sys

# 공통 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.us_unemployment.service import USUnemploymentService
from common.utils import create_response, create_error_response
from app.common.font_utils import test_korean_font, get_available_korean_fonts
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["usa"])

# 서비스 인스턴스 생성 (싱글톤 패턴)
_service_instance: Optional[USUnemploymentService] = None


def get_service() -> USUnemploymentService:
    """USUnemploymentService 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = USUnemploymentService()
    return _service_instance


@router.get("/")
async def usa_root():
    """미국 실업률 서비스 루트"""
    return create_response(
        data={"service": "mlservice", "module": "usa", "status": "running"},
        message="USA Unemployment Service is running"
    )


@router.get("/stats")
async def get_unemployment_stats():
    """
    미국 실업률 통계 정보 조회
    - 전체 주 수, 평균/최대/최소 실업률, 최고/최저 실업률 주 정보
    """
    try:
        service = get_service()
        service.load_unemployment_data()
        stats = service.get_unemployment_stats()
        
        if stats is None:
            raise HTTPException(
                status_code=404,
                detail="실업률 데이터를 찾을 수 없습니다"
            )
        
        return create_response(
            data=stats,
            message="미국 실업률 통계 조회가 완료되었습니다"
        )
    except Exception as e:
        logger.error(f"실업률 통계 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"통계 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/map")
async def generate_unemployment_map(
    location_lat: float = Query(48, description="지도 중심 위도"),
    location_lng: float = Query(-102, description="지도 중심 경도"),
    zoom_start: int = Query(3, description="초기 줌 레벨"),
    fill_color: str = Query("YlGn", description="색상 팔레트 (YlGn, Blues, Reds 등)"),
    fill_opacity: float = Query(0.7, description="채우기 투명도 (0.0-1.0)"),
    line_opacity: float = Query(0.2, description="경계선 투명도 (0.0-1.0)"),
    legend_name: str = Query("Unemployment Rate (%)", description="범례 이름")
):
    """
    미국 실업률 지도 생성
    - 코로플레스(단계구분도) 방식으로 실업률을 시각화
    - 다양한 커스터마이징 옵션 제공
    """
    try:
        service = get_service()
        
        # 지도 생성
        folium_map = service.generate_map(
            location=[location_lat, location_lng],
            zoom_start=zoom_start,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            line_opacity=line_opacity,
            legend_name=legend_name
        )
        
        # HTML로 변환
        map_html = folium_map._repr_html_()
        
        return HTMLResponse(
            content=map_html,
            status_code=200,
            headers={"Content-Type": "text/html; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"지도 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"지도 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/data")
async def get_unemployment_data():
    """
    미국 실업률 원본 데이터 조회
    - 모든 주의 실업률 데이터를 JSON 형태로 반환
    """
    try:
        service = get_service()
        unemployment_data = service.load_unemployment_data()
        
        # DataFrame을 딕셔너리로 변환
        data_dict = unemployment_data.to_dict(orient='records')
        
        return create_response(
            data={
                "total_states": len(data_dict),
                "unemployment_data": data_dict
            },
            message="미국 실업률 데이터 조회가 완료되었습니다"
        )
        
    except Exception as e:
        logger.error(f"데이터 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"데이터 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/geo")
async def get_geo_data():
    """
    미국 주 경계 GeoJSON 데이터 조회
    - 지도 시각화에 사용되는 지리 정보 반환
    """
    try:
        service = get_service()
        geo_data = service.load_geo_data()
        
        return create_response(
            data={
                "type": geo_data.get("type"),
                "features_count": len(geo_data.get("features", [])),
                "geo_data": geo_data
            },
            message="미국 주 경계 GeoJSON 데이터 조회가 완료되었습니다"
        )
        
    except Exception as e:
        logger.error(f"GeoJSON 데이터 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"GeoJSON 데이터 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/font-test")
async def test_font():
    """
    한글 폰트 테스트
    - matplotlib에서 한글이 제대로 표시되는지 확인
    - 사용 가능한 한글 폰트 목록 반환
    """
    try:
        # 폰트 테스트 실행
        test_result = test_korean_font()
        
        # 사용 가능한 한글 폰트 목록
        available_fonts = get_available_korean_fonts()
        
        return create_response(
            data={
                "test_result": test_result,
                "available_korean_fonts": available_fonts,
                "total_korean_fonts": len(available_fonts)
            },
            message="한글 폰트 테스트가 완료되었습니다"
        )
        
    except Exception as e:
        logger.error(f"폰트 테스트 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"폰트 테스트 중 오류가 발생했습니다: {str(e)}"
        )
