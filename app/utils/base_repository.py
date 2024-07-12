from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Базовый класс репозитория для работы с асинхронной сессией SQLAlchemy.

    Этот класс предоставляет абстрактные методы CRUD для работы с данными.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Создать новую запись."""
        pass

    @abstractmethod
    async def read(self, id: Any) -> Optional[T]:
        """Прочитать запись по id."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Обновить существующую запись."""
        pass

    @abstractmethod
    async def delete(self, id: Any) -> bool:
        """Удалить запись по id."""
        pass

    @abstractmethod
    async def list(self, **kwargs) -> List[T]:
        """Получить список записей с возможностью фильтрации."""
        pass
