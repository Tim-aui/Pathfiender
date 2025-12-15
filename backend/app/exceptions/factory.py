from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class ExceptionResponseFactory:
    def __init__(self, status_code: int):
        self.status_code = status_code
    
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        detail = getattr(exc, 'detail', str(exc))
        return JSONResponse(
            content={"detail": detail},
            status_code=self.status_code
        )