import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.routes import router
from models.model_loader import model_loader
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행
    print("감정 분석 API 서버 시작")
    try:
        await model_loader.load_model()
        print("모델 로딩 완료")
    except Exception as e:
        print(f"모델 로딩 실패: {e}")    
    yield
    
    # 종료 시 실행
    print("서버 종료")

# FastAPI 앱 생성
app = FastAPI(
    title="감성 분석 API",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(router)

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
