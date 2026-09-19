import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime


DATABASE_NAME = "cafe.db"


class MyReservations(ctk.CTkFrame):

    def __init__(self, parent, user_id=2):
        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.user_id = user_id

        self.create_header()
        self.create_summary()
        self.create_reservation_area()
        self.load_reservations()

    # =====================================================
    # DATABASE
    # =====================================================

    def get_connection(self):
        return sqlite3.connect(DATABASE_NAME)

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        title_box = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_box.pack(
            side="left"
        )

        ctk.CTkLabel(
            title_box,
            text="▦  My Reservations",
            font=("Arial", 30, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_box,
            text="Manage your café table bookings",
            font=("Arial", 13),
            text_color="#8A7B70"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#70452D",
            hover_color="#5A3623",
            font=("Arial", 11, "bold"),
            command=self.load_reservations
        ).pack(
            side="right"
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def create_summary(self):

        summary = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        summary.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        self.total_card = self.create_stat_card(
            summary,
            "Total Bookings",
            "0"
        )
        self.total_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 7)
        )

        self.active_card = self.create_stat_card(
            summary,
            "Active",
            "0"
        )
        self.active_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=7
        )

        self.cancelled_card = self.create_stat_card(
            summary,
            "Cancelled",
            "0"
        )
        self.cancelled_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(7, 0)
        )

    def create_stat_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            height=95,
            corner_radius=15,
            fg_color="#FFFFFF"
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            text_color="#877970"
        ).pack(
            anchor="w",
            padx=18,
            pady=(17, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 24, "bold"),
            text_color="#302017"
        )

        value_label.pack(
            anchor="w",
            padx=18
        )

        card.value_label = value_label

        return card

    # =====================================================
    # RESERVATION AREA
    # =====================================================

    def create_reservation_area(self):

        self.reservation_card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="#FFFFFF"
        )

        self.reservation_card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        header = ctk.CTkFrame(
            self.reservation_card,
            height=55,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(8, 0)
        )

        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Booking History",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            side="left"
        )

        self.count_label = ctk.CTkLabel(
            header,
            text="0 bookings",
            font=("Arial", 10),
            text_color="#877970"
        )

        self.count_label.pack(
            side="right"
        )

        # Fixed reservation area — no internal scrollbar
        self.reservation_scroll = ctk.CTkFrame(
            self.reservation_card,
            fg_color="transparent"
        )

        self.reservation_scroll.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

    # =====================================================
    # LOAD RESERVATIONS
    # =====================================================

    def load_reservations(self):

        for widget in self.reservation_scroll.winfo_children():
            widget.destroy()

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                r.id,
                r.table_id,
                ct.table_number,
                ct.seats,
                r.reservation_date,
                r.reservation_time,
                r.guests,
                r.status
            FROM reservations r
            JOIN cafe_tables ct
                ON r.table_id = ct.id
            WHERE r.user_id = ?
            ORDER BY
                r.id DESC
        """, (self.user_id,))

        reservations = cursor.fetchall()

        connection.close()

        total = len(reservations)
        active = sum(
            1 for item in reservations
            if item[7] not in ("Cancelled", "Completed")
        )
        cancelled = sum(
            1 for item in reservations
            if item[7] == "Cancelled"
        )

        self.total_card.value_label.configure(
            text=str(total)
        )

        self.active_card.value_label.configure(
            text=str(active)
        )

        self.cancelled_card.value_label.configure(
            text=str(cancelled)
        )

        self.count_label.configure(
            text=f"{total} bookings"
        )

        if not reservations:
            self.show_empty()
            return

        # Show latest 3 reservations on the fixed page.
        for reservation in reservations[:3]:
            self.create_reservation_card(reservation)

        if len(reservations) > 3:
            ctk.CTkLabel(
                self.reservation_scroll,
                text=f"+ {len(reservations) - 3} older reservations hidden — no internal scrolling.",
                font=("Arial", 10),
                text_color="#8A7A6E"
            ).pack(pady=(3, 0))

    # =====================================================
    # EMPTY STATE
    # =====================================================

    def show_empty(self):

        empty = ctk.CTkFrame(
            self.reservation_scroll,
            height=260,
            corner_radius=15,
            fg_color="#FBF8F3"
        )

        empty.pack(
            fill="x",
            pady=20
        )

        empty.pack_propagate(False)

        ctk.CTkLabel(
            empty,
            text="▦",
            font=("Arial", 50),
            text_color="#70452D"
        ).pack(
            pady=(40, 5)
        )

        ctk.CTkLabel(
            empty,
            text="No reservations yet",
            font=("Arial", 20, "bold"),
            text_color="#302017"
        ).pack()

        ctk.CTkLabel(
            empty,
            text="Book a table and your reservation will appear here.",
            font=("Arial", 11),
            text_color="#8A7B70"
        ).pack(
            pady=5
        )

    # =====================================================
    # RESERVATION CARD
    # =====================================================

    def create_reservation_card(self, reservation):

        reservation_id = reservation[0]
        table_number = reservation[2]
        seats = reservation[3]
        reservation_date = reservation[4]
        reservation_time = reservation[5]
        guests = reservation[6]
        status = reservation[7]

        card = ctk.CTkFrame(
            self.reservation_scroll,
            corner_radius=15,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E8DDD2"
        )

        card.pack(
            fill="x",
            pady=6
        )

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=18,
            pady=(15, 8)
        )

        ctk.CTkLabel(
            top,
            text=f"Reservation #{reservation_id}",
            font=("Arial", 17, "bold"),
            text_color="#302017"
        ).pack(
            side="left"
        )

        status_colors = {
            "Reserved": "#3E8A5A",
            "Confirmed": "#3E6FA8",
            "Completed": "#3E8A5A",
            "Cancelled": "#A83D2C"
        }

        status_color = status_colors.get(
            status,
            "#8A6A35"
        )

        ctk.CTkLabel(
            top,
            text=f"● {status}",
            font=("Arial", 11, "bold"),
            text_color=status_color
        ).pack(
            side="right"
        )

        details = ctk.CTkFrame(
            card,
            fg_color="#F9F5F0",
            corner_radius=12
        )

        details.pack(
            fill="x",
            padx=18,
            pady=(0, 12)
        )

        self.create_detail(
            details,
            "▦",
            "Table",
            f"Table {table_number} • {seats} Seats"
        )

        self.create_detail(
            details,
            "📅",
            "Date",
            self.format_date(reservation_date)
        )

        self.create_detail(
            details,
            "◷",
            "Time",
            reservation_time
        )

        self.create_detail(
            details,
            "👥",
            "Guests",
            str(guests)
        )

        bottom = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        if status not in ("Cancelled", "Completed"):

            ctk.CTkButton(
                bottom,
                text="✕  Cancel Reservation",
                width=180,
                height=36,
                corner_radius=9,
                fg_color="#FCE7E2",
                hover_color="#F3D0C9",
                text_color="#A83D2C",
                font=("Arial", 10, "bold"),
                command=lambda rid=reservation_id:
                    self.cancel_reservation(rid)
            ).pack(
                side="right"
            )

        else:

            ctk.CTkLabel(
                bottom,
                text="No actions available",
                font=("Arial", 9),
                text_color="#A09389"
            ).pack(
                side="right"
            )

    # =====================================================
    # DETAIL
    # =====================================================

    def create_detail(self, parent, icon, title, value):

        box = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        box.pack(
            side="left",
            fill="x",
            expand=True,
            padx=7,
            pady=12
        )

        ctk.CTkLabel(
            box,
            text=icon,
            font=("Arial", 18),
            text_color="#70452D"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            box,
            text=title,
            font=("Arial", 9, "bold"),
            text_color="#95867B"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        ctk.CTkLabel(
            box,
            text=value,
            font=("Arial", 10, "bold"),
            text_color="#4D3B30"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

    # =====================================================
    # CANCEL RESERVATION
    # =====================================================

    def cancel_reservation(self, reservation_id):

        answer = messagebox.askyesno(
            "Cancel Reservation",
            "Are you sure you want to cancel this reservation?"
        )

        if not answer:
            return

        connection = self.get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    table_id,
                    status
                FROM reservations
                WHERE id = ?
                AND user_id = ?
            """, (
                reservation_id,
                self.user_id
            ))

            reservation = cursor.fetchone()

            if not reservation:

                connection.close()

                messagebox.showerror(
                    "Reservation Not Found",
                    "This reservation could not be found."
                )

                return

            table_id = reservation[0]
            status = reservation[1]

            if status == "Cancelled":

                connection.close()

                messagebox.showinfo(
                    "Already Cancelled",
                    "This reservation is already cancelled."
                )

                self.load_reservations()
                return

            cursor.execute("""
                UPDATE reservations
                SET status = 'Cancelled'
                WHERE id = ?
                AND user_id = ?
            """, (
                reservation_id,
                self.user_id
            ))

            cursor.execute("""
                UPDATE cafe_tables
                SET status = 'Available'
                WHERE id = ?
            """, (
                table_id,
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Reservation Cancelled",
                "Your reservation has been cancelled successfully.\n\n"
                "The table is now available again."
            )

            self.load_reservations()

        except Exception as error:

            connection.rollback()
            connection.close()

            messagebox.showerror(
                "Cancellation Error",
                f"Unable to cancel reservation.\n\n{error}"
            )

    # =====================================================
    # FORMAT DATE
    # =====================================================

    def format_date(self, value):

        if not value:
            return "-"

        value = str(value)

        try:

            parsed = datetime.strptime(
                value,
                "%Y-%m-%d"
            )

            return parsed.strftime(
                "%d %b %Y"
            )

        except Exception:
            return value
