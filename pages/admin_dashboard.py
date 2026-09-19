import customtkinter as ctk
from datetime import datetime, timedelta

from pages.menu_management import MenuManagement
from pages.orders_management import OrdersManagement
from pages.inventory_management import InventoryManagement
from pages.feedback_management import FeedbackManagement
from pages.offers_management import OffersManagement
from pages.sales_reports import SalesReports
from pages.customers_management import CustomersManagement
from pages.tables_management import TablesManagement
from pages.settings_management import SettingsManagement

from database import (
    get_connection,
    get_all_orders,
    get_order_items,
    get_user_by_id
)


class AdminDashboard(ctk.CTkFrame):

    def __init__(self, parent, logout_callback):
        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.logout_callback = logout_callback

        self.create_sidebar()
        self.create_main_area()

    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=235,
            corner_radius=0,
            fg_color="#2F1B12"
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Logo
        ctk.CTkLabel(
            self.sidebar,
            text="☕",
            font=("Arial", 42),
            text_color="#F3B562"
        ).pack(
            pady=(30, 2)
        )

        ctk.CTkLabel(
            self.sidebar,
            text="BREW & BYTES",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack()

        ctk.CTkLabel(
            self.sidebar,
            text="CAFÉ MANAGEMENT",
            font=("Arial", 10, "bold"),
            text_color="#BFAFA3"
        ).pack(
            pady=(0, 30)
        )

        # Navigation
        self.create_nav_button(
            "⌂",
            "Dashboard",
            True
        )

        self.create_nav_button(
            "▣",
            "Orders",
            command=self.open_orders_management
        )

        self.create_nav_button(
            "☕",
            "Menu",
            command=self.open_menu_management
        )

        self.create_nav_button(
            "▤",
            "Inventory",
            command=self.open_inventory_management
        )

        self.create_nav_button(
            "♟",
            "Customers",
            command=self.open_customers_management
        )

        self.create_nav_button(
            "▦",
            "Tables",
            command=self.open_tables_management
        )

        self.create_nav_button(
            "↗",
            "Sales & Reports",
            command=self.open_sales_reports
        )

        self.create_nav_button(
            "★",
            "Offers",
            command=self.open_offers_management
        )

        self.create_nav_button(
            "💬",
            "Feedback",
            command=self.open_feedback_management
        )

        self.create_nav_button(
            "⚙",
            "Settings",
            command=self.open_settings_management
        )

        # Bottom profile
        bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color="#41271C",
            corner_radius=12
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            bottom,
            text="👨‍💼",
            font=("Arial", 25)
        ).pack(
            side="left",
            padx=8,
            pady=8
        )

        info = ctk.CTkFrame(
            bottom,
            fg_color="transparent"
        )

        info.pack(
            side="left"
        )

        ctk.CTkLabel(
            info,
            text="Cafe Admin",
            font=("Arial", 12, "bold"),
            text_color="white"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text="Administrator",
            font=("Arial", 9),
            text_color="#CDBEB3"
        ).pack(
            anchor="w"
        )

    # =====================================================
    # NAVIGATION BUTTON
    # =====================================================

    def create_nav_button(
        self,
        icon,
        text,
        active=False,
        command=None
    ):

        if active:
            fg = "#70452D"
        else:
            fg = "transparent"

        button = ctk.CTkButton(
            self.sidebar,
            text=f"  {icon}    {text}",
            anchor="w",
            height=43,
            font=(
                "Arial",
                13,
                "bold" if active else "normal"
            ),
            fg_color=fg,
            hover_color="#4A2B1E",
            text_color="#FFFFFF",
            corner_radius=8,
            command=command
        )

        button.pack(
            fill="x",
            padx=12,
            pady=2
        )

    # =====================================================
    # ORDERS MANAGEMENT
    # =====================================================

    def open_orders_management(self):

        orders_window = ctk.CTkToplevel(self)

        orders_window.title(
            "Orders Management - Brew & Bytes"
        )

        orders_window.geometry(
            "1200x750"
        )

        orders_window.minsize(
            1000,
            650
        )

        orders_window.transient(
            self.winfo_toplevel()
        )

        orders_window.grab_set()

        orders_page = OrdersManagement(
            orders_window
        )

        orders_page.pack(
            fill="both",
            expand=True
        )

        def close_window():

            try:
                orders_window.grab_release()
            except Exception:
                pass

            orders_window.destroy()

        orders_window.protocol(
            "WM_DELETE_WINDOW",
            close_window
        )

    # =====================================================
    # MENU MANAGEMENT
    # =====================================================

    def open_menu_management(self):

        menu_window = ctk.CTkToplevel(self)

        menu_window.title(
            "Menu Management - Brew & Bytes"
        )

        menu_window.geometry(
            "1150x720"
        )

        menu_window.minsize(
            950,
            600
        )

        menu_window.transient(
            self.winfo_toplevel()
        )

        menu_window.grab_set()

        menu_page = MenuManagement(
            menu_window,
            refresh_callback=lambda: None
        )

        menu_page.pack(
            fill="both",
            expand=True
        )

        def close_window():

            try:
                menu_window.grab_release()
            except Exception:
                pass

            menu_window.destroy()

        menu_window.protocol(
            "WM_DELETE_WINDOW",
            close_window
        )

    # =====================================================
    # INVENTORY MANAGEMENT
    # =====================================================

    def open_inventory_management(self):

        inventory_window = ctk.CTkToplevel(self)

        inventory_window.title(
            "Inventory Management - Brew & Bytes"
        )

        inventory_window.geometry(
            "1250x760"
        )

        inventory_window.minsize(
            1050,
            650
        )

        inventory_window.transient(
            self.winfo_toplevel()
        )

        inventory_window.grab_set()

        inventory_page = InventoryManagement(
            inventory_window
        )

        inventory_page.pack(
            fill="both",
            expand=True
        )

        def close_window():
            try:
                inventory_window.grab_release()
            except Exception:
                pass

            inventory_window.destroy()

        inventory_window.protocol(
            "WM_DELETE_WINDOW",
            close_window
        )

    # =====================================================
    # OFFERS MANAGEMENT
    # =====================================================

    def open_offers_management(self):

        offers_window = ctk.CTkToplevel(self)

        offers_window.title(
            "Offers Management - Brew & Bytes"
        )

        offers_window.geometry(
            "1250x800"
        )

        offers_window.minsize(
            1050,
            650
        )

        offers_window.transient(
            self.winfo_toplevel()
        )

        offers_window.grab_set()

        offers_page = OffersManagement(
            offers_window
        )

        offers_page.pack(
            fill="both",
            expand=True
        )

        def close_window():
            try:
                offers_window.grab_release()
            except Exception:
                pass

            offers_window.destroy()

        offers_window.protocol(
            "WM_DELETE_WINDOW",
            close_window
        )

    # =====================================================
    # SALES & REPORTS
    # =====================================================

    def open_sales_reports(self):

        reports_window = ctk.CTkToplevel(self)
        reports_window.title("Sales & Reports - Brew & Bytes")
        reports_window.geometry("1250x800")
        reports_window.minsize(1050, 700)
        reports_window.transient(self.winfo_toplevel())
        reports_window.grab_set()

        reports_page = SalesReports(reports_window)
        reports_page.pack(fill="both", expand=True)

        def close_window():
            try:
                reports_window.grab_release()
            except Exception:
                pass
            reports_window.destroy()

        reports_window.protocol("WM_DELETE_WINDOW", close_window)

    # =====================================================
    # FEEDBACK MANAGEMENT
    # =====================================================

    def open_feedback_management(self):

        feedback_window = ctk.CTkToplevel(self)

        feedback_window.title(
            "Feedback Management - Brew & Bytes"
        )

        feedback_window.geometry(
            "1250x780"
        )

        feedback_window.minsize(
            1050,
            650
        )

        feedback_window.transient(
            self.winfo_toplevel()
        )

        feedback_window.grab_set()

        feedback_page = FeedbackManagement(
            feedback_window
        )

        feedback_page.pack(
            fill="both",
            expand=True
        )

        def close_window():
            try:
                feedback_window.grab_release()
            except Exception:
                pass

            feedback_window.destroy()

        feedback_window.protocol(
            "WM_DELETE_WINDOW",
            close_window
        )

    # =====================================================
    # CUSTOMERS MANAGEMENT
    # =====================================================

    def open_customers_management(self):

        customers_window = ctk.CTkToplevel(self)
        customers_window.title("Customers Management - Brew & Bytes")
        customers_window.geometry("1200x760")
        customers_window.minsize(1050, 650)
        customers_window.transient(self.winfo_toplevel())
        customers_window.grab_set()

        customers_page = CustomersManagement(customers_window)
        customers_page.pack(fill="both", expand=True)

        def close_window():
            try:
                customers_window.grab_release()
            except Exception:
                pass
            customers_window.destroy()

        customers_window.protocol("WM_DELETE_WINDOW", close_window)

    # =====================================================
    # TABLES MANAGEMENT
    # =====================================================

    def open_tables_management(self):

        tables_window = ctk.CTkToplevel(self)
        tables_window.title("Tables Management - Brew & Bytes")
        tables_window.geometry("1200x760")
        tables_window.minsize(1050, 650)
        tables_window.transient(self.winfo_toplevel())
        tables_window.grab_set()

        tables_page = TablesManagement(tables_window)
        tables_page.pack(fill="both", expand=True)

        def close_window():
            try:
                tables_window.grab_release()
            except Exception:
                pass
            tables_window.destroy()

        tables_window.protocol("WM_DELETE_WINDOW", close_window)

    # =====================================================
    # SETTINGS MANAGEMENT
    # =====================================================

    def open_settings_management(self):

        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings - Brew & Bytes")
        settings_window.geometry("1150x760")
        settings_window.minsize(1000, 680)
        settings_window.transient(self.winfo_toplevel())
        settings_window.grab_set()

        settings_page = SettingsManagement(settings_window)
        settings_page.pack(fill="both", expand=True)

        def close_window():
            try:
                settings_window.grab_release()
            except Exception:
                pass
            settings_window.destroy()

        settings_window.protocol("WM_DELETE_WINDOW", close_window)

    # =====================================================
    # MAIN AREA
    # =====================================================

    def create_main_area(self):

        self.main = ctk.CTkFrame(
            self,
            fg_color="#F6F1E9"
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )

        # =================================================
        # HEADER
        # =================================================

        header = ctk.CTkFrame(
            self.main,
            height=80,
            fg_color="#FFFFFF",
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left",
            padx=30
        )

        ctk.CTkLabel(
            title_frame,
            text="Good Afternoon, Akshay! 👋",
            font=("Arial", 23, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_frame,
            text="Here's what's happening at your café today.",
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(
            anchor="w"
        )

        # Refresh
        ctk.CTkButton(
            header,
            text="↻",
            width=42,
            height=42,
            fg_color="#F4EEE7",
            hover_color="#E9DED2",
            text_color="#5B4030",
            corner_radius=12,
            font=("Arial", 20, "bold"),
            command=self.refresh_dashboard
        ).pack(
            side="right",
            padx=8
        )

        # Notification
        ctk.CTkButton(
            header,
            text="🔔",
            width=42,
            height=42,
            fg_color="#F4EEE7",
            hover_color="#E9DED2",
            text_color="#5B4030",
            corner_radius=12
        ).pack(
            side="right",
            padx=8
        )

        # Logout
        ctk.CTkButton(
            header,
            text="Logout",
            width=90,
            height=38,
            fg_color="#3A2116",
            hover_color="#553222",
            text_color="white",
            corner_radius=9,
            command=self.logout_callback
        ).pack(
            side="right",
            padx=15
        )

        # =================================================
        # SCROLLABLE CONTENT
        # =================================================

        self.content = ctk.CTkScrollableFrame(
            self.main,
            fg_color="#F6F1E9"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.build_dashboard()

    # =====================================================
    # BUILD DASHBOARD
    # =====================================================

    def build_dashboard(self):

        # Clear existing
        for widget in self.content.winfo_children():
            widget.destroy()

        # Get live data
        data = self.get_dashboard_data()

        # =================================================
        # STAT CARDS
        # =================================================

        stats = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            pady=(0, 15)
        )

        self.create_stat_card(
            stats,
            "Today's Revenue",
            f"₹{data['today_revenue']:,.2f}",
            data["revenue_change"],
            "💰"
        )

        self.create_stat_card(
            stats,
            "Total Orders",
            str(data["total_orders"]),
            data["orders_change"],
            "🧾"
        )

        self.create_stat_card(
            stats,
            "Customers",
            str(data["customers"]),
            data["customers_change"],
            "👥"
        )

        self.create_stat_card(
            stats,
            "Average Order",
            f"₹{data['average_order']:,.2f}",
            "Live database data",
            "📊"
        )

        # =================================================
        # SALES + POPULAR
        # =================================================

        row = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        row.pack(
            fill="x"
        )

        # -------------------------------------------------
        # SALES ANALYTICS
        # -------------------------------------------------

        sales_card = ctk.CTkFrame(
            row,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        sales_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        ctk.CTkLabel(
            sales_card,
            text="📈  Sales Analytics",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 2)
        )

        ctk.CTkLabel(
            sales_card,
            text="Revenue overview · Last 7 days",
            font=("Arial", 11),
            text_color="#91837A"
        ).pack(
            anchor="w",
            padx=20
        )

        self.create_sales_chart(
            sales_card,
            data["daily_sales"]
        )

        # -------------------------------------------------
        # POPULAR ITEMS
        # -------------------------------------------------

        popular = ctk.CTkFrame(
            row,
            width=330,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        popular.pack(
            side="right",
            fill="y",
            padx=(8, 0)
        )

        popular.pack_propagate(False)

        ctk.CTkLabel(
            popular,
            text="🔥  Popular Items",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 2)
        )

        ctk.CTkLabel(
            popular,
            text="Top selling items",
            font=("Arial", 11),
            text_color="#91837A"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        popular_items = data["popular_items"]

        if not popular_items:

            ctk.CTkLabel(
                popular,
                text="No order data yet",
                font=("Arial", 11),
                text_color="#95867B"
            ).pack(
                pady=30
            )

        else:

            for icon, name, quantity in popular_items:

                item = ctk.CTkFrame(
                    popular,
                    fg_color="#FBF8F3",
                    corner_radius=10
                )

                item.pack(
                    fill="x",
                    padx=15,
                    pady=5
                )

                ctk.CTkLabel(
                    item,
                    text=icon,
                    font=("Arial", 22)
                ).pack(
                    side="left",
                    padx=10,
                    pady=8
                )

                info = ctk.CTkFrame(
                    item,
                    fg_color="transparent"
                )

                info.pack(
                    side="left"
                )

                ctk.CTkLabel(
                    info,
                    text=name,
                    font=("Arial", 12, "bold"),
                    text_color="#3D2A20"
                ).pack(
                    anchor="w"
                )

                ctk.CTkLabel(
                    info,
                    text=f"{quantity} sold",
                    font=("Arial", 9),
                    text_color="#95867B"
                ).pack(
                    anchor="w"
                )

        # =================================================
        # BOTTOM
        # =================================================

        bottom = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            pady=(15, 0)
        )

        # -------------------------------------------------
        # RECENT ORDERS
        # -------------------------------------------------

        orders_card = ctk.CTkFrame(
            bottom,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        orders_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        ctk.CTkLabel(
            orders_card,
            text="🧾  Recent Orders",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 12)
        )

        recent_orders = data["recent_orders"]

        if not recent_orders:

            ctk.CTkLabel(
                orders_card,
                text="No orders available",
                font=("Arial", 12),
                text_color="#897A70"
            ).pack(
                pady=30
            )

        else:

            for order in recent_orders:

                order_id = order["id"]
                customer = order["customer"]
                amount = order["amount"]
                status = order["status"]

                order_frame = ctk.CTkFrame(
                    orders_card,
                    fg_color="#FBF8F3",
                    corner_radius=9
                )

                order_frame.pack(
                    fill="x",
                    padx=15,
                    pady=4
                )

                ctk.CTkLabel(
                    order_frame,
                    text=f"#{order_id}",
                    font=("Arial", 11, "bold"),
                    text_color="#65412E",
                    width=65
                ).pack(
                    side="left",
                    padx=10
                )

                ctk.CTkLabel(
                    order_frame,
                    text=customer,
                    font=("Arial", 11),
                    text_color="#3D2A20",
                    width=150,
                    anchor="w"
                ).pack(
                    side="left"
                )

                ctk.CTkLabel(
                    order_frame,
                    text=f"₹{amount:,.2f}",
                    font=("Arial", 11, "bold"),
                    text_color="#3D2A20",
                    width=80
                ).pack(
                    side="left"
                )

                status_color = {
                    "Pending": "#A86A2D",
                    "Preparing": "#B45F32",
                    "Ready": "#3D7A52",
                    "Completed": "#34735C",
                    "Cancelled": "#A33E32"
                }.get(
                    status,
                    "#8A5A32"
                )

                ctk.CTkLabel(
                    order_frame,
                    text=status,
                    font=("Arial", 10, "bold"),
                    text_color=status_color
                ).pack(
                    side="right",
                    padx=15
                )

        # -------------------------------------------------
        # TABLE STATUS
        # -------------------------------------------------

        tables_card = ctk.CTkFrame(
            bottom,
            width=330,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        tables_card.pack(
            side="right",
            fill="y",
            padx=(8, 0)
        )

        tables_card.pack_propagate(False)

        ctk.CTkLabel(
            tables_card,
            text="🪑  Table Status",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        table_info = data["table_info"]

        for status, number, text_color in table_info:

            box = ctk.CTkFrame(
                tables_card,
                fg_color="#FBF8F3",
                corner_radius=10
            )

            box.pack(
                fill="x",
                padx=18,
                pady=6
            )

            ctk.CTkLabel(
                box,
                text=status,
                font=("Arial", 12),
                text_color="#5E5148"
            ).pack(
                side="left",
                padx=12,
                pady=10
            )

            ctk.CTkLabel(
                box,
                text=str(number),
                font=("Arial", 15, "bold"),
                text_color=text_color
            ).pack(
                side="right",
                padx=15
            )

        # -------------------------------------------------
        # LOW STOCK
        # -------------------------------------------------

        ctk.CTkLabel(
            tables_card,
            text="⚠ Low Stock",
            font=("Arial", 14, "bold"),
            text_color="#9A542F"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        low_stock = data["low_stock"]

        if low_stock:

            low_stock_text = " · ".join(
                item[0] for item in low_stock[:4]
            )

        else:

            low_stock_text = "No low stock items"

        ctk.CTkLabel(
            tables_card,
            text=low_stock_text,
            font=("Arial", 11),
            text_color="#877970",
            wraplength=280
        ).pack(
            anchor="w",
            padx=20
        )

    # =====================================================
    # LIVE DATABASE DATA
    # =====================================================

    def get_dashboard_data(self):

        orders = get_all_orders()

        connection = get_connection()
        cursor = connection.cursor()

        # -------------------------------------------------
        # TODAY
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                COALESCE(SUM(total), 0),
                COUNT(*)
            FROM orders
            WHERE date(created_at) = date('now', 'localtime')
              AND status != 'Cancelled'
        """)

        today_result = cursor.fetchone()

        today_revenue = float(
            today_result[0] or 0
        )

        today_orders = int(
            today_result[1] or 0
        )

        # -------------------------------------------------
        # YESTERDAY
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                COALESCE(SUM(total), 0),
                COUNT(*)
            FROM orders
            WHERE date(created_at) =
                  date('now', 'localtime', '-1 day')
              AND status != 'Cancelled'
        """)

        yesterday_result = cursor.fetchone()

        yesterday_revenue = float(
            yesterday_result[0] or 0
        )

        yesterday_orders = int(
            yesterday_result[1] or 0
        )

        # -------------------------------------------------
        # CUSTOMERS
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role = 'Customer'
        """)

        customers = int(
            cursor.fetchone()[0] or 0
        )

        # -------------------------------------------------
        # TABLES
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                status,
                COUNT(*)
            FROM cafe_tables
            GROUP BY status
        """)

        table_rows = cursor.fetchall()

        table_counts = {
            "Available": 0,
            "Occupied": 0,
            "Reserved": 0
        }

        for status, count in table_rows:

            table_counts[status] = count

        # -------------------------------------------------
        # LOW STOCK
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                item_name,
                quantity,
                unit,
                minimum_stock
            FROM inventory
            WHERE quantity <= minimum_stock
            ORDER BY quantity ASC
        """)

        low_stock = cursor.fetchall()

        # -------------------------------------------------
        # DAILY SALES - LAST 7 DAYS
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                date(created_at),
                COALESCE(SUM(total), 0)
            FROM orders
            WHERE date(created_at) >=
                  date('now', 'localtime', '-6 day')
              AND status != 'Cancelled'
            GROUP BY date(created_at)
            ORDER BY date(created_at)
        """)

        sales_rows = cursor.fetchall()

        sales_map = {}

        for date_value, amount in sales_rows:

            sales_map[str(date_value)] = float(
                amount or 0
            )

        daily_sales = []

        for days_ago in range(6, -1, -1):

            date_value = (
                datetime.now() -
                timedelta(days=days_ago)
            ).strftime("%Y-%m-%d")

            day_name = (
                datetime.strptime(
                    date_value,
                    "%Y-%m-%d"
                ).strftime("%a")
            )

            daily_sales.append(
                (
                    day_name,
                    sales_map.get(
                        date_value,
                        0
                    )
                )
            )

        # -------------------------------------------------
        # POPULAR ITEMS
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                menu.name,
                menu.image,
                SUM(order_items.quantity) AS total_quantity
            FROM order_items
            JOIN menu
                ON order_items.menu_id = menu.id
            JOIN orders
                ON order_items.order_id = orders.id
            WHERE orders.status != 'Cancelled'
            GROUP BY
                order_items.menu_id
            ORDER BY
                total_quantity DESC
            LIMIT 5
        """)

        popular_rows = cursor.fetchall()

        popular_items = []

        for name, image, quantity in popular_rows:

            icon = image if image else "☕"

            popular_items.append(
                (
                    icon,
                    name,
                    int(quantity or 0)
                )
            )

        # -------------------------------------------------
        # CLOSE DB
        # -------------------------------------------------

        connection.close()

        # -------------------------------------------------
        # AVERAGE ORDER
        # -------------------------------------------------

        if orders:

            average_order = (
                sum(
                    float(order[3] or 0)
                    for order in orders
                    if order[4] != 'Cancelled'
                )
                / max(1, sum(1 for order in orders if order[4] != 'Cancelled'))
            )

        else:

            average_order = 0

        # -------------------------------------------------
        # CHANGE TEXT
        # -------------------------------------------------

        revenue_change = self.calculate_change(
            today_revenue,
            yesterday_revenue,
            "from yesterday"
        )

        orders_change = self.calculate_change(
            today_orders,
            yesterday_orders,
            "from yesterday"
        )

        customers_change = "Live database count"

        # -------------------------------------------------
        # RECENT ORDERS
        # -------------------------------------------------

        recent_orders = []

        for order in orders[:5]:

            order_id = order[0]
            user_id = order[1]
            total = float(order[3] or 0)
            status = order[4]

            customer_name = "Customer"

            try:

                user = get_user_by_id(
                    user_id
                )

                if user:
                    customer_name = user[1]

            except Exception:
                customer_name = "Customer"

            recent_orders.append(
                {
                    "id": order_id,
                    "customer": customer_name,
                    "amount": total,
                    "status": status
                }
            )

        return {
            "today_revenue": today_revenue,
            "total_orders": sum(1 for order in orders if order[4] != 'Cancelled'),
            "customers": customers,
            "average_order": average_order,
            "revenue_change": revenue_change,
            "orders_change": orders_change,
            "customers_change": customers_change,
            "daily_sales": daily_sales,
            "popular_items": popular_items,
            "recent_orders": recent_orders,
            "table_info": [
                (
                    "Available",
                    table_counts["Available"],
                    "#3E7B50"
                ),
                (
                    "Occupied",
                    table_counts["Occupied"],
                    "#A85D35"
                ),
                (
                    "Reserved",
                    table_counts["Reserved"],
                    "#8A7040"
                )
            ],
            "low_stock": low_stock
        }

    # =====================================================
    # CALCULATE CHANGE
    # =====================================================

    def calculate_change(
        self,
        current,
        previous,
        suffix
    ):

        try:

            current = float(current)
            previous = float(previous)

            if previous == 0:

                if current == 0:
                    return "No change"

                return "↑ New activity"

            percentage = (
                (current - previous)
                / previous
            ) * 100

            if percentage >= 0:

                return (
                    f"↑ {percentage:.1f}% "
                    f"{suffix}"
                )

            return (
                f"↓ {abs(percentage):.1f}% "
                f"{suffix}"
            )

        except Exception:

            return "Live database data"

    # =====================================================
    # SALES CHART
    # =====================================================

    def create_sales_chart(
        self,
        parent,
        daily_sales
    ):

        chart = ctk.CTkFrame(
            parent,
            height=230,
            fg_color="#FBF8F3",
            corner_radius=12
        )

        chart.pack(
            fill="x",
            padx=20,
            pady=20
        )

        chart.pack_propagate(False)

        graph = ctk.CTkFrame(
            chart,
            fg_color="transparent"
        )

        graph.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        values = [
            value
            for day, value in daily_sales
        ]

        max_value = max(
            values
        ) if values else 1

        if max_value <= 0:
            max_value = 1

        for day, value in daily_sales:

            bar_area = ctk.CTkFrame(
                graph,
                fg_color="transparent"
            )

            bar_area.pack(
                side="left",
                fill="both",
                expand=True,
                padx=4
            )

            if value >= 1000:

                display_value = (
                    f"₹{value / 1000:.1f}K"
                )

            else:

                display_value = (
                    f"₹{value:.0f}"
                )

            ctk.CTkLabel(
                bar_area,
                text=display_value,
                font=("Arial", 9, "bold"),
                text_color="#604331"
            ).pack(
                pady=(0, 4)
            )

            bar_container = ctk.CTkFrame(
                bar_area,
                fg_color="transparent"
            )

            bar_container.pack(
                fill="both",
                expand=True
            )

            # Minimum visual height
            bar_height = int(
                (value / max_value) * 170
            )

            if value > 0:
                bar_height = max(
                    15,
                    bar_height
                )
            else:
                bar_height = 4

            ctk.CTkFrame(
                bar_container,
                width=24,
                height=bar_height,
                fg_color="#B77A45",
                corner_radius=5
            ).pack(
                side="bottom"
            )

            ctk.CTkLabel(
                bar_area,
                text=day,
                font=("Arial", 9),
                text_color="#87796F"
            ).pack(
                pady=(5, 0)
            )

    # =====================================================
    # REFRESH DASHBOARD
    # =====================================================

    def refresh_dashboard(self):

        self.build_dashboard()

    # =====================================================
    # STAT CARD
    # =====================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        change,
        icon
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=15,
            height=125
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        # Icon
        icon_box = ctk.CTkFrame(
            card,
            width=55,
            height=55,
            fg_color="#F3E5D7",
            corner_radius=12
        )

        icon_box.pack(
            side="left",
            padx=(15, 10),
            pady=20
        )

        icon_box.pack_propagate(False)

        ctk.CTkLabel(
            icon_box,
            text=icon,
            font=("Arial", 25)
        ).pack(
            expand=True
        )

        # Information
        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="both",
            expand=True,
            pady=18
        )

        ctk.CTkLabel(
            info,
            text=title,
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text=value,
            font=("Arial", 22, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=2
        )

        change_color = "#3E8A5A"

        if change.startswith("↓"):
            change_color = "#A33E32"

        ctk.CTkLabel(
            info,
            text=change,
            font=("Arial", 9),
            text_color=change_color
        ).pack(
            anchor="w"
        )