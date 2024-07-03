from abc import ABC, abstractmethod
from app.api.unit_of_work import UnitOfWork


class BaseService(ABC):
    @abstractmethod
    async def execute(self, uow: UnitOfWork, **kwargs):
        pass

    @classmethod
    async def __call__(cls, uow: UnitOfWork, **kwargs):
        return await cls().execute(uow, **kwargs)
