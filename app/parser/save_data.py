from typing import List, Dict, Any

from app.database import async_session_maker
from app.api.models import TradeResult


async def save_data_to_db(data: List[Dict[str, Any]]) -> None:
    """
    Сохраняет данные в базу данных.

    :param data: Список словарей с данными для сохранения.
    """
    print("Saving data to database...")
    async with async_session_maker() as session:
        async with session.begin():
            try:
                for item in data:
                    exchange_product_id = item["exchange_product_id"]
                    oil_id = exchange_product_id[:4]
                    delivery_basis_id = exchange_product_id[4:7]
                    delivery_type_id = exchange_product_id[-1]

                    trade_result = TradeResult(
                        exchange_product_id=exchange_product_id,
                        exchange_product_name=item["exchange_product_name"],
                        oil_id=oil_id,
                        delivery_basis_id=delivery_basis_id,
                        delivery_basis_name=item["delivery_basis_name"],
                        delivery_type_id=delivery_type_id,
                        volume=item["volume"],
                        total=item["total"],
                        count=item["count"],
                        date=item["date"],
                    )
                    session.add(trade_result)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
