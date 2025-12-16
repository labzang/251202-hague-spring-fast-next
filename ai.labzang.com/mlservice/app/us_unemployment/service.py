import pandas as pd
import folium
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class USUnemploymentService:
    """미국 실업률 지도 시각화 서비스"""
    
    def __init__(self):
        self.state_geo_url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
        self.state_data_url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
        self.state_geo = None
        self.state_data = None
        self.map = None
        
    def load_geo_data(self) -> Dict[str, Any]:
        """지리 데이터(GeoJSON) 로드"""
        try:
            logger.info("미국 주 경계 GeoJSON 데이터 로드 중...")
            response = requests.get(self.state_geo_url)
            response.raise_for_status()
            self.state_geo = response.json()
            logger.info(f"GeoJSON 데이터 로드 완료: {len(self.state_geo.get('features', []))}개 주")
            return self.state_geo
        except Exception as e:
            logger.error(f"GeoJSON 데이터 로드 실패: {str(e)}")
            raise
    
    def load_unemployment_data(self) -> pd.DataFrame:
        """실업률 데이터 로드"""
        try:
            logger.info("미국 실업률 데이터 로드 중...")
            self.state_data = pd.read_csv(self.state_data_url)
            logger.info(f"실업률 데이터 로드 완료: {len(self.state_data)}개 주, 컬럼: {self.state_data.columns.tolist()}")
            return self.state_data
        except Exception as e:
            logger.error(f"실업률 데이터 로드 실패: {str(e)}")
            raise
    
    def create_base_map(self, location: list = [48, -102], zoom_start: int = 3) -> folium.Map:
        """기본 지도 생성"""
        logger.info(f"기본 지도 생성: 중심점 {location}, 줌 레벨 {zoom_start}")
        self.map = folium.Map(location=location, zoom_start=zoom_start)
        return self.map
    
    def add_choropleth_layer(self, 
                           fill_color: str = "YlGn",
                           fill_opacity: float = 0.7,
                           line_opacity: float = 0.2,
                           legend_name: str = "Unemployment Rate (%)") -> None:
        """코로플레스(단계구분도) 레이어 추가"""
        if not self.state_geo:
            raise ValueError("GeoJSON 데이터가 로드되지 않았습니다. load_geo_data()를 먼저 호출하세요.")
        
        if self.state_data is None:
            raise ValueError("실업률 데이터가 로드되지 않았습니다. load_unemployment_data()를 먼저 호출하세요.")
        
        if not self.map:
            raise ValueError("기본 지도가 생성되지 않았습니다. create_base_map()을 먼저 호출하세요.")
        
        logger.info("코로플레스 레이어 추가 중...")
        folium.Choropleth(
            geo_data=self.state_geo,
            name="choropleth",
            data=self.state_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            line_opacity=line_opacity,
            legend_name=legend_name,
        ).add_to(self.map)
        
        logger.info("코로플레스 레이어 추가 완료")
    
    def add_layer_control(self) -> None:
        """레이어 컨트롤 추가"""
        if not self.map:
            raise ValueError("기본 지도가 생성되지 않았습니다.")
        
        folium.LayerControl().add_to(self.map)
        logger.info("레이어 컨트롤 추가 완료")
    
    def generate_map(self, **kwargs) -> folium.Map:
        """전체 지도 생성 (모든 단계를 한 번에 실행)"""
        logger.info("미국 실업률 지도 생성 시작...")
        
        # 데이터 로드
        self.load_geo_data()
        self.load_unemployment_data()
        
        # 지도 생성
        location = kwargs.get('location', [48, -102])
        zoom_start = kwargs.get('zoom_start', 3)
        self.create_base_map(location=location, zoom_start=zoom_start)
        
        # 레이어 추가
        self.add_choropleth_layer(
            fill_color=kwargs.get('fill_color', 'YlGn'),
            fill_opacity=kwargs.get('fill_opacity', 0.7),
            line_opacity=kwargs.get('line_opacity', 0.2),
            legend_name=kwargs.get('legend_name', 'Unemployment Rate (%)')
        )
        
        # 컨트롤 추가
        self.add_layer_control()
        
        logger.info("미국 실업률 지도 생성 완료")
        return self.map
    
    def get_unemployment_stats(self) -> Optional[Dict[str, Any]]:
        """실업률 통계 정보 반환"""
        if self.state_data is None:
            return None
        
        stats = {
            "total_states": len(self.state_data),
            "avg_unemployment": self.state_data['Unemployment'].mean(),
            "max_unemployment": self.state_data['Unemployment'].max(),
            "min_unemployment": self.state_data['Unemployment'].min(),
            "max_state": self.state_data.loc[self.state_data['Unemployment'].idxmax(), 'State'],
            "min_state": self.state_data.loc[self.state_data['Unemployment'].idxmin(), 'State']
        }
        
        return stats


# 기존 코드와의 호환성을 위한 인스턴스 생성 및 실행
if __name__ == "__main__":
    service = USUnemploymentService()
    m = service.generate_map()