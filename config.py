import os
from typing import List

class Settings:
    
    # 프로젝트 루트 경로
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 모델 파일 경로
    MODEL_DIR = os.path.join(BASE_DIR, "models", "saved_models")
    MODEL_PATH: str = os.path.join(MODEL_DIR, "emotion_model2.h5")
    LABELS_PATH: str = os.path.join(MODEL_DIR, "emotion_labels2.pkl")  # 필요시
    
    IMAGE_SIZE: tuple = (48, 48)
    
    # 감정 라벨 
    EMOTION_LABELS: List[str] = [
        'angry', 'disgust', 'fear', 'happy', 
        'neutral', 'sad', 'surprise'
    ]
    
    # CORS 설정
    ALLOW_ORIGINS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]

settings = Settings()
