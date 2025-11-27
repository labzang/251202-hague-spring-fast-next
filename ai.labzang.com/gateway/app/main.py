import uvicorn
import sys
import importlib.util
from pathlib import Path
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# 프로젝트 루트 경로 설정
project_root = Path(__file__).parent.parent.parent
clawler_main_path = project_root / "services" / "clawlerservice" / "app" / "main.py"

# clawler-service의 라우터 동적 import
spec = importlib.util.spec_from_file_location("clawler_main", clawler_main_path)
clawler_main = importlib.util.module_from_spec(spec)
sys.modules["clawler_main"] = clawler_main
spec.loader.exec_module(clawler_main)
clawler_router = clawler_main.clawler_router

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 origin만 허용하도록 변경
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 메인 라우터 생성
main_router = APIRouter()

@main_router.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# 라우터를 앱에 포함
app.include_router(main_router)
# clawler-service 서브라우터 연결
app.include_router(clawler_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)