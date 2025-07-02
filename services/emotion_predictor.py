import numpy as np
from typing import Dict
from models.model_loader import model_loader
from services.image_processor import ImageProcessor
from utils.exceptions import ModelNotLoadedException, PredictionException

class EmotionPredictor:
    """감정 예측 클래스"""
    
    @staticmethod
    def predict(image_bytes: bytes, filename: str = None) -> Dict:
        """감정을 예측합니다"""
        
        # 모델 로드 확인
        if not model_loader.is_loaded:
            raise ModelNotLoadedException()
        
        try:
            # 이미지 전처리
            processed_image = ImageProcessor.preprocess_image(image_bytes)
            
            # 모델과 라벨 가져오기
            model = model_loader.get_model()
            emotion_labels = model_loader.get_emotion_labels()
            
            # 예측 수행
            predictions = model.predict(processed_image, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])
            
            # 모든 클래스의 확률
            all_predictions = {
                emotion_labels[i]: float(predictions[0][i]) 
                for i in range(len(emotion_labels))
            }
            
            # 디버깅 정보 출력
            print(f"Raw predictions: {predictions[0]}")
            print(f"Predicted class: {predicted_class}")
            print(f"Predicted emotion: {emotion_labels[predicted_class]}")
            
            result = {
                "predicted_emotion": emotion_labels[predicted_class],
                "confidence": confidence,
                "all_predictions": all_predictions,
                "filename": filename
            }
            
            return result
            
        except Exception as e:
            raise PredictionException(str(e))
