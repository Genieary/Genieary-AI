import tensorflow as tf
import pickle
import os
from typing import Optional, List
from config import settings

class ModelLoader:
    """모델 로딩 및 관리 클래스"""
    
    def __init__(self):
        self.model: Optional[tf.keras.Model] = None
        self.emotion_labels: List[str] = settings.EMOTION_LABELS
        self.is_loaded: bool = False
    
    async def load_model(self) -> None:
        """모델과 라벨을 로드합니다"""
        try:
            # 모델 파일 존재 확인
            if not os.path.exists(settings.MODEL_PATH):
                raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {settings.MODEL_PATH}")
            
            # 모델 로드
            self.model = tf.keras.models.load_model(settings.MODEL_PATH)
            
            # 라벨 파일이 있다면 로드 (선택사항)
            if os.path.exists(settings.LABELS_PATH):
                with open(settings.LABELS_PATH, 'rb') as f:
                    self.emotion_labels = pickle.load(f)
                print(f"라벨 파일에서 로드된 감정 클래스: {self.emotion_labels}")
            else:
                print(f"기본 감정 클래스 사용: {self.emotion_labels}")
            
            self.is_loaded = True
            print("모델이 성공적으로 로드되었습니다.")
            print(f"모델 경로: {settings.MODEL_PATH}")
            
        except Exception as e:
            self.is_loaded = False
            print(f"모델 로드 중 오류 발생: {e}")
            raise e
    
    def get_model(self) -> tf.keras.Model:
        """로드된 모델을 반환합니다"""
        if not self.is_loaded or self.model is None:
            raise ValueError("모델이 로드되지 않았습니다.")
        return self.model
    
    def get_emotion_labels(self) -> List[str]:
        """감정 라벨을 반환합니다"""
        return self.emotion_labels

# 전역 모델 로더 인스턴스
model_loader = ModelLoader()
