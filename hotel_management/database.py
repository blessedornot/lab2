import sqlite3
from datetime import datetime
from typing import List, Optional


class DatabaseManager:
    """Менеджер базы данных для сохранения результатов"""

    def __init__(self, db_path: str = "hotel.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Инициализация базы данных и создание таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Таблица комнат
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY,
                    number INTEGER UNIQUE NOT NULL,
                    room_type TEXT NOT NULL,
                    price_per_night REAL NOT NULL,
                    capacity INTEGER NOT NULL,
                    is_available BOOLEAN NOT NULL,
                    created_at TEXT NOT NULL
                )
            """
            )

            # Таблица гостей
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS guests (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT NOT NULL,
                    passport TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL
                )
            """
            )

            # Таблица бронирований
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY,
                    guest_id INTEGER NOT NULL,
                    room_id INTEGER NOT NULL,
                    check_in_date TEXT NOT NULL,
                    check_out_date TEXT NOT NULL,
                    num_guests INTEGER NOT NULL,
                    total_cost REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (guest_id) REFERENCES guests (id),
                    FOREIGN KEY (room_id) REFERENCES rooms (id)
                )
            """
            )

            conn.commit()

    def save_room(self, room_data: dict) -> int:
        """Сохранение комнаты в БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO rooms 
                (id, number, room_type, price_per_night, capacity, is_available, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    room_data["id"],
                    room_data["number"],
                    room_data["room_type"],
                    room_data["price_per_night"],
                    room_data["capacity"],
                    room_data["is_available"],
                    room_data["created_at"],
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def save_guest(self, guest_data: dict) -> int:
        """Сохранение гостя в БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO guests 
                (id, name, email, phone, passport, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    guest_data["id"],
                    guest_data["name"],
                    guest_data["email"],
                    guest_data["phone"],
                    guest_data["passport"],
                    guest_data["created_at"],
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def save_reservation(self, reservation_data: dict) -> int:
        """Сохранение бронирования в БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO reservations 
                (id, guest_id, room_id, check_in_date, check_out_date, 
                 num_guests, total_cost, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    reservation_data["id"],
                    reservation_data["guest_id"],
                    reservation_data["room_id"],
                    reservation_data["check_in_date"],
                    reservation_data["check_out_date"],
                    reservation_data["num_guests"],
                    reservation_data["total_cost"],
                    reservation_data["status"],
                    reservation_data["created_at"],
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_rooms(self) -> List[dict]:
        """Получение всех комнат из БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_all_reservations(self) -> List[dict]:
        """Получение всех бронирований из БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reservations")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
