from .base import BaseEntity


class Room(BaseEntity):
    """Класс для представления номера в отеле"""

    ROOM_TYPES = ["single", "double", "suite", "deluxe"]

    def __init__(
        self,
        id: int,
        number: int,
        room_type: str,
        price_per_night: float,
        capacity: int,
    ):
        super().__init__(id)
        self._number = number
        self._room_type = room_type
        self._price_per_night = price_per_night
        self._capacity = capacity
        self._is_available = True

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, value: int):
        if value <= 0:
            raise ValueError("Номер комнаты должен быть положительным числом")
        self._number = value

    @property
    def room_type(self) -> str:
        return self._room_type

    @room_type.setter
    def room_type(self, value: str):
        if value not in self.ROOM_TYPES:
            raise ValueError(
                f"Тип комнаты должен быть одним из: {', '.join(self.ROOM_TYPES)}"
            )
        self._room_type = value

    @property
    def price_per_night(self) -> float:
        return self._price_per_night

    @price_per_night.setter
    def price_per_night(self, value: float):
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price_per_night = value

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value: int):
        if value <= 0:
            raise ValueError("Вместимость должна быть положительным числом")
        self._capacity = value

    @property
    def is_available(self) -> bool:
        return self._is_available

    @is_available.setter
    def is_available(self, value: bool):
        self._is_available = value

    def calculate_stay_cost(self, nights: int) -> float:
        """Расчет стоимости проживания"""
        if nights <= 0:
            raise ValueError("Количество ночей должно быть положительным")
        return self.price_per_night * nights

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "number": self.number,
            "room_type": self.room_type,
            "price_per_night": self.price_per_night,
            "capacity": self.capacity,
            "is_available": self.is_available,
            "created_at": self.created_at.isoformat(),
        }

    def validate(self) -> bool:
        if (
            self.number <= 0
            or self.price_per_night < 0
            or self.capacity <= 0
            or self.room_type not in self.ROOM_TYPES
        ):
            return False
        return True

    def __add__(self, other):
        """Объединение номеров (для создания suite)"""
        if isinstance(other, Room):
            return self.price_per_night + other.price_per_night
        return NotImplemented

    def __lt__(self, other):
        """Сравнение номеров по цене"""
        if isinstance(other, Room):
            return self.price_per_night < other.price_per_night
        return NotImplemented
