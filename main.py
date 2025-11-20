import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3
from hotel_management.room import Room
from hotel_management.guest import Guest
from hotel_management.reservation import Reservation
from hotel_management.database import DatabaseManager
from openpyxl import Workbook


class HotelManagementApp:
    """Главное приложение для управления отелем"""

    def __init__(self, root):
        self.root = root
        self.root.title("Система управления отелем")
        self.root.geometry("800x600")

        self.db = DatabaseManager()
        self.rooms = []
        self.guests = []
        self.reservations = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Создание вкладок
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Вкладка управления номерами
        rooms_frame = ttk.Frame(notebook)
        notebook.add(rooms_frame, text="Номера")
        self.create_rooms_tab(rooms_frame)

        # Вкладка управления гостями
        guests_frame = ttk.Frame(notebook)
        notebook.add(guests_frame, text="Гости")
        self.create_guests_tab(guests_frame)

        # Вкладка бронирования
        reservations_frame = ttk.Frame(notebook)
        notebook.add(reservations_frame, text="Бронирования")
        self.create_reservations_tab(reservations_frame)

        # Вкладка отчетов
        reports_frame = ttk.Frame(notebook)
        notebook.add(reports_frame, text="Отчеты")
        self.create_reports_tab(reports_frame)

    def create_rooms_tab(self, parent):
        """Создание вкладки для управления номерами"""
        # Форма добавления номера
        form_frame = ttk.LabelFrame(parent, text="Добавить номер")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Номер:").grid(row=0, column=0, padx=5, pady=5)
        self.room_number = ttk.Entry(form_frame)
        self.room_number.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Тип:").grid(row=1, column=0, padx=5, pady=5)
        self.room_type = ttk.Combobox(form_frame, values=Room.ROOM_TYPES)
        self.room_type.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Цена за ночь:").grid(
            row=2, column=0, padx=5, pady=5
        )
        self.room_price = ttk.Entry(form_frame)
        self.room_price.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Вместимость:").grid(row=3, column=0, padx=5, pady=5)
        self.room_capacity = ttk.Entry(form_frame)
        self.room_capacity.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Добавить номер", command=self.add_room).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # Список номеров
        list_frame = ttk.LabelFrame(parent, text="Список номеров")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("ID", "Номер", "Тип", "Цена", "Вместимость", "Доступен")
        self.rooms_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        for col in columns:
            self.rooms_tree.heading(col, text=col)
            self.rooms_tree.column(col, width=100)

        self.rooms_tree.pack(fill="both", expand=True)

    def create_guests_tab(self, parent):
        """Создание вкладки для управления гостями"""
        # Форма добавления гостя
        form_frame = ttk.LabelFrame(parent, text="Добавить гостя")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.guest_name = ttk.Entry(form_frame)
        self.guest_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.guest_email = ttk.Entry(form_frame)
        self.guest_email.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Телефон:").grid(row=2, column=0, padx=5, pady=5)
        self.guest_phone = ttk.Entry(form_frame)
        self.guest_phone.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Паспорт:").grid(row=3, column=0, padx=5, pady=5)
        self.guest_passport = ttk.Entry(form_frame)
        self.guest_passport.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Добавить гостя", command=self.add_guest).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # Список гостей
        list_frame = ttk.LabelFrame(parent, text="Список гостей")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("ID", "Имя", "Email", "Телефон", "Паспорт")
        self.guests_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        for col in columns:
            self.guests_tree.heading(col, text=col)
            self.guests_tree.column(col, width=120)

        self.guests_tree.pack(fill="both", expand=True)

    def create_reservations_tab(self, parent):
        """Создание вкладки для бронирований"""
        # Форма бронирования
        form_frame = ttk.LabelFrame(parent, text="Создать бронирование")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Гость:").grid(row=0, column=0, padx=5, pady=5)
        self.reservation_guest = ttk.Combobox(form_frame)
        self.reservation_guest.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Номер:").grid(row=1, column=0, padx=5, pady=5)
        self.reservation_room = ttk.Combobox(form_frame)
        self.reservation_room.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Дата заезда:").grid(row=2, column=0, padx=5, pady=5)
        self.check_in_date = ttk.Entry(form_frame)
        self.check_in_date.grid(row=2, column=1, padx=5, pady=5)
        self.check_in_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(form_frame, text="Дата выезда:").grid(row=3, column=0, padx=5, pady=5)
        self.check_out_date = ttk.Entry(form_frame)
        self.check_out_date.grid(row=3, column=1, padx=5, pady=5)
        self.check_out_date.insert(
            0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        )

        ttk.Label(form_frame, text="Количество гостей:").grid(
            row=4, column=0, padx=5, pady=5
        )
        self.num_guests = ttk.Entry(form_frame)
        self.num_guests.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(
            form_frame, text="Рассчитать стоимость", command=self.calculate_cost
        ).grid(row=5, column=0, pady=10)
        ttk.Button(
            form_frame, text="Создать бронирование", command=self.add_reservation
        ).grid(row=5, column=1, pady=10)

        # Результаты расчета
        result_frame = ttk.LabelFrame(parent, text="Результаты расчета")
        result_frame.pack(fill="x", padx=5, pady=5)

        self.result_text = tk.Text(result_frame, height=4, width=80)
        self.result_text.pack(padx=5, pady=5)

    def create_reports_tab(self, parent):
        """Создание вкладки для отчетов"""
        report_frame = ttk.Frame(parent)
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(
            report_frame, text="Экспорт в Excel", command=self.export_to_excel
        ).pack(pady=5)
        ttk.Button(
            report_frame, text="Показать статистику", command=self.show_statistics
        ).pack(pady=5)

        self.report_text = tk.Text(report_frame, height=15, width=80)
        self.report_text.pack(pady=10)

    def load_data(self):
        """Загрузка данных из БД"""
        # Загрузка будет реализована после создания тестов
        pass

    def add_room(self):
        """Добавление нового номера"""
        try:
            room_id = len(self.rooms) + 1
            room = Room(
                id=room_id,
                number=int(self.room_number.get()),
                room_type=self.room_type.get(),
                price_per_night=float(self.room_price.get()),
                capacity=int(self.room_capacity.get()),
            )

            if room.validate():
                self.rooms.append(room)
                self.db.save_room(room.to_dict())
                self.update_rooms_list()
                messagebox.showinfo("Успех", "Номер успешно добавлен")
            else:
                messagebox.showerror("Ошибка", "Некорректные данные номера")

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")

    def add_guest(self):
        """Добавление нового гостя"""
        try:
            guest_id = len(self.guests) + 1
            guest = Guest(
                id=guest_id,
                name=self.guest_name.get(),
                email=self.guest_email.get(),
                phone=self.guest_phone.get(),
                passport=self.guest_passport.get(),
            )

            if guest.validate():
                self.guests.append(guest)
                self.db.save_guest(guest.to_dict())
                self.update_guests_list()
                messagebox.showinfo("Успех", "Гость успешно добавлен")
            else:
                messagebox.showerror("Ошибка", "Некорректные данные гостя")

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")

    def calculate_cost(self):
        """Расчет стоимости бронирования"""
        try:
            room_id = int(self.reservation_room.get().split(":")[0])
            room = next((r for r in self.rooms if r.id == room_id), None)

            if not room:
                messagebox.showerror("Ошибка", "Номер не найден")
                return

            check_in = datetime.strptime(self.check_in_date.get(), "%Y-%m-%d")
            check_out = datetime.strptime(self.check_out_date.get(), "%Y-%m-%d")
            num_guests = int(self.num_guests.get())

            reservation_id = len(self.reservations) + 1
            reservation = Reservation(
                id=reservation_id,
                guest_id=1,  # Временное значение
                room_id=room_id,
                check_in_date=check_in,
                check_out_date=check_out,
                num_guests=num_guests,
            )

            stay_cost = reservation.calculate_stay_cost(room.price_per_night)
            deposit = reservation.calculate_booking_deposit(room.price_per_night)
            available_beds = reservation.get_available_beds(room.capacity)

            result = f"""Результаты расчета:
Стоимость проживания: {stay_cost:.2f} руб.
Сумма бронирования (депозит): {deposit:.2f} руб.
Свободных мест в номере: {available_beds}
Продолжительность проживания: {reservation.get_stay_duration()} дней"""

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")

    def add_reservation(self):
        """Добавление нового бронирования"""
        try:
            reservation_id = len(self.reservations) + 1
            guest_id = int(self.reservation_guest.get().split(":")[0])
            room_id = int(self.reservation_room.get().split(":")[0])

            reservation = Reservation(
                id=reservation_id,
                guest_id=guest_id,
                room_id=room_id,
                check_in_date=datetime.strptime(self.check_in_date.get(), "%Y-%m-%d"),
                check_out_date=datetime.strptime(self.check_out_date.get(), "%Y-%m-%d"),
                num_guests=int(self.num_guests.get()),
            )

            room = next((r for r in self.rooms if r.id == room_id), None)
            if room:
                reservation.calculate_stay_cost(room.price_per_night)

            if reservation.validate():
                self.reservations.append(reservation)
                self.db.save_reservation(reservation.to_dict())
                messagebox.showinfo("Успех", "Бронирование успешно создано")
            else:
                messagebox.showerror("Ошибка", "Некорректные данные бронирования")

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")

    def export_to_excel(self):
        """Экспорт данных в Excel"""
        try:
            wb = Workbook()

            # Лист с номерами
            ws_rooms = wb.active
            ws_rooms.title = "Номера"
            ws_rooms.append(
                ["ID", "Номер", "Тип", "Цена за ночь", "Вместимость", "Доступен"]
            )
            for room in self.rooms:
                ws_rooms.append(
                    [
                        room.id,
                        room.number,
                        room.room_type,
                        room.price_per_night,
                        room.capacity,
                        room.is_available,
                    ]
                )

            # Лист с бронированиями
            ws_reservations = wb.create_sheet("Бронирования")
            ws_reservations.append(
                [
                    "ID",
                    "ID Гостя",
                    "ID Номера",
                    "Дата заезда",
                    "Дата выезда",
                    "Кол-во гостей",
                    "Общая стоимость",
                    "Статус",
                ]
            )
            for reservation in self.reservations:
                ws_reservations.append(
                    [
                        reservation.id,
                        reservation.guest_id,
                        reservation.room_id,
                        reservation.check_in_date.strftime("%Y-%m-%d"),
                        reservation.check_out_date.strftime("%Y-%m-%d"),
                        reservation.num_guests,
                        reservation.total_cost,
                        reservation.status,
                    ]
                )

            wb.save("hotel_report.xlsx")
            messagebox.showinfo("Успех", "Данные экспортированы в hotel_report.xlsx")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте: {e}")

    def show_statistics(self):
        """Показать статистику"""
        total_rooms = len(self.rooms)
        available_rooms = len([r for r in self.rooms if r.is_available])
        total_guests = len(self.guests)
        active_reservations = len(
            [r for r in self.reservations if r.status == "active"]
        )

        total_revenue = sum(r.total_cost for r in self.reservations)

        stats = f"""Статистика отеля:
Всего номеров: {total_rooms}
Доступных номеров: {available_rooms}
Всего гостей: {total_guests}
Активных бронирований: {active_reservations}
Общий доход: {total_revenue:.2f} руб."""

        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, stats)

    def update_rooms_list(self):
        """Обновление списка номеров"""
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)

        for room in self.rooms:
            self.rooms_tree.insert(
                "",
                "end",
                values=(
                    room.id,
                    room.number,
                    room.room_type,
                    room.price_per_night,
                    room.capacity,
                    "Да" if room.is_available else "Нет",
                ),
            )

    def update_guests_list(self):
        """Обновление списка гостей"""
        for item in self.guests_tree.get_children():
            self.guests_tree.delete(item)

        for guest in self.guests:
            self.guests_tree.insert(
                "",
                "end",
                values=(guest.id, guest.name, guest.email, guest.phone, guest.passport),
            )


def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
