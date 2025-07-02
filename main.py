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
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    print("🚀 감정 분석 API 서버를 시작합니다...")
    try:
        await model_loader.load_model()
        print("✅ 모델 로딩 완료")
    except Exception as e:
        print(f"❌ 모델 로딩 실패: {e}")
        print("⚠️ 서버는 시작되지만 예측 기능이 작동하지 않을 수 있습니다.")
    
    yield
    
    # 종료 시 실행
    print("🛑 감정 분석 API 서버를 종료합니다...")

# FastAPI 앱 생성
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="""
    ## 감정 분석 API
    
    이미지에서 얼굴을 검출하고 7가지 감정을 분석하는 API입니다.
    
    ### 지원 감정
    - angry (화남) - disgust (혐오) - fear (두려움) - happy (행복)
    - neutral (중립) - sad (슬픔) - surprise (놀람)
    """,
    lifespan=lifespan
)

# CORS 설정 (config.py에서 가져온 설정 사용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

# 라우터 등록 (예외처리는 routes.py와 utils/exceptions.py에서 처리)
app.include_router(router)

def main():
    """메인 함수 - 서버 실행"""
    print(f"🌟 {settings.API_TITLE} v{settings.API_VERSION}")
    print(f"📡 서버 주소: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API 문서: http://{settings.HOST}:{settings.PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
