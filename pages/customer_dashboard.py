import customtkinter as ctk
from tkinter import messagebox

from pages.table_booking import TableBooking
from pages.my_reservations import MyReservations
from pages.offers import OffersPage
from pages.feedback import FeedbackPage
from pages.favorites import FavoritesPage, ensure_favorites_table, is_favorite, toggle_favorite

from database import (
    get_menu_items,
    create_order,
    get_customer_orders,
    get_order_items
)


class CustomerDashboard(ctk.CTkFrame):

    def __init__(self, parent, logout_callback):

        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.logout_callback = logout_callback

        # Temporary demo customer
        # पुढे login session मधून actual ID घेऊ
        self.user_id = 2

        self.cart = {}
        self.selected_offer = None
        ensure_favorites_table()

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
            text="CAFÉ",
            font=("Arial", 10, "bold"),
            text_color="#BFAFA3"
        ).pack(
            pady=(0, 30)
        )

        self.create_nav_button(
            "⌂",
            "Home",
            self.show_home,
            True
        )

        self.create_nav_button(
            "☕",
            "Browse Menu",
            self.show_menu
        )

        self.create_nav_button(
            "🛒",
            "My Cart",
            self.show_cart
        )

        self.create_nav_button(
            "▣",
            "My Orders",
            self.show_orders
        )

        self.create_nav_button(
            "▦",
            "Book a Table",
            self.show_table_booking
        )

        self.create_nav_button(
            "◫",
            "My Reservations",
            self.show_reservations
        )

        self.create_nav_button(
            "★",
            "Offers",
            self.show_offers
        )

        self.create_nav_button(
            "♥",
            "Favorites",
            self.show_favorites
        )

        self.create_nav_button(
            "●",
            "Feedback",
            self.show_feedback
        )

        # Profile

        profile = ctk.CTkFrame(
            self.sidebar,
            fg_color="#41271C",
            corner_radius=12
        )

        profile.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            profile,
            text="👤",
            font=("Arial", 24)
        ).pack(
            side="left",
            padx=8,
            pady=8
        )

        info = ctk.CTkFrame(
            profile,
            fg_color="transparent"
        )

        info.pack(
            side="left"
        )

        ctk.CTkLabel(
            info,
            text="Customer",
            font=("Arial", 12, "bold"),
            text_color="white"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text="Welcome back!",
            font=("Arial", 9),
            text_color="#CDBEB3"
        ).pack(
            anchor="w"
        )

    # =====================================================
    # TABLE BOOKING
    # =====================================================

    def show_table_booking(self):

        self.clear_content()

        booking_page = TableBooking(
            self.content,
            user_id=self.user_id
        )

        booking_page.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # MY RESERVATIONS
    # =====================================================

    def show_reservations(self):

        self.clear_content()

        reservations_page = MyReservations(
            self.content,
            user_id=self.user_id
        )

        reservations_page.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # FAVORITES
    # =====================================================

    def show_favorites(self):

        self.clear_content()

        favorites_page = FavoritesPage(
            self.content,
            user_id=self.user_id,
            on_add_to_cart=self.add_to_cart
        )

        favorites_page.pack(
            fill="both",
            expand=True
        )

    def toggle_item_favorite(self, menu_id):

        try:
            saved = toggle_favorite(
                self.user_id,
                menu_id
            )

            # Refresh the currently displayed menu/category.
            if hasattr(self, "_current_category") and self._current_category:
                self.show_category(self._current_category)
            else:
                self.show_menu()

            if saved:
                messagebox.showinfo(
                    "Favorite Added ♥",
                    "Item added to your Favorites."
                )
            else:
                messagebox.showinfo(
                    "Favorite Removed",
                    "Item removed from your Favorites."
                )

        except Exception as e:
            messagebox.showerror(
                "Favorites Error",
                f"Could not update Favorites.\n\n{e}"
            )

    # =====================================================
    # FEEDBACK
    # =====================================================

    def show_feedback(self):
        self.clear_content()

        feedback_page = FeedbackPage(
            self.content,
            user_id=self.user_id
        )

        feedback_page.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # OFFERS
    # =====================================================

    def show_offers(self):

        self.clear_content()

        offers_page = OffersPage(
            self.content,
            on_apply_offer=self.apply_offer_from_offers
        )

        offers_page.pack(
            fill="both",
            expand=True
        )

    def apply_offer_from_offers(self, offer):

        self.selected_offer = offer

        if not self.cart:
            messagebox.showinfo(
                "Offer Selected",
                f"{offer['code']} selected successfully.\n\n"
                "Add items to your cart and open Checkout to use this offer."
            )
            return

        subtotal = self.calculate_subtotal()

        if subtotal < offer["minimum"]:
            messagebox.showinfo(
                "Minimum Order Required",
                f"{offer['code']} requires a minimum order of ₹{offer['minimum']}.\n\n"
                f"Your current cart total is ₹{subtotal:.0f}."
            )
            self.show_cart()
            return

        messagebox.showinfo(
            "Offer Applied ✓",
            f"{offer['title']} ({offer['code']}) has been applied.\n\n"
            "Your discount will be shown at checkout."
        )

        self.checkout()

    # =====================================================
    # NAV BUTTON
    # =====================================================

    def create_nav_button(
        self,
        icon,
        text,
        command,
        active=False
    ):

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
            fg_color="#70452D" if active else "transparent",
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

        self.create_header()

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

        self.show_home()

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

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

        self.search = ctk.CTkEntry(
            header,
            width=430,
            height=42,
            placeholder_text="Search coffee, food, desserts...",
            font=("Arial", 13),
            fg_color="#FBF8F3",
            border_color="#E1D4C7",
            border_width=1,
            corner_radius=10
        )

        self.search.pack(
            side="left",
            padx=25
        )

        ctk.CTkButton(
            header,
            text="🔔",
            width=45,
            height=42,
            fg_color="#F4EEE7",
            hover_color="#E9DED2",
            text_color="#5B4030",
            corner_radius=10
        ).pack(
            side="right",
            padx=8
        )

        self.cart_button = ctk.CTkButton(
            header,
            text="🛒  0",
            width=75,
            height=42,
            fg_color="#F4EEE7",
            hover_color="#E9DED2",
            text_color="#5B4030",
            corner_radius=10,
            command=self.show_cart
        )

        self.cart_button.pack(
            side="right",
            padx=8
        )

        ctk.CTkLabel(
            header,
            text="👤  Customer",
            font=("Arial", 13, "bold"),
            text_color="#3B2417"
        ).pack(
            side="right",
            padx=15
        )

    # =====================================================
    # CLEAR CONTENT
    # =====================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # =====================================================
    # HOME
    # =====================================================

    def show_home(self):

        self.clear_content()

        welcome = ctk.CTkFrame(
            self.content,
            height=155,
            fg_color="#6B4029",
            corner_radius=18
        )

        welcome.pack(
            fill="x",
            pady=(0, 18)
        )

        welcome.pack_propagate(False)

        ctk.CTkLabel(
            welcome,
            text="Good Afternoon! 👋",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(
            anchor="w",
            padx=28,
            pady=(25, 2)
        )

        ctk.CTkLabel(
            welcome,
            text="What are you craving today?",
            font=("Arial", 16),
            text_color="#E9D8C8"
        ).pack(
            anchor="w",
            padx=28
        )

        ctk.CTkButton(
            welcome,
            text="Explore Menu  →",
            width=150,
            height=38,
            font=("Arial", 12, "bold"),
            fg_color="#F3B562",
            hover_color="#E2A34D",
            text_color="#3B2417",
            corner_radius=10,
            command=self.show_menu
        ).pack(
            anchor="w",
            padx=28,
            pady=12
        )

        ctk.CTkLabel(
            self.content,
            text="Browse Categories",
            font=("Arial", 21, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        categories = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        categories.pack(
            fill="x",
            pady=(0, 20)
        )

        category_data = [
            ("☕", "Coffee"),
            ("🍕", "Pizza"),
            ("🍔", "Burgers"),
            ("🍰", "Desserts"),
            ("🥤", "Beverages")
        ]

        for icon, name in category_data:

            ctk.CTkButton(
                categories,
                text=f"{icon}\n\n{name}",
                font=("Arial", 12, "bold"),
                fg_color="#FFFFFF",
                hover_color="#EFE4D7",
                text_color="#3B2417",
                corner_radius=14,
                height=90,
                command=lambda c=name: self.show_category(c)
            ).pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

        ctk.CTkLabel(
            self.content,
            text="Popular Today 🔥",
            font=("Arial", 21, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        grid = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        grid.pack(
            fill="x"
        )

        menu = get_menu_items()

        popular_names = [
            "Cappuccino",
            "Cold Coffee",
            "Margherita Pizza",
            "Classic Burger"
        ]

        popular_items = [
            item
            for item in menu
            if item[1] in popular_names
        ]

        for index, item in enumerate(popular_items):

            card = self.create_product_card(
                grid,
                item
            )

            card.grid(
                row=0,
                column=index,
                padx=7,
                pady=5,
                sticky="nsew"
            )

        for i in range(4):

            grid.grid_columnconfigure(
                i,
                weight=1
            )

        self.create_offer()
        self.create_loyalty()

    # =====================================================
    # MENU
    # =====================================================

    def show_menu(self):

        self._current_category = None
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="☕ Our Menu",
            font=("Arial", 30, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=(5, 3)
        )

        ctk.CTkLabel(
            self.content,
            text="Freshly prepared just for you",
            font=("Arial", 13),
            text_color="#8A7B70"
        ).pack(
            anchor="w",
            pady=(0, 18)
        )

        categories = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        categories.pack(
            fill="x",
            pady=(0, 18)
        )

        ctk.CTkButton(
            categories,
            text="All",
            width=80,
            height=35,
            fg_color="#3B2417",
            hover_color="#5A3823",
            command=self.show_menu
        ).pack(
            side="left",
            padx=4
        )

        for category in [
            "Coffee",
            "Pizza",
            "Burgers",
            "Desserts",
            "Beverages"
        ]:

            ctk.CTkButton(
                categories,
                text=category,
                width=100,
                height=35,
                fg_color="#FFFFFF",
                hover_color="#E9DED2",
                text_color="#3B2417",
                command=lambda c=category: self.show_category(c)
            ).pack(
                side="left",
                padx=4
            )

        self.display_products(
            get_menu_items()
        )

    # =====================================================
    # CATEGORY
    # =====================================================

    def show_category(self, category):

        self._current_category = category
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text=category,
            font=("Arial", 30, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=(5, 3)
        )

        ctk.CTkButton(
            self.content,
            text="← Back to Menu",
            width=130,
            height=35,
            fg_color="#3B2417",
            hover_color="#5A3823",
            command=self.show_menu
        ).pack(
            anchor="w",
            pady=(0, 18)
        )

        menu = get_menu_items()

        filtered = [
            item
            for item in menu
            if item[2] == category
        ]

        self.display_products(
            filtered
        )

    # =====================================================
    # DISPLAY PRODUCTS
    # =====================================================

    def display_products(self, items):

        grid = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        grid.pack(
            fill="x"
        )

        for index, item in enumerate(items):

            row = index // 3
            column = index % 3

            card = self.create_product_card(
                grid,
                item
            )

            card.grid(
                row=row,
                column=column,
                padx=7,
                pady=7,
                sticky="nsew"
            )

        for column in range(3):

            grid.grid_columnconfigure(
                column,
                weight=1
            )

    # =====================================================
    # PRODUCT CARD
    # =====================================================

    def create_product_card(
        self,
        parent,
        item
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=15,
            height=225
        )

        card.pack_propagate(False)

        image_box = ctk.CTkFrame(
            card,
            height=80,
            fg_color="#F4E7D8",
            corner_radius=12
        )

        image_box.pack(
            fill="x",
            padx=10,
            pady=10
        )

        image_box.pack_propagate(False)

        ctk.CTkLabel(
            image_box,
            text=item[5] or "☕",
            font=("Arial", 40)
        ).pack(
            expand=True
        )

        # Favorite status
        favorite_now = is_favorite(
            self.user_id,
            item[0]
        )

        ctk.CTkLabel(
            card,
            text=item[1],
            font=("Arial", 14, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=14
        )

        ctk.CTkLabel(
            card,
            text=item[4] or "Freshly prepared just for you",
            font=("Arial", 9),
            text_color="#8A7B70"
        ).pack(
            anchor="w",
            padx=14,
            pady=3
        )

        bottom = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            padx=12,
            pady=6
        )

        ctk.CTkLabel(
            bottom,
            text=f"₹{item[3]:.0f}",
            font=("Arial", 15, "bold"),
            text_color="#6B4029"
        ).pack(
            side="left"
        )

        heart_button = ctk.CTkButton(
            bottom,
            text="♥" if favorite_now else "♡",
            width=36,
            height=30,
            font=("Arial", 17, "bold"),
            fg_color="#F7E1E1" if favorite_now else "#F3E9DE",
            hover_color="#EFC7C7",
            text_color="#B3261E" if favorite_now else "#7A4E2D",
            corner_radius=8,
            command=lambda mid=item[0]: self.toggle_item_favorite(mid)
        )

        heart_button.pack(
            side="right",
            padx=(5, 0)
        )

        ctk.CTkButton(
            bottom,
            text="+ Add",
            width=70,
            height=30,
            font=("Arial", 10, "bold"),
            fg_color="#3B2417",
            hover_color="#5A3823",
            corner_radius=8,
            command=lambda i=item: self.add_to_cart(i)
        ).pack(
            side="right"
        )

        return card

    # =====================================================
    # ADD TO CART
    # =====================================================

    def add_to_cart(self, item):

        menu_id = item[0]

        if menu_id in self.cart:

            self.cart[menu_id]["quantity"] += 1

        else:

            self.cart[menu_id] = {
                "item": item,
                "quantity": 1
            }

        self.update_cart_button()

        messagebox.showinfo(
            "Added to Cart",
            f"{item[1]} added to your cart!"
        )

    # =====================================================
    # CART COUNT
    # =====================================================

    def get_cart_count(self):

        return sum(
            data["quantity"]
            for data in self.cart.values()
        )

    # =====================================================
    # UPDATE CART BUTTON
    # =====================================================

    def update_cart_button(self):

        self.cart_button.configure(
            text=f"🛒  {self.get_cart_count()}"
        )

    # =====================================================
    # CART
    # =====================================================

    def show_cart(self):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="🛒 My Cart",
            font=("Arial", 30, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        if not self.cart:

            empty = ctk.CTkFrame(
                self.content,
                fg_color="#FFFFFF",
                corner_radius=18,
                height=270
            )

            empty.pack(
                fill="x"
            )

            empty.pack_propagate(False)

            ctk.CTkLabel(
                empty,
                text="🛒",
                font=("Arial", 55)
            ).pack(
                pady=(45, 5)
            )

            ctk.CTkLabel(
                empty,
                text="Your cart is empty",
                font=("Arial", 20, "bold"),
                text_color="#3B2417"
            ).pack()

            ctk.CTkButton(
                empty,
                text="Browse Menu",
                width=150,
                height=40,
                fg_color="#3B2417",
                hover_color="#5A3823",
                command=self.show_menu
            ).pack(
                pady=18
            )

            return

        for menu_id, data in self.cart.items():

            item = data["item"]
            quantity = data["quantity"]

            card = ctk.CTkFrame(
                self.content,
                fg_color="#FFFFFF",
                corner_radius=13
            )

            card.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=item[5],
                font=("Arial", 35)
            ).pack(
                side="left",
                padx=15,
                pady=10
            )

            info = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            info.pack(
                side="left",
                fill="both",
                expand=True
            )

            ctk.CTkLabel(
                info,
                text=item[1],
                font=("Arial", 15, "bold"),
                text_color="#302017"
            ).pack(
                anchor="w",
                pady=(12, 2)
            )

            ctk.CTkLabel(
                info,
                text=f"₹{item[3]:.0f} each",
                font=("Arial", 10),
                text_color="#8A7B70"
            ).pack(
                anchor="w"
            )

            quantity_box = ctk.CTkFrame(
                card,
                fg_color="#F5EEE6",
                corner_radius=8
            )

            quantity_box.pack(
                side="left",
                padx=15
            )

            ctk.CTkButton(
                quantity_box,
                text="−",
                width=30,
                height=30,
                fg_color="transparent",
                hover_color="#E4D5C6",
                text_color="#3B2417",
                command=lambda i=menu_id: self.change_quantity(i, -1)
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                quantity_box,
                text=str(quantity),
                width=30,
                text_color="#3B2417",
                font=("Arial", 12, "bold")
            ).pack(
                side="left"
            )

            ctk.CTkButton(
                quantity_box,
                text="+",
                width=30,
                height=30,
                fg_color="transparent",
                hover_color="#E4D5C6",
                text_color="#3B2417",
                command=lambda i=menu_id: self.change_quantity(i, 1)
            ).pack(
                side="left"
            )

            total = item[3] * quantity

            ctk.CTkLabel(
                card,
                text=f"₹{total:.0f}",
                font=("Arial", 15, "bold"),
                text_color="#6B4029",
                width=90
            ).pack(
                side="left"
            )

            ctk.CTkButton(
                card,
                text="🗑",
                width=40,
                height=35,
                fg_color="#FCE7E2",
                hover_color="#F3D0C9",
                text_color="#A83D2C",
                corner_radius=8,
                command=lambda i=menu_id: self.remove_from_cart(i)
            ).pack(
                side="right",
                padx=15
            )

        self.create_cart_summary()

    # =====================================================
    # CART SUMMARY
    # =====================================================

    def create_cart_summary(self):

        summary = ctk.CTkFrame(
            self.content,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        summary.pack(
            fill="x",
            pady=20
        )

        subtotal = self.calculate_subtotal()

        discount = self.calculate_discount(
            subtotal
        )

        total = subtotal - discount

        ctk.CTkLabel(
            summary,
            text="Order Summary",
            font=("Arial", 20, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 12)
        )

        self.summary_row(
            summary,
            "Subtotal",
            f"₹{subtotal:.0f}"
        )

        self.summary_row(
            summary,
            "Discount",
            f"- ₹{discount:.0f}"
        )

        ctk.CTkFrame(
            summary,
            height=1,
            fg_color="#E8DDD2"
        ).pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.summary_row(
            summary,
            "Grand Total",
            f"₹{total:.0f}",
            True
        )

        ctk.CTkButton(
            summary,
            text="Proceed to Checkout  →",
            height=48,
            font=("Arial", 14, "bold"),
            fg_color="#3B2417",
            hover_color="#5A3823",
            corner_radius=10,
            command=self.checkout
        ).pack(
            fill="x",
            padx=20,
            pady=(10, 20)
        )

    # =====================================================
    # SUMMARY ROW
    # =====================================================

    def summary_row(
        self,
        parent,
        label,
        value,
        bold=False
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=4
        )

        ctk.CTkLabel(
            row,
            text=label,
            font=(
                "Arial",
                13,
                "bold" if bold else "normal"
            ),
            text_color="#4D3B30"
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            row,
            text=value,
            font=("Arial", 15, "bold"),
            text_color="#6B4029"
        ).pack(
            side="right"
        )

    # =====================================================
    # CALCULATE SUBTOTAL
    # =====================================================

    def calculate_subtotal(self):

        return sum(
            data["item"][3] * data["quantity"]
            for data in self.cart.values()
        )

    # =====================================================
    # CALCULATE DISCOUNT
    # =====================================================

    def calculate_discount(
        self,
        subtotal
    ):

        # Selected offer has priority over the default café discount.
        if self.selected_offer:

            offer = self.selected_offer

            if subtotal < offer["minimum"]:
                return 0

            discount_type = offer.get("discount_type", "percent")
            discount_value = float(offer.get("discount", 0) or 0)

            if discount_type == "flat":
                return min(discount_value, subtotal)

            return min(subtotal * (discount_value / 100), subtotal)

        # Existing automatic café discount
        if subtotal >= 500:
            return subtotal * 0.10

        return 0

    # =====================================================
    # CHANGE QUANTITY
    # =====================================================

    def change_quantity(
        self,
        menu_id,
        amount
    ):

        if menu_id not in self.cart:
            return

        self.cart[menu_id]["quantity"] += amount

        if self.cart[menu_id]["quantity"] <= 0:

            del self.cart[menu_id]

        self.update_cart_button()

        self.show_cart()

    # =====================================================
    # REMOVE FROM CART
    # =====================================================

    def remove_from_cart(
        self,
        menu_id
    ):

        if menu_id in self.cart:

            del self.cart[menu_id]

        self.update_cart_button()

        self.show_cart()

    # =====================================================
    # CHECKOUT
    # =====================================================

    def checkout(self):

        if not self.cart:

            messagebox.showwarning(
                "Empty Cart",
                "Please add items to your cart first."
            )

            return

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="💳 Checkout",
            font=("Arial", 30, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        checkout_box = ctk.CTkFrame(
            self.content,
            fg_color="#FFFFFF",
            corner_radius=18
        )

        checkout_box.pack(
            fill="x"
        )

        ctk.CTkLabel(
            checkout_box,
            text="Choose Order Type",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 12)
        )

        self.order_type = ctk.StringVar(
            value="Dine In"
        )

        radio_frame = ctk.CTkFrame(
            checkout_box,
            fg_color="transparent"
        )

        radio_frame.pack(
            fill="x",
            padx=20
        )

        ctk.CTkRadioButton(
            radio_frame,
            text="🍽  Dine In",
            variable=self.order_type,
            value="Dine In",
            font=("Arial", 13, "bold"),
            text_color="#3B2417"
        ).pack(
            side="left",
            padx=15,
            pady=15
        )

        ctk.CTkRadioButton(
            radio_frame,
            text="🥡  Takeaway",
            variable=self.order_type,
            value="Takeaway",
            font=("Arial", 13, "bold"),
            text_color="#3B2417"
        ).pack(
            side="left",
            padx=15
        )

        subtotal = self.calculate_subtotal()

        discount = self.calculate_discount(
            subtotal
        )

        total = subtotal - discount

        ctk.CTkLabel(
            checkout_box,
            text="Payment Summary",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        self.summary_row(
            checkout_box,
            "Subtotal",
            f"₹{subtotal:.0f}"
        )

        self.summary_row(
            checkout_box,
            "Discount",
            f"- ₹{discount:.0f}"
        )

        ctk.CTkFrame(
            checkout_box,
            height=1,
            fg_color="#E8DDD2"
        ).pack(
            fill="x",
            padx=25,
            pady=12
        )

        self.summary_row(
            checkout_box,
            "Total Payable",
            f"₹{total:.0f}",
            True
        )

        if self.selected_offer:

            offer_text = (
                f"✓ {self.selected_offer['code']} • "
                f"{self.selected_offer['title']}"
            )

            ctk.CTkLabel(
                checkout_box,
                text=offer_text,
                font=("Arial", 11, "bold"),
                text_color="#5B7A4A",
                fg_color="#EAF3E5",
                corner_radius=8,
                padx=12,
                pady=7
            ).pack(
                anchor="w",
                padx=25,
                pady=(5, 5)
            )

        ctk.CTkLabel(
            checkout_box,
            text="Payment Method",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        self.payment_method = ctk.StringVar(
            value="Cash"
        )

        payment_frame = ctk.CTkFrame(
            checkout_box,
            fg_color="transparent"
        )

        payment_frame.pack(
            fill="x",
            padx=20
        )

        for text, value in [
            ("💵 Cash", "Cash"),
            ("💳 Card", "Card"),
            ("📱 UPI", "UPI")
        ]:

            ctk.CTkRadioButton(
                payment_frame,
                text=text,
                variable=self.payment_method,
                value=value,
                font=("Arial", 12)
            ).pack(
                side="left",
                padx=15
            )

        ctk.CTkButton(
            checkout_box,
            text="✓  PLACE ORDER",
            height=52,
            font=("Arial", 15, "bold"),
            fg_color="#3B2417",
            hover_color="#5A3823",
            corner_radius=10,
            command=self.place_order
        ).pack(
            fill="x",
            padx=25,
            pady=(25, 12)
        )

        ctk.CTkButton(
            checkout_box,
            text="← Back to Cart",
            height=40,
            font=("Arial", 12),
            fg_color="#EFE5DB",
            hover_color="#E2D5C8",
            text_color="#3B2417",
            corner_radius=9,
            command=self.show_cart
        ).pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

    # =====================================================
    # PLACE ORDER
    # =====================================================

    def place_order(self):

        if not self.cart:
            return

        subtotal = self.calculate_subtotal()

        discount = self.calculate_discount(
            subtotal
        )

        total = subtotal - discount

        order_type = self.order_type.get()

        cart_items = []

        for menu_id, data in self.cart.items():

            item = data["item"]

            cart_items.append(
                (
                    menu_id,
                    data["quantity"],
                    item[3]
                )
            )

        try:

            order_id = create_order(
                self.user_id,
                order_type,
                cart_items,
                total
            )

            self.cart.clear()
            self.selected_offer = None

            self.update_cart_button()

            self.show_order_success(
                order_id,
                total,
                order_type
            )

        except Exception as error:

            messagebox.showerror(
                "Order Error",
                f"Unable to place order.\n\n{error}"
            )

    # =====================================================
    # ORDER SUCCESS
    # =====================================================

    def show_order_success(
        self,
        order_id,
        total,
        order_type
    ):

        self.clear_content()

        success = ctk.CTkFrame(
            self.content,
            fg_color="#FFFFFF",
            corner_radius=20,
            height=430
        )

        success.pack(
            fill="x",
            pady=30
        )

        success.pack_propagate(False)

        ctk.CTkLabel(
            success,
            text="✓",
            font=("Arial", 55, "bold"),
            text_color="#3E8A5A"
        ).pack(
            pady=(45, 5)
        )

        ctk.CTkLabel(
            success,
            text="Order Placed Successfully!",
            font=("Arial", 25, "bold"),
            text_color="#302017"
        ).pack()

        ctk.CTkLabel(
            success,
            text=f"Order #{order_id}",
            font=("Arial", 18, "bold"),
            text_color="#6B4029"
        ).pack(
            pady=10
        )

        ctk.CTkLabel(
            success,
            text=f"Order Type: {order_type}",
            font=("Arial", 12),
            text_color="#806F63"
        ).pack()

        ctk.CTkLabel(
            success,
            text=f"Total Amount: ₹{total:.0f}",
            font=("Arial", 15, "bold"),
            text_color="#3B2417"
        ).pack(
            pady=5
        )

        ctk.CTkLabel(
            success,
            text="Your order has been sent to the café.",
            font=("Arial", 12),
            text_color="#806F63"
        ).pack(
            pady=5
        )

        ctk.CTkButton(
            success,
            text="View My Orders",
            width=190,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="#3B2417",
            hover_color="#5A3823",
            corner_radius=10,
            command=self.show_orders
        ).pack(
            pady=20
        )

    # =====================================================
    # MY ORDERS
    # =====================================================

    def show_orders(self):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="▣ My Orders",
            font=("Arial", 30, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        try:

            orders = get_customer_orders(
                self.user_id
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return

        if not orders:

            empty = ctk.CTkFrame(
                self.content,
                fg_color="#FFFFFF",
                corner_radius=18,
                height=270
            )

            empty.pack(
                fill="x"
            )

            empty.pack_propagate(False)

            ctk.CTkLabel(
                empty,
                text="▣",
                font=("Arial", 50)
            ).pack(
                pady=(45, 5)
            )

            ctk.CTkLabel(
                empty,
                text="No orders yet",
                font=("Arial", 20, "bold"),
                text_color="#3B2417"
            ).pack()

            ctk.CTkButton(
                empty,
                text="Order Something",
                width=160,
                height=40,
                fg_color="#3B2417",
                hover_color="#5A3823",
                command=self.show_menu
            ).pack(
                pady=18
            )

            return

        for order in orders:

            order_id = order[0]
            order_type = order[1]
            total = order[2]
            status = order[3]
            created_at = order[4]

            self.create_order_card(
                order_id,
                order_type,
                total,
                status,
                created_at
            )

    # =====================================================
    # ORDER CARD
    # =====================================================

    def create_order_card(
        self,
        order_id,
        order_type,
        total,
        status,
        created_at
    ):

        card = ctk.CTkFrame(
            self.content,
            fg_color="#FFFFFF",
            corner_radius=16
        )

        card.pack(
            fill="x",
            pady=7
        )

        # Header
        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 8)
        )

        ctk.CTkLabel(
            header,
            text=f"Order #{order_id}",
            font=("Arial", 18, "bold"),
            text_color="#302017"
        ).pack(
            side="left"
        )

        status_color = {
            "Pending": "#C78A25",
            "Confirmed": "#3D6FA8",
            "Preparing": "#8A5CA8",
            "Ready": "#3E8A5A",
            "Completed": "#3E8A5A",
            "Cancelled": "#A83D2C"
        }.get(
            status,
            "#6B4029"
        )

        ctk.CTkLabel(
            header,
            text=f"● {status}",
            font=("Arial", 12, "bold"),
            text_color=status_color
        ).pack(
            side="right"
        )

        # Items
        items = get_order_items(
            order_id
        )

        items_frame = ctk.CTkFrame(
            card,
            fg_color="#F9F5F0",
            corner_radius=10
        )

        items_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        for item in items:

            item_name = item[1]
            quantity = item[2]
            price = item[3]

            row = ctk.CTkFrame(
                items_frame,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=12,
                pady=5
            )

            ctk.CTkLabel(
                row,
                text=f"{item_name}  × {quantity}",
                font=("Arial", 11),
                text_color="#4D3B30"
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                row,
                text=f"₹{price * quantity:.0f}",
                font=("Arial", 11, "bold"),
                text_color="#6B4029"
            ).pack(
                side="right"
            )

        # Footer
        footer = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        footer.pack(
            fill="x",
            padx=20,
            pady=(8, 18)
        )

        ctk.CTkLabel(
            footer,
            text=f"🍽 {order_type}",
            font=("Arial", 11),
            text_color="#806F63"
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            footer,
            text=f"Total: ₹{total:.0f}",
            font=("Arial", 14, "bold"),
            text_color="#3B2417"
        ).pack(
            side="right"
        )

        ctk.CTkLabel(
            card,
            text=f"Placed: {created_at}",
            font=("Arial", 9),
            text_color="#9A8B80"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )

    # =====================================================
    # OFFER
    # =====================================================

    def create_offer(self):

        offer = ctk.CTkFrame(
            self.content,
            height=100,
            fg_color="#E9D6BD",
            corner_radius=15
        )

        offer.pack(
            fill="x",
            pady=20
        )

        offer.pack_propagate(False)

        ctk.CTkLabel(
            offer,
            text="🎁  SPECIAL OFFER",
            font=("Arial", 12, "bold"),
            text_color="#70452D"
        ).pack(
            anchor="w",
            padx=22,
            pady=(15, 0)
        )

        ctk.CTkLabel(
            offer,
            text="Get 10% OFF on orders above ₹500!",
            font=("Arial", 18, "bold"),
            text_color="#3B2417"
        ).pack(
            anchor="w",
            padx=22
        )

        ctk.CTkLabel(
            offer,
            text="Your discount is automatically applied at checkout.",
            font=("Arial", 10),
            text_color="#80634D"
        ).pack(
            anchor="w",
            padx=22
        )

    # =====================================================
    # LOYALTY
    # =====================================================

    def create_loyalty(self):

        loyalty = ctk.CTkFrame(
            self.content,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        loyalty.pack(
            fill="x"
        )

        ctk.CTkLabel(
            loyalty,
            text="⭐ Your Loyalty Points",
            font=("Arial", 18, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        ctk.CTkLabel(
            loyalty,
            text="420 Points",
            font=("Arial", 25, "bold"),
            text_color="#6B4029"
        ).pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            loyalty,
            text="80 more points to unlock your next reward 🎁",
            font=("Arial", 11),
            text_color="#8A7B70"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

    # =====================================================
    # PLACEHOLDER
    # =====================================================

    def placeholder(self):

        messagebox.showinfo(
            "Coming Soon",
            "This feature will be added in the next module."
        )