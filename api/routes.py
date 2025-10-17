from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import Dict
from PIL import Image
import io
import httpx
from services.emotion_predictor import EmotionPredictor
from utils.exceptions import (
    InvalidFileTypeException, 
    FileSizeException,
    InvalidImageException,
    ImageDownloadException,
    ImageDownloadTimeoutException
    )
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


@router.post("/analyze/url")
async def analyze_emotion_by_url(image_url: str = Form(...)) -> Dict:
    try:
        # URL에서 이미지 다운로드
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(str(image_url))
            
            if response.status_code != 200:
                raise ImageDownloadException()
            
            image_bytes = response.content
        
        # 파일 크기 확인 (10MB 제한)
        if len(image_bytes) > 10 * 1024 * 1024:
            raise FileSizeException()
        
        # 유효한 이미지인지 검사
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
        except Exception:
            raise InvalidImageException()
        
        # 감정 예측
        result = EmotionPredictor.predict(image_bytes, str(image_url))
        return result
    
    except httpx.TimeoutException:
        raise ImageDownloadTimeoutException()
    except httpx.RequestError:
        raise ImageDownloadException()