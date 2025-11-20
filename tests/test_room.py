import pytest
from hotel_management.room import Room


class TestRoom:
    def test_room_creation(self):
        room = Room(1, 101, "single", 100.0, 2)
        assert room.number == 101
        assert room.room_type == "single"
        assert room.price_per_night == 100.0
        assert room.capacity == 2

    def test_room_validation(self):
        room = Room(1, 101, "single", 100.0, 2)
        assert room.validate() == True

    def test_calculate_stay_cost(self):
        room = Room(1, 101, "single", 100.0, 2)
        assert room.calculate_stay_cost(5) == 500.0
