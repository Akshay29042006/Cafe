import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import calendar
from datetime import datetime, date


DATABASE_NAME = "cafe.db"


class TableBooking(ctk.CTkFrame):

    def __init__(self, parent, user_id=2):
        super().__init__(parent, fg_color="#F6F1E9")

        self.user_id = user_id
        self.selected_table = None

        today = datetime.now()
        self.calendar_year = today.year
        self.calendar_month = today.month

        self.create_header()
        self.create_booking_area()
        self.load_tables()

    # =====================================================
    # DATABASE
    # =====================================================

    def get_connection(self):
        return sqlite3.connect(DATABASE_NAME)

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 15))

        ctk.CTkLabel(
            header,
            text="▦  Book a Table",
            font=("Arial", 30, "bold"),
            text_color="#302017"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Reserve your favourite table at Brew & Bytes Café",
            font=("Arial", 13),
            text_color="#8A7B70"
        ).pack(anchor="w", pady=(4, 0))

    # =====================================================
    # MAIN BOOKING AREA
    # =====================================================

    def create_booking_area(self):
        # Fixed height makes the complete reservation panel visible.
        main = ctk.CTkFrame(
            self,
            height=555,
            fg_color="transparent"
        )
        main.pack(fill="x", padx=30, pady=10)
        main.pack_propagate(False)

        # -------------------------------------------------
        # LEFT
        # -------------------------------------------------

        left = ctk.CTkFrame(
            main,
            fg_color="#FFFFFF",
            corner_radius=18
        )
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkLabel(
            left,
            text="Available Tables",
            font=("Arial", 20, "bold"),
            text_color="#302017"
        ).pack(anchor="w", padx=22, pady=(20, 3))

        ctk.CTkLabel(
            left,
            text="Select a table for your reservation",
            font=("Arial", 11),
            text_color="#8A7B70"
        ).pack(anchor="w", padx=22, pady=(0, 15))

        self.table_scroll = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent"
        )
        self.table_scroll.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # -------------------------------------------------
        # RIGHT
        # -------------------------------------------------

        right = ctk.CTkFrame(
            main,
            width=370,
            height=555,
            fg_color="#FFFFFF",
            corner_radius=18
        )
        right.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )
        right.pack_propagate(False)

        ctk.CTkLabel(
            right,
            text="Reservation Details",
            font=("Arial", 20, "bold"),
            text_color="#302017"
        ).pack(anchor="w", padx=25, pady=(20, 14))

        ctk.CTkLabel(
            right,
            text="Selected Table",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(anchor="w", padx=25)

        self.selected_label = ctk.CTkLabel(
            right,
            text="No table selected",
            height=40,
            corner_radius=10,
            fg_color="#F5EEE6",
            text_color="#8A7B70",
            font=("Arial", 12, "bold")
        )
        self.selected_label.pack(fill="x", padx=25, pady=(5, 12))

        # DATE
        ctk.CTkLabel(
            right,
            text="Reservation Date",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(anchor="w", padx=25)

        date_box = ctk.CTkFrame(right, fg_color="transparent")
        date_box.pack(fill="x", padx=25, pady=(5, 12))

        self.date_entry = ctk.CTkEntry(
            date_box,
            height=40,
            corner_radius=10,
            placeholder_text="Select date",
            border_color="#D9C9BC"
        )
        self.date_entry.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            date_box,
            text="📅",
            width=45,
            height=40,
            corner_radius=10,
            fg_color="#70452D",
            hover_color="#5A3623",
            command=self.open_calendar
        ).pack(side="right", padx=(6, 0))

        self.date_entry.bind(
            "<Button-1>",
            lambda event: self.open_calendar()
        )

        # TIME
        ctk.CTkLabel(
            right,
            text="Reservation Time",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(anchor="w", padx=25)

        self.time_combo = ctk.CTkComboBox(
            right,
            height=40,
            corner_radius=10,
            values=[
                "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
                "12:00 PM", "12:30 PM", "01:00 PM", "01:30 PM",
                "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
                "04:00 PM", "04:30 PM", "05:00 PM", "05:30 PM",
                "06:00 PM", "06:30 PM", "07:00 PM", "07:30 PM",
                "08:00 PM", "08:30 PM", "09:00 PM", "09:30 PM",
                "10:00 PM"
            ]
        )
        self.time_combo.pack(fill="x", padx=25, pady=(5, 12))
        self.time_combo.set("07:30 PM")

        # GUESTS
        ctk.CTkLabel(
            right,
            text="Number of Guests",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(anchor="w", padx=25)

        self.guests_combo = ctk.CTkComboBox(
            right,
            height=40,
            corner_radius=10,
            values=["1", "2", "3", "4"]
        )
        self.guests_combo.pack(fill="x", padx=25, pady=(5, 14))
        self.guests_combo.set("2")

        # SAVE - kept near the bottom but inside fixed panel
        self.save_button = ctk.CTkButton(
            right,
            text="✓  SAVE BOOKING",
            height=48,
            corner_radius=11,
            font=("Arial", 13, "bold"),
            fg_color="#70452D",
            hover_color="#5A3623",
            command=self.confirm_booking
        )
        self.save_button.pack(fill="x", padx=25, pady=(0, 9))

        ctk.CTkButton(
            right,
            text="Clear",
            height=34,
            corner_radius=9,
            font=("Arial", 10),
            fg_color="#EFE5DB",
            hover_color="#E2D5C8",
            text_color="#3B2417",
            command=self.clear_form
        ).pack(fill="x", padx=25)

        ctk.CTkLabel(
            right,
            text="☕ Enjoy your time at Brew & Bytes!",
            font=("Arial", 10),
            text_color="#9A8B80"
        ).pack(pady=10)

    # =====================================================
    # CALENDAR
    # =====================================================

    def open_calendar(self):
        self.calendar_popup = ctk.CTkToplevel(self)
        self.calendar_popup.title("Select Reservation Date")
        self.calendar_popup.geometry("360x410")
        self.calendar_popup.resizable(False, False)
        self.calendar_popup.transient(self.winfo_toplevel())
        self.calendar_popup.grab_set()
        self.create_calendar()

    def create_calendar(self):
        for widget in self.calendar_popup.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(
            self.calendar_popup,
            fg_color="#2F1B12",
            corner_radius=0
        )
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="📅  Select Date",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(pady=14)

        nav = ctk.CTkFrame(
            self.calendar_popup,
            fg_color="transparent"
        )
        nav.pack(fill="x", padx=15, pady=12)

        ctk.CTkButton(
            nav,
            text="‹",
            width=40,
            height=34,
            fg_color="#EFE5DB",
            hover_color="#E2D5C8",
            text_color="#3B2417",
            command=self.previous_month
        ).pack(side="left")

        ctk.CTkLabel(
            nav,
            text=f"{calendar.month_name[self.calendar_month]} {self.calendar_year}",
            font=("Arial", 15, "bold"),
            text_color="#302017"
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            nav,
            text="›",
            width=40,
            height=34,
            fg_color="#EFE5DB",
            hover_color="#E2D5C8",
            text_color="#3B2417",
            command=self.next_month
        ).pack(side="right")

        weekdays = ctk.CTkFrame(
            self.calendar_popup,
            fg_color="#F5EEE6"
        )
        weekdays.pack(fill="x", padx=15)

        for index, day_name in enumerate(
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ):
            ctk.CTkLabel(
                weekdays,
                text=day_name,
                font=("Arial", 9, "bold"),
                text_color="#70452D"
            ).grid(
                row=0,
                column=index,
                padx=2,
                pady=7,
                sticky="nsew"
            )
            weekdays.grid_columnconfigure(index, weight=1)

        calendar_frame = ctk.CTkFrame(
            self.calendar_popup,
            fg_color="transparent"
        )
        calendar_frame.pack(fill="both", expand=True, padx=15, pady=5)

        for row_index, week in enumerate(
            calendar.monthcalendar(
                self.calendar_year,
                self.calendar_month
            )
        ):
            for col_index, day in enumerate(week):
                if day == 0:
                    continue

                # Disable dates before today
                selected = date(
                    self.calendar_year,
                    self.calendar_month,
                    day
                )
                today = date.today()

                button_state = (
                    "normal"
                    if selected >= today
                    else "disabled"
                )

                ctk.CTkButton(
                    calendar_frame,
                    text=str(day),
                    width=38,
                    height=30,
                    corner_radius=8,
                    fg_color="#FFFFFF",
                    hover_color="#E9D6BD",
                    text_color="#302017",
                    font=("Arial", 10),
                    state=button_state,
                    command=lambda d=day: self.select_date(d)
                ).grid(
                    row=row_index,
                    column=col_index,
                    padx=3,
                    pady=3
                )

        ctk.CTkButton(
            self.calendar_popup,
            text="Cancel",
            width=100,
            height=32,
            corner_radius=8,
            fg_color="#E9DED2",
            hover_color="#DCCCBD",
            text_color="#3B2417",
            command=self.calendar_popup.destroy
        ).pack(pady=(2, 12))

    def select_date(self, day):
        selected_date = (
            f"{self.calendar_year:04d}-"
            f"{self.calendar_month:02d}-"
            f"{day:02d}"
        )

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, selected_date)
        self.calendar_popup.destroy()

    def previous_month(self):
        self.calendar_month -= 1
        if self.calendar_month < 1:
            self.calendar_month = 12
            self.calendar_year -= 1
        self.create_calendar()

    def next_month(self):
        self.calendar_month += 1
        if self.calendar_month > 12:
            self.calendar_month = 1
            self.calendar_year += 1
        self.create_calendar()

    # =====================================================
    # TABLES
    # =====================================================

    def load_tables(self):
        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT id, table_number, seats, status
                FROM cafe_tables
                ORDER BY table_number
            """)
            tables = cursor.fetchall()
        finally:
            connection.close()

        if not tables:
            ctk.CTkLabel(
                self.table_scroll,
                text="No tables available.",
                font=("Arial", 13),
                text_color="#8A7B70"
            ).pack(pady=50)
            return

        for table in tables:
            self.create_table_card(table)

    def create_table_card(self, table):
        table_id, table_number, seats, status = table
        available = status == "Available"

        card = ctk.CTkFrame(
            self.table_scroll,
            height=100,
            corner_radius=14,
            fg_color="#FFFFFF" if available else "#F3EFEB",
            border_width=1,
            border_color="#E6DCD2"
        )
        card.pack(fill="x", pady=6)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="▦",
            font=("Arial", 30),
            text_color="#70452D" if available else "#A59A92"
        ).pack(side="left", padx=(18, 12))

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        info.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            info,
            text=f"Table {table_number}",
            font=("Arial", 14, "bold"),
            text_color="#302017"
        ).pack(anchor="w", pady=(18, 2))

        ctk.CTkLabel(
            info,
            text=f"{seats} Seats",
            font=("Arial", 10),
            text_color="#8A7B70"
        ).pack(anchor="w")

        ctk.CTkLabel(
            card,
            text="AVAILABLE" if available else status.upper(),
            font=("Arial", 9, "bold"),
            text_color="#3E8A5A" if available else "#A83D2C"
        ).pack(side="right", padx=10)

        ctk.CTkButton(
            card,
            text="Select",
            width=75,
            height=32,
            corner_radius=8,
            font=("Arial", 10, "bold"),
            fg_color="#70452D" if available else "#D5CCC5",
            hover_color="#5A3623" if available else "#D5CCC5",
            text_color="white" if available else "#8A7B70",
            state="normal" if available else "disabled",
            command=lambda tid=table_id, tn=table_number, s=seats:
                self.select_table(tid, tn, s)
        ).pack(side="right", padx=15)

    def select_table(self, table_id, table_number, seats):
        self.selected_table = {
            "id": table_id,
            "number": table_number,
            "seats": seats
        }

        self.selected_label.configure(
            text=f"Table {table_number}  •  {seats} Seats",
            fg_color="#E9D6BD",
            text_color="#70452D"
        )

    # =====================================================
    # SAVE BOOKING TO SQLITE
    # =====================================================

    def confirm_booking(self):
        if self.selected_table is None:
            messagebox.showwarning(
                "Select Table",
                "Please select a table first."
            )
            return

        reservation_date = self.date_entry.get().strip()
        reservation_time = self.time_combo.get().strip()
        guests_text = self.guests_combo.get().strip()

        if not reservation_date:
            messagebox.showwarning(
                "Select Date",
                "Please select a reservation date."
            )
            return

        try:
            selected_date = datetime.strptime(
                reservation_date,
                "%Y-%m-%d"
            ).date()

            if selected_date < date.today():
                messagebox.showwarning(
                    "Invalid Date",
                    "Please select today or a future date."
                )
                return
        except ValueError:
            messagebox.showwarning(
                "Invalid Date",
                "Date format must be YYYY-MM-DD."
            )
            return

        try:
            guests = int(guests_text)
        except ValueError:
            messagebox.showwarning(
                "Invalid Guests",
                "Please select a valid number of guests."
            )
            return

        if guests > self.selected_table["seats"]:
            messagebox.showwarning(
                "Too Many Guests",
                f"Table {self.selected_table['number']} has only "
                f"{self.selected_table['seats']} seats."
            )
            return

        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            # Check table status
            cursor.execute("""
                SELECT status
                FROM cafe_tables
                WHERE id = ?
            """, (self.selected_table["id"],))

            result = cursor.fetchone()

            if not result:
                raise Exception("Selected table was not found.")

            if result[0] != "Available":
                messagebox.showwarning(
                    "Table Unavailable",
                    "This table is no longer available."
                )
                connection.close()
                self.load_tables()
                return

            # Check whether this table already has a reservation
            # for the same date/time.
            cursor.execute("""
                SELECT id
                FROM reservations
                WHERE table_id = ?
                  AND reservation_date = ?
                  AND reservation_time = ?
                  AND status != 'Cancelled'
            """, (
                self.selected_table["id"],
                reservation_date,
                reservation_time
            ))

            if cursor.fetchone():
                messagebox.showwarning(
                    "Already Booked",
                    "This table is already booked for that date and time."
                )
                connection.close()
                return

            # Save reservation
            cursor.execute("""
                INSERT INTO reservations
                (
                    user_id,
                    table_id,
                    reservation_date,
                    reservation_time,
                    guests,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.user_id,
                self.selected_table["id"],
                reservation_date,
                reservation_time,
                guests,
                "Reserved"
            ))

            # Keep table status synchronized.
            cursor.execute("""
                UPDATE cafe_tables
                SET status = 'Reserved'
                WHERE id = ?
            """, (self.selected_table["id"],))

            connection.commit()
            reservation_id = cursor.lastrowid
            connection.close()

            messagebox.showinfo(
                "Booking Saved ✓",
                "Your table booking has been saved successfully!\n\n"
                f"Reservation ID: #{reservation_id}\n"
                f"Table: {self.selected_table['number']}\n"
                f"Date: {reservation_date}\n"
                f"Time: {reservation_time}\n"
                f"Guests: {guests}"
            )

            self.clear_form()
            self.load_tables()

        except Exception as error:
            connection.rollback()
            connection.close()

            messagebox.showerror(
                "Booking Error",
                f"Could not save booking.\n\n{error}"
            )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_form(self):
        self.selected_table = None

        self.selected_label.configure(
            text="No table selected",
            fg_color="#F5EEE6",
            text_color="#8A7B70"
        )

        self.date_entry.delete(0, "end")
        self.time_combo.set("07:30 PM")
        self.guests_combo.set("2")
