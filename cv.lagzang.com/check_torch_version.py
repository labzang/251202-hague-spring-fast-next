"""
PyTorch 및 관련 패키지 버전 확인 스크립트
"""
import sys

print("=" * 60)
print("Python 및 PyTorch 환경 정보")
print("=" * 60)

# Python 버전
print(f"\nPython 버전: {sys.version}")
print(f"Python 실행 경로: {sys.executable}")

# PyTorch 버전 확인
try:
    import torch
    print(f"\n[OK] PyTorch 버전: {torch.__version__}")
    
    # CUDA 사용 가능 여부
    print(f"CUDA 사용 가능: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA 버전: {torch.version.cuda}")
        print(f"cuDNN 버전: {torch.backends.cudnn.version()}")
        print(f"GPU 개수: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("[WARNING] CUDA를 사용할 수 없습니다 (CPU 모드)")
        
except ImportError:
    print("\n[ERROR] PyTorch가 설치되어 있지 않습니다.")
    print("   설치 명령어: pip install torch torchvision torchaudio")

# torchvision 버전 확인
try:
    import torchvision
    print(f"\n[OK] torchvision 버전: {torchvision.__version__}")
except ImportError:
    print("\n[WARNING] torchvision이 설치되어 있지 않습니다.")

# ultralytics (YOLO) 버전 확인
try:
    from ultralytics import YOLO
    import ultralytics
    print(f"\n[OK] ultralytics (YOLO) 버전: {ultralytics.__version__}")
except ImportError:
    print("\n[WARNING] ultralytics (YOLO)가 설치되어 있지 않습니다.")
    print("   설치 명령어: pip install ultralytics")

# 기타 패키지 버전 확인
packages = {
    "numpy": "numpy",
    "cv2": "opencv-python",
    "matplotlib": "matplotlib",
}

print("\n" + "=" * 60)
print("기타 패키지 버전")
print("=" * 60)

for module_name, package_name in packages.items():
    try:
        module = __import__(module_name)
        version = getattr(module, "__version__", "버전 정보 없음")
        print(f"[OK] {package_name}: {version}")
    except ImportError:
        print(f"[WARNING] {package_name}: 설치되지 않음")

print("\n" + "=" * 60)

