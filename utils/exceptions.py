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
        
class InvalidImageException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, 
            detail="유효하지 않은 이미지입니다."
        )
        
class FileSizeException(HTTPException):
     def __init__(self):
        super().__init__(
            status_code=413, 
            detail="파일 크기가 너무 큽니다. 10MB 이하의 파일을 업로드해주세요."
        )

class PredictionException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=500, 
            detail=f"예측 중 오류 발생: {detail}"
        )
