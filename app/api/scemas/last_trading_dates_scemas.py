from pydantic import BaseModel
from datetime import date
from typing import List


class LastTradingDatesResponse(BaseModel):
    status: str = "success"
    data: List[date]
    details: str = None
