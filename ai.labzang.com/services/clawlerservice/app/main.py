from fastapi import FastAPI, APIRouter
import uvicorn

# 서브라우터 생성
clawler_router = APIRouter(prefix="/clawler", tags=["clawler"])

@clawler_router.get("/")
async def clawler_root():
    return {"message": "Clawler Service", "status": "running"}

app = FastAPI(
    title="Clawler Service API",
    description="Clawler 서비스 API 문서",
    version="1.0.0"
)

# 서브라우터를 앱에 포함
app.include_router(clawler_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)

