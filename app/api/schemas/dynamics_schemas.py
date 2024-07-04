from datetime import date

from pydantic import BaseModel
from typing import List, Optional

from app.api.schemas.trade_result_schemas import TradeResultSchema


class DynamicsResponse(BaseModel):
    status: str = "success"
    data: List[TradeResultSchema]


class DynamicsRequest(BaseModel):
    oil_id: Optional[str] = None
    delivery_type_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
