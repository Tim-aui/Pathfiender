from fastapi import Request
from fastapi.responses import JSONResponse

class ExceptionResponseFactory:
    def __init__(self, status_code: int):
        self.status_code = status_code
    
    def __call__(self, request: Request, exception: Exception) -> JSONResponse:
        return JSONResponse(
            content={"message": getattr(exception, "message", str(exception))},
            status_code={self.status_code}
        )