"""
한글 폰트 설정 유틸리티
matplotlib에서 한글이 깨지지 않도록 폰트를 설정합니다.
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_korean_font():
    """
    한글 폰트 설정
    - Linux/Docker: Nanum 폰트 사용
    - Windows: 맑은 고딕 또는 나눔고딕 사용
    - macOS: Apple SD Gothic Neo 사용
    """
    system = platform.system()
    
    try:
        if system == "Linux":
            # Docker 컨테이너 환경 (Ubuntu/Debian)
            font_candidates = [
                "NanumGothic",
                "NanumBarunGothic", 
                "NanumSquare",
                "DejaVu Sans"
            ]
        elif system == "Windows":
            # Windows 환경
            font_candidates = [
                "Malgun Gothic",
                "NanumGothic",
                "NanumBarunGothic",
                "Arial Unicode MS"
            ]
        elif system == "Darwin":  # macOS
            # macOS 환경
            font_candidates = [
                "Apple SD Gothic Neo",
                "NanumGothic",
                "Arial Unicode MS"
            ]
        else:
            font_candidates = ["DejaVu Sans"]
        
        # 사용 가능한 폰트 찾기
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        selected_font = None
        
        for font in font_candidates:
            if font in available_fonts:
                selected_font = font
                break
        
        if selected_font:
            plt.rcParams['font.family'] = selected_font
            plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
            logger.info(f"한글 폰트 설정 완료: {selected_font}")
        else:
            logger.warning(f"한글 폰트를 찾을 수 없습니다. 사용 가능한 폰트: {font_candidates}")
            # 기본 폰트로 fallback
            plt.rcParams['axes.unicode_minus'] = False
            
    except Exception as e:
        logger.error(f"폰트 설정 중 오류 발생: {str(e)}")
        plt.rcParams['axes.unicode_minus'] = False


def get_available_korean_fonts():
    """사용 가능한 한글 폰트 목록 반환"""
    korean_fonts = []
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    korean_keywords = ['Nanum', 'Malgun', 'Gothic', 'Apple SD', 'Batang', 'Dotum']
    
    for font in available_fonts:
        for keyword in korean_keywords:
            if keyword in font:
                korean_fonts.append(font)
                break
    
    return list(set(korean_fonts))  # 중복 제거


def test_korean_font():
    """한글 폰트 테스트"""
    try:
        import matplotlib.pyplot as plt
        
        # 테스트 플롯 생성
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, '한글 테스트: 안녕하세요!', 
                fontsize=20, ha='center', va='center')
        ax.set_title('한글 폰트 테스트')
        
        # 메모리에서 이미지 생성 (실제 파일로 저장하지 않음)
        import io
        import base64
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        
        # base64 인코딩
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return {
            "status": "success",
            "message": "한글 폰트 테스트 완료",
            "font": plt.rcParams['font.family'],
            "image_base64": image_base64
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"한글 폰트 테스트 실패: {str(e)}",
            "font": None,
            "image_base64": None
        }


# 모듈 import 시 자동으로 한글 폰트 설정
setup_korean_font()
