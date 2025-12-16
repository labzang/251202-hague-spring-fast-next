"""
TransformerService 설정 파일
KoELECTRA 감성분석 서비스 환경 설정
"""

import os
from pathlib import Path
from typing import Optional

class TransformerConfig:
    """TransformerService 설정 클래스"""
    
    # ========================================================================
    # 기본 서비스 설정
    # ========================================================================
    SERVICE_NAME: str = "TransformerService"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = int(os.getenv("TRANSFORMER_PORT", "9020"))
    
    # ========================================================================
    # KoELECTRA 모델 설정
    # ========================================================================
    
    # 모델 경로 설정
    MODEL_BASE_PATH: str = "app/koelectra"
    KOELECTRA_MODEL_PATH: str = "app/koelectra/koelectra_model"
    
    # 허깅페이스 모델 설정 (대안)
    HUGGINGFACE_MODEL_NAME: str = "monologg/koelectra-small-v3-discriminator"
    
    # 모델 캐시 설정
    MODEL_CACHE_DIR: str = "app/koelectra/cache"
    TRANSFORMERS_CACHE: str = os.getenv("TRANSFORMERS_CACHE", MODEL_CACHE_DIR)
    
    # ========================================================================
    # 토크나이저 설정
    # ========================================================================
    MAX_SEQUENCE_LENGTH: int = 512
    TOKENIZER_DO_LOWER_CASE: bool = False
    PADDING: str = "max_length"
    TRUNCATION: bool = True
    
    # ========================================================================
    # 추론 설정
    # ========================================================================
    
    # 디바이스 설정
    USE_GPU: bool = os.getenv("USE_GPU", "true").lower() == "true"
    DEVICE: str = "cuda" if USE_GPU else "cpu"
    
    # 배치 처리 설정
    MAX_BATCH_SIZE: int = int(os.getenv("MAX_BATCH_SIZE", "50"))
    DEFAULT_BATCH_SIZE: int = int(os.getenv("DEFAULT_BATCH_SIZE", "8"))
    
    # 신뢰도 임계값
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
    
    # ========================================================================
    # API 설정
    # ========================================================================
    
    # 텍스트 길이 제한
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "1000"))
    MIN_TEXT_LENGTH: int = int(os.getenv("MIN_TEXT_LENGTH", "1"))
    
    # 요청 제한
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "100"))
    
    # ========================================================================
    # 로깅 설정
    # ========================================================================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ========================================================================
    # 성능 설정
    # ========================================================================
    
    # 모델 로딩 설정
    LAZY_LOADING: bool = os.getenv("LAZY_LOADING", "true").lower() == "true"
    PRELOAD_MODEL: bool = os.getenv("PRELOAD_MODEL", "false").lower() == "true"
    
    # 메모리 관리
    CLEAR_CACHE_AFTER_INFERENCE: bool = os.getenv("CLEAR_CACHE_AFTER_INFERENCE", "false").lower() == "true"
    
    # ========================================================================
    # 감성 분류 설정
    # ========================================================================
    
    # 레이블 매핑
    SENTIMENT_LABELS = {
        0: "부정",
        1: "긍정"
    }
    
    # 영어 레이블 (국제화 대응)
    SENTIMENT_LABELS_EN = {
        0: "negative",
        1: "positive"
    }
    
    # ========================================================================
    # 헬스체크 설정
    # ========================================================================
    HEALTH_CHECK_TIMEOUT: int = int(os.getenv("HEALTH_CHECK_TIMEOUT", "30"))
    HEALTH_CHECK_TEXT: str = "이것은 테스트 문장입니다."
    
    # ========================================================================
    # 개발/프로덕션 설정
    # ========================================================================
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS 설정
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://labzang.com",
        "https://api.labzang.com"
    ]
    
    # ========================================================================
    # 유틸리티 메서드
    # ========================================================================
    
    @classmethod
    def get_model_path(cls) -> Path:
        """모델 경로 반환"""
        return Path(cls.KOELECTRA_MODEL_PATH)
    
    @classmethod
    def get_cache_path(cls) -> Path:
        """캐시 경로 반환"""
        cache_path = Path(cls.MODEL_CACHE_DIR)
        cache_path.mkdir(parents=True, exist_ok=True)
        return cache_path
    
    @classmethod
    def is_model_available(cls) -> bool:
        """로컬 모델 사용 가능 여부 확인"""
        model_path = cls.get_model_path()
        required_files = [
            "config.json",
            "pytorch_model.bin",
            "tokenizer_config.json",
            "vocab.txt"
        ]
        
        return all((model_path / file).exists() for file in required_files)
    
    @classmethod
    def get_device_info(cls) -> dict:
        """디바이스 정보 반환"""
        import torch
        
        return {
            "device": cls.DEVICE,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "cuda_current_device": torch.cuda.current_device() if torch.cuda.is_available() else None
        }
    
    @classmethod
    def validate_config(cls) -> dict:
        """설정 유효성 검사"""
        issues = []
        
        # 모델 파일 존재 여부 확인
        if not cls.is_model_available():
            issues.append("로컬 모델 파일이 없습니다. 허깅페이스에서 다운로드됩니다.")
        
        # GPU 설정 확인
        if cls.USE_GPU:
            import torch
            if not torch.cuda.is_available():
                issues.append("GPU 사용이 설정되었지만 CUDA를 사용할 수 없습니다.")
        
        # 디렉토리 생성
        cls.get_cache_path()  # 캐시 디렉토리 생성
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "model_available": cls.is_model_available(),
            "device_info": cls.get_device_info()
        }

# ============================================================================
# 전역 설정 인스턴스
# ============================================================================

config = TransformerConfig()

# ============================================================================
# 환경변수 설정 함수
# ============================================================================

def setup_environment():
    """환경변수 설정"""
    os.environ["TRANSFORMERS_CACHE"] = config.TRANSFORMERS_CACHE
    os.environ["HF_HOME"] = config.MODEL_CACHE_DIR
    
    # 로깅 레벨 설정
    import logging
    logging.getLogger("transformers").setLevel(getattr(logging, config.LOG_LEVEL))
    logging.getLogger("torch").setLevel(logging.WARNING)

# 초기화 시 환경 설정
setup_environment()
