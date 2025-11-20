import pytest
from datetime import datetime, timedelta
from hotel_management.reservation import Reservation


class TestReservation:
    def test_reservation_creation(self):
        check_in = datetime.now() + timedelta(days=1)
        check_out = check_in + timedelta(days=3)
        reservation = Reservation(1, 1, 1, check_in, check_out, 2)
        assert reservation.guest_id == 1
        assert reservation.room_id == 1
        assert reservation.num_guests == 2

    def test_calculate_stay_cost(self):
        check_in = datetime.now() + timedelta(days=1)
        check_out = check_in + timedelta(days=5)
        reservation = Reservation(1, 1, 1, check_in, check_out, 2)
        cost = reservation.calculate_stay_cost(100.0)
        assert cost == 500.0  # 5 ночей * 100

    def test_booking_deposit(self):
        check_in = datetime.now() + timedelta(days=1)
        check_out = check_in + timedelta(days=3)
        reservation = Reservation(1, 1, 1, check_in, check_out, 2)
        deposit = reservation.calculate_booking_deposit(100.0)
        assert deposit == 20.0  # 20% от 100
