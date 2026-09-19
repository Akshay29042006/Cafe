import sqlite3
import customtkinter as ctk
from tkinter import messagebox

DATABASE_NAME = "cafe.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def ensure_offers_table():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subtitle TEXT,
            code TEXT UNIQUE NOT NULL,
            discount_type TEXT NOT NULL DEFAULT 'percent',
            discount_value REAL NOT NULL DEFAULT 0,
            minimum_order REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Active',
            color TEXT DEFAULT '#7A4E2D',
            icon TEXT DEFAULT '🎁',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM offers")
    if cursor.fetchone()[0] == 0:
        defaults = [
            ("Brew & Save", "20% OFF on your order", "BREW20", "percent", 20, 499, "Active", "#7A4E2D", "☕"),
            ("Coffee Break", "₹100 OFF", "COFFEE100", "flat", 100, 599, "Active", "#9A633F", "☕"),
            ("Café Combo", "15% OFF on food orders", "COMBO15", "percent", 15, 699, "Active", "#6B4A38", "🍕"),
            ("Weekend Treat", "10% OFF", "WEEKEND10", "percent", 10, 399, "Active", "#A66A42", "🍰")
        ]
        cursor.executemany("""
            INSERT INTO offers
            (title, subtitle, code, discount_type, discount_value,
             minimum_order, status, color, icon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, defaults)
    connection.commit()
    connection.close()


def load_active_offers():
    ensure_offers_table()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, title, subtitle, code, discount_type, discount_value,
               minimum_order, status, color, icon
        FROM offers
        WHERE status = 'Active'
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    connection.close()

    offers = []
    for row in rows:
        offer_id, title, subtitle, code, discount_type, discount_value, minimum, status, color, icon = row
        if discount_type == "flat":
            tag = f"₹{discount_value:.0f} OFF"
        else:
            tag = f"{discount_value:.0f}% OFF"
        if subtitle:
            description = subtitle
        elif discount_type == "flat":
            description = f"Get ₹{discount_value:.0f} OFF on orders above ₹{minimum:.0f}."
        else:
            description = f"Enjoy {discount_value:.0f}% discount on orders above ₹{minimum:.0f}."
        offers.append({
            "id": offer_id,
            "code": code,
            "title": title,
            "subtitle": subtitle or tag,
            "description": description,
            "discount": float(discount_value),
            "discount_type": discount_type,
            "minimum": float(minimum),
            "icon": icon or "🎁",
            "tag": tag,
            "color": color or "#7A4E2D"
        })
    return offers


class OffersPage(ctk.CTkFrame):
    def __init__(self, parent, on_apply_offer=None):
        super().__init__(parent, fg_color="#F6F1E9")
        self.on_apply_offer = on_apply_offer
        self.selected_offer = None
        self.offers = load_active_offers()
        self.create_header()
        self.create_coupon_bar()
        self.create_offers()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 15))
        ctk.CTkLabel(header, text="🎁  Offers & Rewards",
                     font=("Arial", 30, "bold"), text_color="#302017").pack(anchor="w")
        ctk.CTkLabel(header, text="Save more on every delicious order",
                     font=("Arial", 13), text_color="#8A7B70").pack(anchor="w", pady=(4, 0))

    def create_coupon_bar(self):
        card = ctk.CTkFrame(self, height=105, corner_radius=18, fg_color="#302017")
        card.pack(fill="x", padx=30, pady=(0, 20))
        card.pack_propagate(False)
        left = ctk.CTkFrame(card, fg_color="transparent")
        left.pack(side="left", padx=25)
        ctk.CTkLabel(left, text="Have a coupon code?", font=("Arial", 16, "bold"),
                     text_color="white").pack(anchor="w", pady=(15, 3))
        ctk.CTkLabel(left, text="Select an offer below to use it at checkout.",
                     font=("Arial", 10), text_color="#D8C9BE").pack(anchor="w")
        self.selected_label = ctk.CTkLabel(card, text="No offer selected",
                                           font=("Arial", 11, "bold"), text_color="#E9D6BD")
        self.selected_label.pack(side="right", padx=25)

    def create_offers(self):
        offers_frame = ctk.CTkFrame(self, fg_color="transparent")
        offers_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        ctk.CTkLabel(offers_frame, text="Available Offers", font=("Arial", 21, "bold"),
                     text_color="#302017").pack(anchor="w", padx=10, pady=(0, 8))

        if not self.offers:
            ctk.CTkFrame(offers_frame, height=1, fg_color="transparent").pack(fill="x", expand=True)
            ctk.CTkLabel(offers_frame, text="No active offers available right now.",
                         font=("Arial", 14), text_color="#8A7B70").pack(pady=45)
            return

        for offer in self.offers[:6]:
            self.create_offer_card(offers_frame, offer)

    def create_offer_card(self, parent, offer):
        card = ctk.CTkFrame(parent, height=145, corner_radius=17, fg_color="#FFFFFF",
                            border_width=1, border_color="#E8DDD2")
        card.pack(fill="x", padx=10, pady=7)
        card.pack_propagate(False)

        icon_box = ctk.CTkFrame(card, width=75, height=75, corner_radius=18, fg_color="#F2E4D5")
        icon_box.pack(side="left", padx=(18, 15), pady=35)
        icon_box.pack_propagate(False)
        ctk.CTkLabel(icon_box, text=offer["icon"], font=("Arial", 30)).pack(expand=True)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=18)
        top = ctk.CTkFrame(info, fg_color="transparent")
        top.pack(fill="x")
        ctk.CTkLabel(top, text=offer["title"], font=("Arial", 16, "bold"),
                     text_color="#302017").pack(side="left")
        ctk.CTkLabel(top, text=offer["tag"], font=("Arial", 10, "bold"),
                     text_color="#A55B2A", fg_color="#F8E9D8", corner_radius=8).pack(
                         side="left", padx=10, ipadx=7, ipady=3)
        ctk.CTkLabel(info, text=offer["subtitle"], font=("Arial", 12, "bold"),
                     text_color="#70452D").pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(info, text=offer["description"], font=("Arial", 10),
                     text_color="#8A7B70", anchor="w").pack(anchor="w")
        ctk.CTkLabel(info, text=f"Minimum order: ₹{offer['minimum']:.0f}",
                     font=("Arial", 9), text_color="#A09389").pack(anchor="w", pady=(5, 0))

        ctk.CTkButton(card, text="Apply Offer", width=115, height=38, corner_radius=10,
                      fg_color="#70452D", hover_color="#5A3623", font=("Arial", 10, "bold"),
                      command=lambda o=offer: self.apply_offer(o)).pack(side="right", padx=20)

    def apply_offer(self, offer):
        self.selected_offer = offer
        self.selected_label.configure(text=f"✓ {offer['code']} selected")
        if self.on_apply_offer:
            self.on_apply_offer(offer)
        else:
            messagebox.showinfo("Offer Selected",
                                f"{offer['title']}\n\nCoupon: {offer['code']}\n"
                                f"{offer['subtitle']}\n\nThis offer is selected for checkout.")
