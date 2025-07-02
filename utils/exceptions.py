from fastapi import HTTPException

class ModelNotLoadedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=503, 
            detail="모델이 로드되지 않았습니다."
        )

class ImageProcessingException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=400, 
            detail=f"이미지 처리 중 오류: {detail}"
        )

class InvalidFileTypeException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, 
            detail="이미지 파일만 업로드 가능합니다."
        )

class PredictionException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=500, 
            detail=f"예측 중 오류 발생: {detail}"
        )
