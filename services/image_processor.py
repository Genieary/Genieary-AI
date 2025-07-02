import numpy as np
from PIL import Image
import io
import cv2
from config import settings
from utils.exceptions import ImageProcessingException

class ImageProcessor:
    """이미지 전처리 클래스"""
    
    @staticmethod
    def preprocess_image(image_bytes: bytes) -> np.ndarray:
        """Colab과 정확히 동일한 전처리 함수"""
        try:
            # PIL Image로 변환
            image = Image.open(io.BytesIO(image_bytes))
            
            # numpy 배열로 변환
            image_array = np.array(image)
            
            # RGB를 BGR로 변환 (OpenCV 형식에 맞춤)
            if len(image_array.shape) == 3:
                if image_array.shape[2] == 3:  # RGB 이미지인 경우
                    image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            
            # OpenCV로 그레이스케일 변환 (Colab과 동일)
            if len(image_array.shape) == 3:
                gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            else:
                gray_image = image_array
            
            # 48x48로 리사이즈 (Colab과 동일)
            resized_image = cv2.resize(gray_image, settings.IMAGE_SIZE)
            
            # reshape으로 (48, 48, 1) 형태 만들기 (Colab과 동일)
            img_array = resized_image.reshape(
                settings.IMAGE_SIZE[0], 
                settings.IMAGE_SIZE[1], 
                1
            )
            
            # float32로 변환 후 255.0으로 나누어 정규화 (Colab과 동일)
            img_array = img_array.astype('float32') / 255.0
            
            # 배치 차원 추가 (예측을 위해)
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise ImageProcessingException(str(e))
    
    @staticmethod
    def get_debug_info(image_bytes: bytes) -> dict:
        """디버깅용 이미지 정보 추출"""
        try:
            # 원본 이미지 정보
            original_image = Image.open(io.BytesIO(image_bytes))
            
            # 전처리된 이미지
            processed_image = ImageProcessor.preprocess_image(image_bytes)
            
            return {
                "original_size": original_image.size,
                "original_mode": original_image.mode,
                "processed_shape": processed_image.shape,
                "processed_dtype": str(processed_image.dtype),
                "processed_range": f"{processed_image.min():.6f} ~ {processed_image.max():.6f}",
                "processed_mean": float(processed_image.mean()),
                "processed_std": float(processed_image.std())
            }
        except Exception as e:
            raise ImageProcessingException(str(e))
