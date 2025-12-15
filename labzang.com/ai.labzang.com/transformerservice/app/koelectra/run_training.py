"""
KoELECTRA 파인튜닝 실행 스크립트
Docker 컨테이너 내에서 훈련을 실행하기 위한 래퍼 스크립트
"""

import sys
import os
from pathlib import Path
import logging

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, '/app')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """환경 확인"""
    logger.info("=== 환경 확인 ===")
    
    # CUDA 사용 가능 여부
    try:
        import torch
        logger.info(f"PyTorch 버전: {torch.__version__}")
        logger.info(f"CUDA 사용 가능: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            logger.info(f"CUDA 디바이스 수: {torch.cuda.device_count()}")
            logger.info(f"현재 디바이스: {torch.cuda.current_device()}")
    except ImportError:
        logger.warning("PyTorch를 찾을 수 없습니다")
    
    # 데이터 파일 확인
    data_path = Path("/app/app/koelectra/data")
    if data_path.exists():
        json_files = list(data_path.glob("*.json"))
        logger.info(f"데이터 파일 수: {len(json_files)}")
        
        # 샘플 데이터 크기 확인
        total_size = sum(f.stat().st_size for f in json_files)
        logger.info(f"총 데이터 크기: {total_size / (1024*1024):.1f} MB")
    else:
        logger.error(f"데이터 폴더를 찾을 수 없습니다: {data_path}")
        return False
    
    # 모델 파일 확인
    model_path = Path("/app/app/koelectra/koelectra_model")
    if model_path.exists():
        required_files = ["config.json", "pytorch_model.bin", "tokenizer_config.json", "vocab.txt"]
        missing_files = [f for f in required_files if not (model_path / f).exists()]
        
        if missing_files:
            logger.error(f"필수 모델 파일이 없습니다: {missing_files}")
            return False
        else:
            logger.info("모든 필수 모델 파일이 존재합니다")
    else:
        logger.error(f"모델 폴더를 찾을 수 없습니다: {model_path}")
        return False
    
    return True

def run_training():
    """훈련 실행"""
    try:
        logger.info("=== KoELECTRA 파인튜닝 시작 ===")
        
        # 환경 확인
        if not check_environment():
            logger.error("환경 확인 실패")
            return False
        
        # 훈련 모듈 임포트 및 실행
        from app.koelectra.train_koelectra import KoELECTRATrainer
        
        # 트레이너 초기화
        trainer = KoELECTRATrainer(
            model_path="/app/app/koelectra/koelectra_model",
            data_path="/app/app/koelectra/data"
        )
        
        # 훈련 실행 (5 epochs)
        logger.info("훈련 시작 - 5 epochs")
        results = trainer.train(
            epochs=5,
            batch_size=8,  # 메모리 절약을 위해 작은 배치 크기
            learning_rate=2e-5
        )
        
        logger.info("=== 훈련 완료 ===")
        logger.info(f"최종 정확도: {results['final_accuracy']:.4f}")
        logger.info(f"훈련 샘플 수: {results['training_samples']}")
        logger.info(f"검증 샘플 수: {results['validation_samples']}")
        logger.info(f"저장된 모델 경로: {results['model_path']}")
        
        # 테스트 실행
        logger.info("=== 모델 테스트 ===")
        test_results = trainer.test_model(results['model_path'])
        
        for result in test_results:
            logger.info(f"'{result['text']}' -> {result['sentiment']} ({result['confidence']:.4f})")
        
        return True
        
    except Exception as e:
        logger.error(f"훈련 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_training()
    sys.exit(0 if success else 1)
