from pydantic import BaseModel
from typing import Optional, Any


class ErrorResponse(BaseModel):
    status: str = "error"
    data: Optional[Any] = None
    details: str
