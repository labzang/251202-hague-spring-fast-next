from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import shutil
import uvicorn

# yolo_detection 모듈 import
try:
    from yolo_detection import auto_detect_faces

    FACE_DETECTION_AVAILABLE = True
except ImportError:
    FACE_DETECTION_AVAILABLE = False
    print("[WARNING] yolo_detection 모듈을 import할 수 없습니다.")

app = FastAPI()

# CORS 설정 (Next.js 로컬 개발용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# data/yolo 경로 고정 (실행 위치와 무관)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "yolo"
DATA_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    파일 업로드 및 자동 얼굴 디텍션

    이미지 파일인 경우 자동으로 얼굴 디텍션을 수행하고
    결과 이미지를 -detected 접미사로 저장합니다.
    """
    try:
        # 파일명 충돌 방지
        original_filename = file.filename
        file_extension = Path(original_filename).suffix
        filename = f"{uuid.uuid4()}{file_extension}"
        save_path = DATA_DIR / filename

        # 파일 저장
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = {
            "message": "upload success",
            "filename": filename,
            "original_filename": original_filename,
            "path": str(save_path),
            "face_detection": None,
        }

        # 이미지 파일인 경우 자동으로 얼굴 디텍션 수행
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
        if file_extension.lower() in image_extensions:
            print(f"[INFO] 이미지 파일 감지: {filename}, 얼굴 디텍션 시작...")

            if FACE_DETECTION_AVAILABLE:
                try:
                    success, face_count, output_path = auto_detect_faces(str(save_path))

                    if success:
                        result["face_detection"] = {
                            "success": True,
                            "face_count": face_count,
                            "result_image_path": output_path,
                            "result_filename": Path(output_path).name,
                        }
                        print(
                            f"[SUCCESS] 얼굴 디텍션 완료: {face_count}개 감지, 결과: {output_path}"
                        )
                    else:
                        result["face_detection"] = {
                            "success": False,
                            "face_count": 0,
                            "message": "얼굴을 찾을 수 없습니다.",
                        }
                        print(
                            f"[WARNING] 얼굴 디텍션 실패 또는 얼굴을 찾을 수 없습니다."
                        )
                except Exception as e:
                    result["face_detection"] = {
                        "success": False,
                        "face_count": 0,
                        "error": str(e),
                    }
                    print(f"[ERROR] 얼굴 디텍션 중 오류 발생: {str(e)}")
            else:
                result["face_detection"] = {
                    "success": False,
                    "face_count": 0,
                    "message": "얼굴 디텍션 모듈을 사용할 수 없습니다.",
                }
                print(f"[WARNING] 얼굴 디텍션 모듈을 사용할 수 없습니다.")

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"파일 업로드 중 오류 발생: {str(e)}"
        )


@app.get("/health")
def health():
    """Health check 엔드포인트"""
    return {
        "status": "ok",
        "face_detection_available": FACE_DETECTION_AVAILABLE,
        "data_dir": str(DATA_DIR),
    }


@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "message": "YOLO Face Detection API",
        "endpoints": {"upload": "/api/upload", "health": "/health"},
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 개발 중 자동 리로드
    )
