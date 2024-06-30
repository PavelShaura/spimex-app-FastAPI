from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime

from app.database import Base


class BaseModel(Base):
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class TradeResult(BaseModel):
    __tablename__ = "spimex_trading_results"
    id = Column(Integer, primary_key=True)
    exchange_product_id = Column(String, index=True)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(Float)
    total = Column(Float)
    count = Column(Integer)
    date = Column(DateTime)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    repr_cols = (
        "id",
        "exchange_product_id",
        "exchange_product_name",
        "oil_id",
    )  # <TradeResult id=3914, exchange_product_id=DT50SUR065F, exchange_product_name=ДТ вид 4 (ДТ-А-К5) минус 50, ст. Сургут (ст. отправления), oil_id=None, delivery_basis_id=None>
    repr_cols_num = 5
