import pytest
from hotel_management.guest import Guest


class TestGuest:
    def test_guest_creation(self):
        guest = Guest(1, "John Doe", "john@example.com", "+1234567890", "AB123456")
        assert guest.name == "John Doe"
        assert guest.email == "john@example.com"
        assert guest.phone == "+1234567890"
        assert guest.passport == "AB123456"

    def test_guest_validation(self):
        guest = Guest(1, "John Doe", "john@example.com", "+1234567890", "AB123456")
        assert guest.validate() == True
