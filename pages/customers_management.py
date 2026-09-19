import customtkinter as ctk
import sqlite3
from tkinter import messagebox

from database import get_connection


class CustomersManagement(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.selected_customer_id = None

        self.build_ui()
        self.load_customers()

    # =====================================================
    # MAIN UI
    # =====================================================

    def build_ui(self):

        # HEADER
        header = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            height=85
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title_box = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_box.pack(
            side="left",
            padx=25
        )

        ctk.CTkLabel(
            title_box,
            text="👥  Customers Management",
            font=("Arial", 23, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_box,
            text="Manage café customers and their account information",
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(
            anchor="w"
        )

        ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=100,
            height=38,
            fg_color="#70452D",
            hover_color="#553222",
            corner_radius=9,
            command=self.load_customers
        ).pack(
            side="right",
            padx=25
        )

        # =================================================
        # CONTENT
        # =================================================

        content = ctk.CTkFrame(
            self,
            fg_color="#F6F1E9"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # =================================================
        # STAT CARDS
        # =================================================

        stats = ctk.CTkFrame(
            content,
            fg_color="transparent",
            height=110
        )

        stats.pack(
            fill="x",
            pady=(0, 15)
        )

        stats.pack_propagate(False)

        self.total_card = self.create_stat_card(
            stats,
            "Total Customers",
            "0",
            "👥"
        )

        self.order_card = self.create_stat_card(
            stats,
            "Customers With Orders",
            "0",
            "🛍"
        )

        self.active_card = self.create_stat_card(
            stats,
            "Active Customers",
            "0",
            "✓"
        )

        # =================================================
        # SEARCH
        # =================================================

        search_frame = ctk.CTkFrame(
            content,
            fg_color="#FFFFFF",
            corner_radius=12,
            height=65
        )

        search_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        search_frame.pack_propagate(False)

        ctk.CTkLabel(
            search_frame,
            text="🔎",
            font=("Arial", 20),
            text_color="#70452D"
        ).pack(
            side="left",
            padx=(18, 5)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by customer name or email...",
            height=38,
            font=("Arial", 11),
            fg_color="#F8F3EE",
            border_width=0,
            text_color="#302017"
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.load_customers()
        )

        ctk.CTkButton(
            search_frame,
            text="Clear",
            width=75,
            height=34,
            fg_color="#E9DED2",
            hover_color="#DCCABD",
            text_color="#4A2B1E",
            command=self.clear_search
        ).pack(
            side="right",
            padx=15
        )

        # =================================================
        # CUSTOMER TABLE AREA
        # =================================================

        table_card = ctk.CTkFrame(
            content,
            fg_color="#FFFFFF",
            corner_radius=14
        )

        table_card.pack(
            fill="both",
            expand=True
        )

        # TABLE HEADER

        table_header = ctk.CTkFrame(
            table_card,
            fg_color="#F4EEE7",
            height=50,
            corner_radius=10
        )

        table_header.pack(
            fill="x",
            padx=12,
            pady=(12, 0)
        )

        table_header.pack_propagate(False)

        headers = [
            ("ID", 60),
            ("Customer", 190),
            ("Email", 250),
            ("Orders", 90),
            ("Joined", 150),
            ("Action", 120)
        ]

        for text, width in headers:

            ctk.CTkLabel(
                table_header,
                text=text,
                width=width,
                anchor="w",
                font=("Arial", 11, "bold"),
                text_color="#604331"
            ).pack(
                side="left",
                padx=5
            )

        # CUSTOMER LIST

        self.customer_list = ctk.CTkFrame(
            table_card,
            fg_color="transparent"
        )

        self.customer_list.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

    # =====================================================
    # STAT CARD
    # =====================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        icon
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=14
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        icon_box = ctk.CTkFrame(
            card,
            width=50,
            height=50,
            fg_color="#F3E5D7",
            corner_radius=12
        )

        icon_box.pack(
            side="left",
            padx=15,
            pady=15
        )

        icon_box.pack_propagate(False)

        ctk.CTkLabel(
            icon_box,
            text=icon,
            font=("Arial", 22)
        ).pack(
            expand=True
        )

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            pady=15
        )

        ctk.CTkLabel(
            info,
            text=title,
            font=("Arial", 10),
            text_color="#897A70"
        ).pack(
            anchor="w"
        )

        value_label = ctk.CTkLabel(
            info,
            text=value,
            font=("Arial", 21, "bold"),
            text_color="#302017"
        )

        value_label.pack(
            anchor="w"
        )

        return value_label

    # =====================================================
    # LOAD CUSTOMERS
    # =====================================================

    def load_customers(self):

        for widget in self.customer_list.winfo_children():
            widget.destroy()

        search = self.search_entry.get().strip()

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                u.id,
                u.name,
                u.email,
                u.created_at,
                COUNT(o.id) AS order_count
            FROM users u
            LEFT JOIN orders o
                ON u.id = o.user_id
            WHERE u.role = 'Customer'
        """

        params = []

        if search:

            query += """
                AND (
                    LOWER(u.name) LIKE ?
                    OR LOWER(u.email) LIKE ?
                )
            """

            keyword = f"%{search.lower()}%"

            params.extend([
                keyword,
                keyword
            ])

        query += """
            GROUP BY
                u.id
            ORDER BY
                u.id DESC
        """

        cursor.execute(
            query,
            params
        )

        customers = cursor.fetchall()

        # TOTAL CUSTOMERS

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role = 'Customer'
        """)

        total_customers = cursor.fetchone()[0] or 0

        # CUSTOMERS WITH ORDERS

        cursor.execute("""
            SELECT COUNT(DISTINCT user_id)
            FROM orders
            WHERE user_id IN (
                SELECT id
                FROM users
                WHERE role = 'Customer'
            )
        """)

        customers_with_orders = cursor.fetchone()[0] or 0

        connection.close()

        self.total_card.configure(
            text=str(total_customers)
        )

        self.order_card.configure(
            text=str(customers_with_orders)
        )

        self.active_card.configure(
            text=str(total_customers)
        )

        if not customers:

            empty = ctk.CTkFrame(
                self.customer_list,
                fg_color="#FBF8F3",
                corner_radius=12
            )

            empty.pack(
                fill="x",
                pady=30
            )

            ctk.CTkLabel(
                empty,
                text="👥",
                font=("Arial", 35)
            ).pack(
                pady=(25, 5)
            )

            ctk.CTkLabel(
                empty,
                text="No customers found",
                font=("Arial", 15, "bold"),
                text_color="#4A362B"
            ).pack()

            ctk.CTkLabel(
                empty,
                text="Try another search.",
                font=("Arial", 11),
                text_color="#897A70"
            ).pack(
                pady=(3, 25)
            )

            return

        # CUSTOMER ROWS

        for customer in customers:

            customer_id = customer[0]
            name = customer[1]
            email = customer[2]
            created_at = customer[3]
            order_count = customer[4] or 0

            row = ctk.CTkFrame(
                self.customer_list,
                fg_color="#FBF8F3",
                corner_radius=10,
                height=58
            )

            row.pack(
                fill="x",
                pady=4
            )

            row.pack_propagate(False)

            # ID

            ctk.CTkLabel(
                row,
                text=f"#{customer_id}",
                width=60,
                anchor="w",
                font=("Arial", 10, "bold"),
                text_color="#70452D"
            ).pack(
                side="left",
                padx=5
            )

            # NAME

            name_box = ctk.CTkFrame(
                row,
                width=190,
                fg_color="transparent"
            )

            name_box.pack(
                side="left"
            )

            name_box.pack_propagate(False)

            ctk.CTkLabel(
                name_box,
                text=f"👤  {name}",
                anchor="w",
                font=("Arial", 11, "bold"),
                text_color="#3D2A20"
            ).pack(
                fill="both",
                expand=True
            )

            # EMAIL

            ctk.CTkLabel(
                row,
                text=email,
                width=250,
                anchor="w",
                font=("Arial", 10),
                text_color="#6F625A"
            ).pack(
                side="left",
                padx=5
            )

            # ORDERS

            ctk.CTkLabel(
                row,
                text=str(order_count),
                width=90,
                anchor="w",
                font=("Arial", 11, "bold"),
                text_color="#604331"
            ).pack(
                side="left",
                padx=5
            )

            # JOINED

            joined = str(created_at or "")

            if len(joined) > 10:
                joined = joined[:10]

            ctk.CTkLabel(
                row,
                text=joined,
                width=150,
                anchor="w",
                font=("Arial", 10),
                text_color="#6F625A"
            ).pack(
                side="left",
                padx=5
            )

            # VIEW

            ctk.CTkButton(
                row,
                text="View",
                width=80,
                height=32,
                fg_color="#70452D",
                hover_color="#553222",
                corner_radius=8,
                command=lambda cid=customer_id:
                    self.view_customer(cid)
            ).pack(
                side="right",
                padx=10
            )

    # =====================================================
    # VIEW CUSTOMER
    # =====================================================

    def view_customer(self, customer_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                created_at
            FROM users
            WHERE id = ?
            AND role = 'Customer'
        """, (customer_id,))

        customer = cursor.fetchone()

        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(total), 0)
            FROM orders
            WHERE user_id = ?
        """, (customer_id,))

        order_info = cursor.fetchone()

        cursor.execute("""
            SELECT
                COUNT(*)
            FROM reservations
            WHERE user_id = ?
        """, (customer_id,))

        reservation_count = cursor.fetchone()[0] or 0

        connection.close()

        if not customer:
            messagebox.showerror(
                "Customer",
                "Customer not found."
            )
            return

        order_count = order_info[0] or 0
        total_spent = float(order_info[1] or 0)

        window = ctk.CTkToplevel(self)

        window.title(
            "Customer Details - Brew & Bytes"
        )

        window.geometry(
            "520x570"
        )

        window.resizable(
            False,
            False
        )

        window.transient(
            self.winfo_toplevel()
        )

        window.grab_set()

        # HEADER

        header = ctk.CTkFrame(
            window,
            height=100,
            fg_color="#2F1B12",
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="👤",
            font=("Arial", 35),
            text_color="#F3B562"
        ).pack(
            side="left",
            padx=25
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
            text=customer[1],
            font=("Arial", 19, "bold"),
            text_color="white"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_box,
            text="Customer Profile",
            font=("Arial", 10),
            text_color="#CDBEB3"
        ).pack(
            anchor="w"
        )

        # DETAILS

        body = ctk.CTkFrame(
            window,
            fg_color="#F6F1E9"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.detail_row(
            body,
            "Customer ID",
            f"#{customer[0]}"
        )

        self.detail_row(
            body,
            "Full Name",
            customer[1]
        )

        self.detail_row(
            body,
            "Email",
            customer[2]
        )

        self.detail_row(
            body,
            "Joined",
            str(customer[3] or "")[:10]
        )

        self.detail_row(
            body,
            "Total Orders",
            str(order_count)
        )

        self.detail_row(
            body,
            "Total Spent",
            f"₹{total_spent:,.2f}"
        )

        self.detail_row(
            body,
            "Reservations",
            str(reservation_count)
        )

        ctk.CTkButton(
            body,
            text="Close",
            height=40,
            fg_color="#70452D",
            hover_color="#553222",
            corner_radius=9,
            command=window.destroy
        ).pack(
            fill="x",
            pady=(20, 0)
        )

    # =====================================================
    # DETAIL ROW
    # =====================================================

    def detail_row(
        self,
        parent,
        label,
        value
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=9,
            height=48
        )

        row.pack(
            fill="x",
            pady=4
        )

        row.pack_propagate(False)

        ctk.CTkLabel(
            row,
            text=label,
            width=130,
            anchor="w",
            font=("Arial", 10, "bold"),
            text_color="#897A70"
        ).pack(
            side="left",
            padx=15
        )

        ctk.CTkLabel(
            row,
            text=value,
            anchor="w",
            font=("Arial", 11, "bold"),
            text_color="#3D2A20"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

    # =====================================================
    # CLEAR SEARCH
    # =====================================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.load_customers()