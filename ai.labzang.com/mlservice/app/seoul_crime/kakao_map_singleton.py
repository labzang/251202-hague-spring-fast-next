import os
import logging
from pathlib import Path
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class KakaoMapSingleton:
    _instance = None  # 싱글턴 인스턴스를 저장할 클래스 변수

    def __new__(cls):
        if cls._instance is None:  # 인스턴스가 없으면 생성
            cls._instance = super(KakaoMapSingleton, cls).__new__(cls)
            cls._instance._api_key = cls._instance._retrieve_api_key()  # API 키 가져오기
            cls._instance._base_url = "https://dapi.kakao.com/v2/local"  # 카카오맵 API 기본 URL
        return cls._instance  # 기존 인스턴스 반환

    def _retrieve_api_key(self):
        """API 키를 환경 변수 또는 .env 파일에서 가져오는 내부 메서드"""
        # 1) 환경 변수 우선 (Docker 환경 변수 포함)
        api_key = os.getenv('KAKAO_REST_API_KEY') or os.getenv('KAKAO_API_KEY')
        if api_key:
            return api_key

        # 2) .env 파일에서 읽기 시도 (여러 경로 확인)
        current_file = Path(__file__)
        possible_paths = [
            current_file.parent.parent.parent.parent / '.env',   # ai.labzang.com/.env
            current_file.parent.parent.parent / '.env',          # mlservice/.env
            current_file.parent.parent / '.env',                 # app/.env
            Path('.env'),                                        # 현재 작업 디렉토리
            Path('/app/.env'),                                   # Docker 컨테이너 루트
        ]
        env_file = None
        for path in possible_paths:
            if path.exists():
                env_file = path
                break

        if env_file:
            load_dotenv(env_file)
            logger.info(f":열린_파일_폴더: .env 파일 로드: {env_file}")
        else:
            load_dotenv()  # 기본 경로 시도

        # 3) 다시 환경 변수 확인
        api_key = os.getenv('KAKAO_REST_API_KEY') or os.getenv('KAKAO_API_KEY')
        if not api_key:
            raise ValueError(
                "카카오 REST API 키를 찾을 수 없습니다. "
                "환경 변수 또는 .env 파일에 KAKAO_REST_API_KEY 또는 KAKAO_API_KEY를 설정해주세요. "
                f"시도한 경로: {[str(p) for p in possible_paths]}"
            )
        return api_key

    def get_api_key(self):
        """저장된 API 키 반환"""
        return self._api_key

    def geocode(self, address, language='ko'):
        """
        주소 또는 장소명을 좌표로 변환 (카카오맵 API, keyword 검색)
        Google Maps API 호환 형태로 반환
        """
        url = f"{self._base_url}/search/keyword.json"
        headers = {'Authorization': f'KakaoAK {self._api_key}'}
        params = {'query': address}

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 403:
                logger.error(f"카카오맵 API 403 오류 - 응답: {response.text}")
                logger.error(f"사용된 API 키(앞 10자): {self._api_key[:10]}...")
            response.raise_for_status()

            result = response.json()
            docs = result.get('documents', [])
            if not docs:
                logger.warning(f"카카오맵 검색 결과 없음: query='{address}'")
                return []

            doc = docs[0]
            # 가능한 필드 순서대로 주소 결정
            formatted_address = (
                doc.get('address_name', '') or
                doc.get('road_address_name', '') or
                doc.get('place_name', '')
            )

            # 좌표
            lat = float(doc.get('y', 0))
            lng = float(doc.get('x', 0))

            # 주소 컴포넌트
            address_info = doc.get('address', {}) or doc.get('road_address', {})
            formatted_result = [{
                'formatted_address': formatted_address,
                'geometry': {
                    'location': {
                        'lat': lat,
                        'lng': lng
                    }
                },
                'address_components': [
                    {
                        'long_name': address_info.get('region_1depth_name', ''),
                        'short_name': address_info.get('region_1depth_name', ''),
                        'types': ['administrative_area_level_1']
                    },
                    {
                        'long_name': address_info.get('region_2depth_name', ''),
                        'short_name': address_info.get('region_2depth_name', ''),
                        'types': ['administrative_area_level_2']
                    },
                    {
                        'long_name': address_info.get('region_3depth_name', ''),
                        'short_name': address_info.get('region_3depth_name', ''),
                        'types': ['locality']
                    }
                ]
            }]

            logger.info(
                f"카카오맵 검색 성공: query='{address}', "
                f"formatted='{formatted_address}', lat={lat}, lng={lng}"
            )
            return formatted_result

        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 403:
                logger.error(f"카카오맵 API 인증 오류 (403 Forbidden): API 키 확인 필요. URL: {url}")
            else:
                code = e.response.status_code if e.response is not None else "N/A"
                logger.error(f"카카오맵 API HTTP 오류 ({code}): {str(e)}")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"카카오맵 API 호출 오류: {str(e)}")
            return []

