from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TradeResultSchema(BaseModel):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: Optional[str]
    delivery_type_id: Optional[str]
    volume: float
    total: float
    count: int
    date: datetime
    created_on: datetime = Field(default_factory=datetime.utcnow)
    updated_on: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
