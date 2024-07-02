from typing import List, Dict, Any

from app.api.models import TradeResult
from app.api.unit_of_work import UnitOfWork


async def save_data_to_db(data: List[Dict[str, Any]], uow: UnitOfWork) -> None:
    """
    Сохраняет данные в базу данных используя Unit of Work.

    :param data: Список словарей с данными для сохранения.
    :param uow: Экземпляр Unit of Work.
    """
    print("Saving data to database...")
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
            await uow.trade_result_repository.add(trade_result)
    except Exception as e:
        raise e
