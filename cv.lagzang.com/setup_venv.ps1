# Python 3.12.x로 가상환경 생성 및 패키지 설치 스크립트
# CUDA 12.1 또는 12.4 지원

# 1. 가상환경 생성 (Python 3.12 사용)
# Python 3.12가 py launcher로 설치되어 있다면:
# py -3.12 -m venv venv
# 또는 직접 경로 지정:
# C:\Python312\python.exe -m venv venv

python -m venv venv

# 2. 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 3. pip 업그레이드
python -m pip install --upgrade pip

# 4. PyTorch 설치 (CUDA 12.1 또는 12.4 지원)
# CUDA 12.1용:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 또는 CUDA 12.4용 (12.4는 12.1과 호환되므로 cu121 사용 가능):
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 5. YOLO11 (ultralytics 최신) 설치
pip install ultralytics

# 6. 기타 필요한 패키지 설치
pip install opencv-python matplotlib numpy

# 7. 설치 확인
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"
python -c "from ultralytics import YOLO; print('YOLO11 설치 완료')"

Write-Host "가상환경 설정이 완료되었습니다!" -ForegroundColor Green

