from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Gateway API",
    description="Gateway 서비스 API 문서",
    version="1.0.0"
)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)

