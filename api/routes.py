from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
from PIL import Image
import io
from services.emotion_predictor import EmotionPredictor
from utils.exceptions import InvalidFileTypeException, FileSizeException,InvalidImageException
from models.model_loader import model_loader

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_loader.is_loaded
    }

@router.post("/analyze/file")
async def analyze_emotion_by_file(file: UploadFile = File(...)) -> Dict:
    # content-type 검사
    if not file.content_type.startswith("image/"):
        raise InvalidFileTypeException()
    
    # 파일 크기 확인 (10MB 제한)
    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise FileSizeException()
    
    # 유효한 이미지인지 검사
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
    except Exception:
        raise InvalidImageException()
    
    # 감정 예측
    result = EmotionPredictor.predict(image_bytes, file.filename)
    return result

#@router.post("/analyze/url")
#async def analyze_emotion_by_url() -> Dict:
    