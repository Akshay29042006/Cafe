import customtkinter as ctk
from tkinter import messagebox
import sqlite3

DB_NAME = "cafe.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def ensure_favorites_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            menu_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, menu_id)
        )
        """
    )

    conn.commit()
    conn.close()


def is_favorite(user_id, menu_id):
    ensure_favorites_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM favorites
        WHERE user_id = ? AND menu_id = ?
        LIMIT 1
        """,
        (user_id, menu_id)
    )

    result = cursor.fetchone()
    conn.close()

    return result is not None


def toggle_favorite(user_id, menu_id):
    ensure_favorites_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM favorites
        WHERE user_id = ? AND menu_id = ?
        """,
        (user_id, menu_id)
    )

    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            "DELETE FROM favorites WHERE id = ?",
            (existing[0],)
        )
        saved = False
    else:
        cursor.execute(
            """
            INSERT INTO favorites (user_id, menu_id)
            VALUES (?, ?)
            """,
            (user_id, menu_id)
        )
        saved = True

    conn.commit()
    conn.close()

    return saved


def get_favorite_items(user_id):
    ensure_favorites_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            m.id,
            m.name,
            m.category,
            m.price,
            m.description,
            m.image,
            m.available
        FROM favorites f
        INNER JOIN menu m ON m.id = f.menu_id
        WHERE f.user_id = ?
        ORDER BY f.id DESC
        """,
        (user_id,)
    )

    items = cursor.fetchall()
    conn.close()

    return items


class FavoritesPage(ctk.CTkFrame):
    def __init__(self, parent, user_id=2, on_add_to_cart=None):
        super().__init__(parent, fg_color="#F6F1E9")

        self.user_id = user_id
        self.on_add_to_cart = on_add_to_cart

        ensure_favorites_table()

        self.build_ui()
        self.load_favorites()

    def build_ui(self):
        header = ctk.CTkFrame(
            self,
            fg_color="#3A2418",
            corner_radius=18,
            height=118
        )
        header.pack(fill="x", padx=24, pady=(20, 15))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="♥  My Favorites",
            font=ctk.CTkFont(size=29, weight="bold"),
            text_color="#FFF8F0"
        ).place(x=25, y=20)

        ctk.CTkLabel(
            header,
            text="Your favorite café items, all in one place ☕",
            font=ctk.CTkFont(size=14),
            text_color="#E8D8C8"
        ).place(x=27, y=68)

        self.count_label = ctk.CTkLabel(
            header,
            text="0 items",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#F3B562"
        )
        self.count_label.place(relx=1.0, x=-28, y=24, anchor="ne")

        # Fixed favorites area — no internal scrollbar
        self.list_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 20)
        )

    def load_favorites(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        items = get_favorite_items(self.user_id)

        self.count_label.configure(
            text=f"{len(items)} item" + ("" if len(items) == 1 else "s")
        )

        if not items:
            empty = ctk.CTkFrame(
                self.list_frame,
                fg_color="#FFFFFF",
                corner_radius=18,
                height=170
            )
            empty.pack(fill="x", pady=10)
            empty.pack_propagate(False)

            ctk.CTkLabel(
                empty,
                text="♡",
                font=ctk.CTkFont(size=42),
                text_color="#C58A20"
            ).pack(pady=(22, 0))

            ctk.CTkLabel(
                empty,
                text="No Favorites Yet",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#3A2418"
            ).pack(pady=(0, 3))

            ctk.CTkLabel(
                empty,
                text="Tap ♥ on any menu item to save it here.",
                font=ctk.CTkFont(size=12),
                text_color="#8A7A6E"
            ).pack()

            return

        grid = ctk.CTkFrame(
            self.list_frame,
            fg_color="transparent"
        )
        grid.pack(fill="x")

        # Show up to 6 favorites in the fixed dashboard area.
        # No internal scrolling is used.
        for index, item in enumerate(items[:6]):
            row = index // 3
            column = index % 3

            card = self.create_card(grid, item)
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

        if len(items) > 6:
            ctk.CTkLabel(
                self.list_frame,
                text=f"+ {len(items) - 6} more favorites — remove some favorites to view them here.",
                font=ctk.CTkFont(size=11),
                text_color="#8A7A6E"
            ).pack(pady=(6, 0))

    def create_card(self, parent, item):
        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=16,
            height=255
        )
        card.pack_propagate(False)

        image_box = ctk.CTkFrame(
            card,
            height=92,
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
            font=ctk.CTkFont(size=42)
        ).pack(expand=True)

        ctk.CTkLabel(
            card,
            text=item[1],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=14
        )

        ctk.CTkLabel(
            card,
            text=item[4] or "Freshly prepared for you",
            font=ctk.CTkFont(size=9),
            text_color="#8A7B70",
            anchor="w"
        ).pack(
            anchor="w",
            padx=14,
            pady=(3, 2)
        )

        bottom = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        bottom.pack(
            fill="x",
            padx=12,
            pady=(4, 8)
        )

        ctk.CTkLabel(
            bottom,
            text=f"₹{item[3]:.0f}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#6B4029"
        ).pack(side="left")

        ctk.CTkButton(
            bottom,
            text="♥",
            width=36,
            height=30,
            corner_radius=8,
            fg_color="#F7E1E1",
            hover_color="#EFC7C7",
            text_color="#B3261E",
            font=ctk.CTkFont(size=17),
            command=lambda mid=item[0]: self.remove_favorite(mid)
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            bottom,
            text="+ Add",
            width=72,
            height=30,
            corner_radius=8,
            fg_color="#3B2417",
            hover_color="#5A3823",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda i=item: self.add_to_cart(i)
        ).pack(side="right")

        return card

    def remove_favorite(self, menu_id):
        toggle_favorite(self.user_id, menu_id)
        self.load_favorites()

    def add_to_cart(self, item):
        if self.on_add_to_cart:
            self.on_add_to_cart(item)
        else:
            messagebox.showinfo(
                "Added to Cart",
                f"{item[1]} added to your cart!"
            )


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Brew & Bytes Café - My Favorites")
    app.geometry("1100x780")
    app.minsize(850, 650)

    page = FavoritesPage(app, user_id=2)
    page.pack(fill="both", expand=True)

    app.mainloop()
