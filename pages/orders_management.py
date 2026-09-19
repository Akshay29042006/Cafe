import customtkinter as ctk

from database import (
    get_all_orders,
    get_order_items,
    get_user_by_id,
    update_order_status
)


class OrdersManagement(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.create_header()
        self.create_summary()
        self.create_orders_area()

        self.load_orders()

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            height=80,
            corner_radius=0
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_area.pack(
            side="left",
            padx=25
        )

        ctk.CTkLabel(
            title_area,
            text="🧾 Orders Management",
            font=("Arial", 24, "bold"),
            text_color="#302017"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_area,
            text="Manage café orders and update order status",
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(anchor="w")

        ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=110,
            height=38,
            fg_color="#70452D",
            hover_color="#563421",
            text_color="white",
            corner_radius=9,
            font=("Arial", 12, "bold"),
            command=self.load_orders
        ).pack(
            side="right",
            padx=25
        )

    # =====================================================
    # SUMMARY CARDS
    # =====================================================

    def create_summary(self):

        self.summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.summary_frame.pack(
            fill="x",
            padx=20,
            pady=18
        )

        self.total_value = self.create_summary_card(
            "📋",
            "Total Orders",
            "0"
        )

        self.pending_value = self.create_summary_card(
            "⏳",
            "Pending",
            "0"
        )

        self.preparing_value = self.create_summary_card(
            "🔥",
            "Preparing",
            "0"
        )

        self.ready_value = self.create_summary_card(
            "✅",
            "Ready",
            "0"
        )

        self.revenue_value = self.create_summary_card(
            "💰",
            "Revenue",
            "₹0"
        )

    def create_summary_card(
        self,
        icon,
        title,
        value
    ):

        card = ctk.CTkFrame(
            self.summary_frame,
            fg_color="#FFFFFF",
            corner_radius=14,
            height=100
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 25)
        ).pack(
            side="left",
            padx=(15, 10)
        )

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            expand=True,
            fill="both",
            pady=15
        )

        ctk.CTkLabel(
            info,
            text=title,
            font=("Arial", 10),
            text_color="#897A70"
        ).pack(anchor="w")

        value_label = ctk.CTkLabel(
            info,
            text=value,
            font=("Arial", 20, "bold"),
            text_color="#302017"
        )

        value_label.pack(
            anchor="w",
            pady=(4, 0)
        )

        return value_label

    # =====================================================
    # ORDERS AREA
    # =====================================================

    def create_orders_area(self):

        container = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            container,
            text="All Orders",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.orders_scroll = ctk.CTkScrollableFrame(
            container,
            fg_color="#FBF8F3"
        )

        self.orders_scroll.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # =====================================================
    # LOAD ORDERS
    # =====================================================

    def load_orders(self):

        for widget in self.orders_scroll.winfo_children():
            widget.destroy()

        try:

            orders = get_all_orders()

        except Exception as e:

            self.show_error(
                "Unable to load orders",
                str(e)
            )

            return

        total_orders = len(orders)
        pending = 0
        preparing = 0
        ready = 0
        revenue = 0

        for order in orders:

            order_id = order[0]
            total = order[3]
            status = order[4]

            revenue += float(total or 0)

            if status == "Pending":
                pending += 1

            elif status == "Preparing":
                preparing += 1

            elif status == "Ready":
                ready += 1

        self.total_value.configure(
            text=str(total_orders)
        )

        self.pending_value.configure(
            text=str(pending)
        )

        self.preparing_value.configure(
            text=str(preparing)
        )

        self.ready_value.configure(
            text=str(ready)
        )

        self.revenue_value.configure(
            text=f"₹{revenue:,.2f}"
        )

        if not orders:

            empty = ctk.CTkFrame(
                self.orders_scroll,
                fg_color="#FFFFFF",
                corner_radius=12
            )

            empty.pack(
                fill="x",
                pady=40
            )

            ctk.CTkLabel(
                empty,
                text="📭",
                font=("Arial", 40)
            ).pack(pady=(25, 5))

            ctk.CTkLabel(
                empty,
                text="No orders found",
                font=("Arial", 17, "bold"),
                text_color="#5E5148"
            ).pack()

            ctk.CTkLabel(
                empty,
                text="Customer orders will appear here.",
                font=("Arial", 11),
                text_color="#897A70"
            ).pack(pady=(3, 25))

            return

        for order in orders:
            self.create_order_card(order)

    # =====================================================
    # ORDER CARD
    # =====================================================

    def create_order_card(self, order):

        order_id = order[0]
        user_id = order[1]
        order_type = order[2]
        total = order[3]
        status = order[4]
        created_at = order[5]

        customer_name = "Customer"

        try:

            user = get_user_by_id(user_id)

            if user:

                # Supports common user tuple formats
                if len(user) >= 2:
                    customer_name = user[1]

        except Exception:
            customer_name = f"User #{user_id}"

        card = ctk.CTkFrame(
            self.orders_scroll,
            fg_color="#FFFFFF",
            corner_radius=13,
            border_width=1,
            border_color="#E8DDD2"
        )

        card.pack(
            fill="x",
            pady=7
        )

        # -------------------------------------------------
        # TOP
        # -------------------------------------------------

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=18,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            top,
            text=f"Order #{order_id}",
            font=("Arial", 15, "bold"),
            text_color="#5D3826"
        ).pack(side="left")

        status_color = {
            "Pending": "#A86A2D",
            "Preparing": "#B45F32",
            "Ready": "#3D7A52",
            "Completed": "#34735C",
            "Cancelled": "#A33E32"
        }.get(
            status,
            "#6F625A"
        )

        ctk.CTkLabel(
            top,
            text=status,
            font=("Arial", 11, "bold"),
            text_color=status_color
        ).pack(side="right")

        # -------------------------------------------------
        # ORDER INFO
        # -------------------------------------------------

        info = ctk.CTkFrame(
            card,
            fg_color="#FBF8F3",
            corner_radius=9
        )

        info.pack(
            fill="x",
            padx=18,
            pady=5
        )

        ctk.CTkLabel(
            info,
            text=f"👤 {customer_name}",
            font=("Arial", 11, "bold"),
            text_color="#3D2A20"
        ).pack(
            side="left",
            padx=12,
            pady=10
        )

        ctk.CTkLabel(
            info,
            text=f"🍽 {order_type}",
            font=("Arial", 10),
            text_color="#75665D"
        ).pack(
            side="left",
            padx=15
        )

        ctk.CTkLabel(
            info,
            text=f"🕒 {created_at}",
            font=("Arial", 10),
            text_color="#75665D"
        ).pack(
            side="left",
            padx=15
        )

        ctk.CTkLabel(
            info,
            text=f"₹{float(total):,.2f}",
            font=("Arial", 13, "bold"),
            text_color="#4E3021"
        ).pack(
            side="right",
            padx=15
        )

        # -------------------------------------------------
        # ACTIONS
        # -------------------------------------------------

        actions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        actions.pack(
            fill="x",
            padx=18,
            pady=(5, 15)
        )

        ctk.CTkButton(
            actions,
            text="👁  View Details",
            width=130,
            height=35,
            fg_color="#E9DDD2",
            hover_color="#DCC9BA",
            text_color="#4C3022",
            corner_radius=8,
            command=lambda oid=order_id:
                self.view_order(oid)
        ).pack(
            side="left"
        )

        status_menu = ctk.CTkComboBox(
            actions,
            values=[
                "Pending",
                "Preparing",
                "Ready",
                "Completed",
                "Cancelled"
            ],
            width=145,
            height=35,
            corner_radius=8,
            border_color="#D8C7B8",
            button_color="#70452D",
            button_hover_color="#563421"
        )

        status_menu.set(status)

        status_menu.pack(
            side="right",
            padx=(8, 8)
        )

        ctk.CTkButton(
            actions,
            text="Update Status",
            width=125,
            height=35,
            fg_color="#70452D",
            hover_color="#563421",
            text_color="white",
            corner_radius=8,
            command=lambda oid=order_id, sm=status_menu:
                self.change_status(oid, sm)
        ).pack(
            side="right"
        )

    # =====================================================
    # VIEW ORDER DETAILS
    # =====================================================

    def view_order(self, order_id):

        try:

            items = get_order_items(order_id)

        except Exception as e:

            self.show_error(
                "Unable to load order details",
                str(e)
            )

            return

        window = ctk.CTkToplevel(self)

        window.title(
            f"Order #{order_id} Details"
        )

        window.geometry(
            "520x600"
        )

        window.minsize(
            450,
            500
        )

        window.transient(
            self.winfo_toplevel()
        )

        window.grab_set()

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        ctk.CTkLabel(
            window,
            text=f"🧾 Order #{order_id}",
            font=("Arial", 23, "bold"),
            text_color="#302017"
        ).pack(
            pady=(25, 5)
        )

        ctk.CTkLabel(
            window,
            text="Order Items",
            font=("Arial", 12),
            text_color="#897A70"
        ).pack()

        # -------------------------------------------------
        # ITEMS
        # -------------------------------------------------

        items_frame = ctk.CTkScrollableFrame(
            window,
            fg_color="#FBF8F3",
            corner_radius=12
        )

        items_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        subtotal = 0

        if not items:

            ctk.CTkLabel(
                items_frame,
                text="No items found",
                font=("Arial", 13),
                text_color="#897A70"
            ).pack(
                pady=30
            )

        else:

            for item in items:

                name = item[1]
                quantity = item[2]
                price = item[3]

                item_total = (
                    float(price) *
                    int(quantity)
                )

                subtotal += item_total

                row = ctk.CTkFrame(
                    items_frame,
                    fg_color="#FFFFFF",
                    corner_radius=9
                )

                row.pack(
                    fill="x",
                    pady=5
                )

                ctk.CTkLabel(
                    row,
                    text=name,
                    font=("Arial", 12, "bold"),
                    text_color="#3D2A20"
                ).pack(
                    side="left",
                    padx=12,
                    pady=10
                )

                ctk.CTkLabel(
                    row,
                    text=f"x{quantity}",
                    font=("Arial", 11),
                    text_color="#75665D"
                ).pack(
                    side="left",
                    padx=10
                )

                ctk.CTkLabel(
                    row,
                    text=f"₹{item_total:,.2f}",
                    font=("Arial", 11, "bold"),
                    text_color="#4E3021"
                ).pack(
                    side="right",
                    padx=12
                )

        # -------------------------------------------------
        # TOTAL
        # -------------------------------------------------

        total_frame = ctk.CTkFrame(
            window,
            fg_color="#F3E5D7",
            corner_radius=10
        )

        total_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            total_frame,
            text="Total",
            font=("Arial", 14, "bold"),
            text_color="#4A2C1D"
        ).pack(
            side="left",
            padx=15,
            pady=12
        )

        ctk.CTkLabel(
            total_frame,
            text=f"₹{subtotal:,.2f}",
            font=("Arial", 17, "bold"),
            text_color="#4A2C1D"
        ).pack(
            side="right",
            padx=15
        )

        # -------------------------------------------------
        # CLOSE
        # -------------------------------------------------

        ctk.CTkButton(
            window,
            text="Close",
            width=100,
            height=38,
            fg_color="#70452D",
            hover_color="#563421",
            corner_radius=8,
            command=window.destroy
        ).pack(
            pady=(0, 20)
        )

    # =====================================================
    # CHANGE STATUS
    # =====================================================

    def change_status(
        self,
        order_id,
        status_menu
    ):

        new_status = status_menu.get()

        if not new_status:
            return

        try:

            update_order_status(
                order_id,
                new_status
            )

            self.load_orders()

        except Exception as e:

            self.show_error(
                "Unable to update status",
                str(e)
            )

    # =====================================================
    # ERROR WINDOW
    # =====================================================

    def show_error(
        self,
        title,
        message
    ):

        error_window = ctk.CTkToplevel(self)

        error_window.title(title)

        error_window.geometry(
            "450x220"
        )

        error_window.resizable(
            False,
            False
        )

        error_window.transient(
            self.winfo_toplevel()
        )

        ctk.CTkLabel(
            error_window,
            text="⚠",
            font=("Arial", 35),
            text_color="#A33E32"
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            error_window,
            text=title,
            font=("Arial", 16, "bold"),
            text_color="#302017"
        ).pack()

        ctk.CTkLabel(
            error_window,
            text=str(message),
            font=("Arial", 10),
            text_color="#75665D",
            wraplength=390
        ).pack(
            pady=8
        )

        ctk.CTkButton(
            error_window,
            text="Close",
            width=100,
            height=35,
            fg_color="#70452D",
            hover_color="#563421",
            command=error_window.destroy
        ).pack(
            pady=10
        )