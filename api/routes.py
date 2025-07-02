from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
from services.emotion_predictor import EmotionPredictor
from services.image_processor import ImageProcessor
from utils.exceptions import InvalidFileTypeException
from models.model_loader import model_loader

router = APIRouter()

@router.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "감정 분석 API에 오신 것을 환영합니다!",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict - 이미지 업로드하여 감정 예측",
            "debug_predict": "/debug_predict - 디버깅용 이미지 정보 확인",
            "health": "/health - 서버 상태 확인"
        }
    }

@router.get("/health")
async def health_check():
    """서버 상태 확인 엔드포인트"""
    return {
        "status": "healthy",
        "model_loaded": model_loader.is_loaded,
        "emotion_labels": model_loader.get_emotion_labels() if model_loader.is_loaded else None
    }

@router.post("/predict")
async def predict_emotion(file: UploadFile = File(...)) -> Dict:
    """감정 예측 엔드포인트"""
    
    # 파일 타입 검증 (utils/exceptions.py에서 정의된 예외 사용)
    if not file.content_type or not file.content_type.startswith('image/'):
        raise InvalidFileTypeException()
    
    # 파일 크기 확인 (10MB 제한)
    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413, 
            detail="파일 크기가 너무 큽니다. 10MB 이하의 파일을 업로드해주세요."
        )
    
    # 감정 예측 (services/emotion_predictor.py에서 예외 처리됨)
    result = EmotionPredictor.predict(image_bytes, file.filename)
    return result

@router.post("/debug_predict")
async def debug_predict(file: UploadFile = File(...)):
    """디버깅용 엔드포인트"""
    
    # 파일 타입 검증
    if not file.content_type or not file.content_type.startswith('image/'):
        raise InvalidFileTypeException()
    
    # 이미지 읽기 및 디버깅 정보 반환
    image_bytes = await file.read()
    debug_info = ImageProcessor.get_debug_info(image_bytes)
    
    # 추가 정보
    debug_info.update({
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size_mb": round(len(image_bytes) / (1024 * 1024), 2)
    })
    
    return debug_info
