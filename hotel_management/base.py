from abc import ABC, abstractmethod
from datetime import datetime


class BaseEntity(ABC):
    """Абстрактный базовый класс для всех сущностей отеля"""

    def __init__(self, id: int):
        self._id = id
        self._created_at = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @abstractmethod
    def to_dict(self) -> dict:
        """Преобразование объекта в словарь"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Валидация данных объекта"""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
