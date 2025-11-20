import re
from .base import BaseEntity


class Guest(BaseEntity):
    """Класс для представления гостя отеля"""

    def __init__(self, id: int, name: str, email: str, phone: str, passport: str):
        super().__init__(id)
        self._name = name
        self._email = email
        self._phone = phone
        self._passport = passport

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("Имя не может быть пустым")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not self._validate_email(value):
            raise ValueError("Некорректный email адрес")
        self._email = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        if not self._validate_phone(value):
            raise ValueError("Некорректный номер телефона")
        self._phone = value

    @property
    def passport(self) -> str:
        return self._passport

    @passport.setter
    def passport(self, value: str):
        if not value or len(value) < 5:
            raise ValueError("Некорректные паспортные данные")
        self._passport = value

    def _validate_email(self, email: str) -> bool:
        """Валидация email адреса"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validate_phone(self, phone: str) -> bool:
        """Валидация номера телефона"""
        pattern = r"^\+?[1-9]\d{1,14}$"
        return re.match(pattern, phone) is not None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "passport": self.passport,
            "created_at": self.created_at.isoformat(),
        }

    def validate(self) -> bool:
        return (
            bool(self.name)
            and self._validate_email(self.email)
            and self._validate_phone(self.phone)
            and bool(self.passport)
        )

    def __getitem__(self, key: str):
        """Доступ к атрибутам через квадратные скобки"""
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"Атрибут {key} не найден")

    def __contains__(self, item: str) -> bool:
        """Проверка наличия подстроки в данных гостя"""
        search_text = f"{self.name} {self.email} {self.phone} {self.passport}".lower()
        return item.lower() in search_text
