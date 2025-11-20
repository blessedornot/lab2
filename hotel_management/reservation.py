from datetime import datetime, timedelta
from .base import BaseEntity


class Reservation(BaseEntity):
    """Класс для представления бронирования"""

    def __init__(
        self,
        id: int,
        guest_id: int,
        room_id: int,
        check_in_date: datetime,
        check_out_date: datetime,
        num_guests: int,
    ):
        super().__init__(id)
        self._guest_id = guest_id
        self._room_id = room_id
        self._check_in_date = check_in_date
        self._check_out_date = check_out_date
        self._num_guests = num_guests
        self._total_cost = 0.0
        self._status = "active"

    @property
    def guest_id(self) -> int:
        return self._guest_id

    @property
    def room_id(self) -> int:
        return self._room_id

    @property
    def check_in_date(self) -> datetime:
        return self._check_in_date

    @check_in_date.setter
    def check_in_date(self, value: datetime):
        if value < datetime.now():
            raise ValueError("Дата заезда не может быть в прошлом")
        self._check_in_date = value

    @property
    def check_out_date(self) -> datetime:
        return self._check_out_date

    @check_out_date.setter
    def check_out_date(self, value: datetime):
        if value <= self.check_in_date:
            raise ValueError("Дата выезда должна быть после даты заезда")
        self._check_out_date = value

    @property
    def num_guests(self) -> int:
        return self._num_guests

    @num_guests.setter
    def num_guests(self, value: int):
        if value <= 0:
            raise ValueError("Количество гостей должно быть положительным")
        self._num_guests = value

    @property
    def total_cost(self) -> float:
        return self._total_cost

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in ["active", "cancelled", "completed"]:
            raise ValueError("Некорректный статус бронирования")
        self._status = value

    def calculate_stay_cost(self, room_price: float) -> float:
        """Расчет стоимости проживания"""
        nights = (self.check_out_date - self.check_in_date).days
        if nights <= 0:
            raise ValueError("Минимальное время проживания - 1 ночь")

        self._total_cost = room_price * nights
        return self._total_cost

    def calculate_booking_deposit(self, room_price: float) -> float:
        """Расчет суммы бронирования (депозит)"""
        return room_price * 0.2  # 20% от стоимости номера

    def get_available_beds(self, room_capacity: int) -> int:
        """Расчет количества свободных мест в номере"""
        return room_capacity - self.num_guests

    def get_stay_duration(self) -> int:
        """Получение продолжительности проживания в днях"""
        return (self.check_out_date - self.check_in_date).days

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "guest_id": self.guest_id,
            "room_id": self.room_id,
            "check_in_date": self.check_in_date.isoformat(),
            "check_out_date": self.check_out_date.isoformat(),
            "num_guests": self.num_guests,
            "total_cost": self.total_cost,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

    def validate(self) -> bool:
        if (
            self.guest_id <= 0
            or self.room_id <= 0
            or self.num_guests <= 0
            or self.check_in_date >= self.check_out_date
        ):
            return False
        return True

    def __len__(self) -> int:
        """Получение длительности бронирования в днях"""
        return self.get_stay_duration()

    def __bool__(self) -> bool:
        """Проверка активности бронирования"""
        return self.status == "active" and self.check_in_date > datetime.now()
