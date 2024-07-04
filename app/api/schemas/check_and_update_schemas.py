from pydantic import BaseModel
from typing import Optional, Any


class CheckAndUpdateResponse(BaseModel):
    status: str = "success"
    data: Optional[Any]
