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
    count = cursor.fetchone()[0]

    if count == 0:
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


def get_all_offers():
    ensure_offers_table()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, title, subtitle, code, discount_type,
               discount_value, minimum_order, status, color, icon
        FROM offers
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    connection.close()
    return rows


class OffersManagement(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F6F1E9")
        ensure_offers_table()
        self.build_ui()

    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color="#3A2418", corner_radius=18, height=105)
        header.pack(fill="x", padx=24, pady=(18, 12))
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="🎁  Offers Management",
                     font=ctk.CTkFont(size=29, weight="bold"),
                     text_color="#FFF8F0").place(x=25, y=20)
        ctk.CTkLabel(header, text="Manage café offers, coupon codes and discounts",
                     font=ctk.CTkFont(size=14), text_color="#E8D8C8").place(x=27, y=61)

        summary = ctk.CTkFrame(self, fg_color="transparent")
        summary.pack(fill="x", padx=24, pady=(0, 10))

        self.total_card = self.create_summary_card(summary, "🎁", "Total Offers", "0")
        self.total_card.pack(side="left", fill="x", expand=True, padx=(0, 7))
        self.active_card = self.create_summary_card(summary, "✓", "Active Offers", "0")
        self.active_card.pack(side="left", fill="x", expand=True, padx=7)
        self.discount_card = self.create_summary_card(summary, "%", "Discount Offers", "0")
        self.discount_card.pack(side="left", fill="x", expand=True, padx=7)
        self.flat_card = self.create_summary_card(summary, "₹", "Flat Discount", "0")
        self.flat_card.pack(side="left", fill="x", expand=True, padx=(7, 0))

        action = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15, height=55)
        action.pack(fill="x", padx=24, pady=(0, 10))
        action.pack_propagate(False)

        ctk.CTkLabel(action, text="Manage your promotional offers",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#4A392D").pack(side="left", padx=18)

        ctk.CTkButton(action, text="+  Add New Offer", width=145, height=34,
                      corner_radius=10, fg_color="#7A4E2D", hover_color="#5F3A21",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=self.add_offer).pack(side="right", padx=18)

        self.cards_area = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_area.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self.render_offers()

    def create_summary_card(self, parent, icon, title, value):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15, height=72)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=20),
                     text_color="#7A4E2D").place(x=16, y=12)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=10),
                     text_color="#8A7A6E").place(x=55, y=10)
        value_label = ctk.CTkLabel(card, text=value,
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color="#3A2418")
        value_label.place(x=55, y=31)
        card.value_label = value_label
        return card

    def render_offers(self):
        for widget in self.cards_area.winfo_children():
            widget.destroy()

        offers = get_all_offers()
        grid = ctk.CTkFrame(self.cards_area, fg_color="transparent")
        grid.pack(fill="x")

        if not offers:
            ctk.CTkLabel(grid, text="No offers available.",
                         font=ctk.CTkFont(size=14), text_color="#806F63").pack(pady=40)
        else:
            # Three columns keep all offers visible without an internal scrollbar.
            for index, offer in enumerate(offers):
                card = self.create_offer_card(grid, offer)
                card.grid(row=index // 3, column=index % 3,
                          padx=6, pady=6, sticky="nsew")

        for column in range(3):
            grid.grid_columnconfigure(column, weight=1)
        self.update_summary(offers)

    def create_offer_card(self, parent, offer):
        offer_id, title, subtitle, code, discount_type, discount_value, minimum, status, color, icon = offer
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=16, height=172)
        card.pack_propagate(False)

        ctk.CTkFrame(card, fg_color=color, corner_radius=10, width=7).place(x=0, y=0, relheight=1)
        ctk.CTkLabel(card, text=icon or "🎁", font=ctk.CTkFont(size=24)).place(x=20, y=14)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=17, weight="bold"),
                     text_color="#3A2418").place(x=58, y=14)

        status_color = "#2E7D32" if status == "Active" else "#9A633F"
        status_bg = "#E5F4E7" if status == "Active" else "#F3E6DB"
        ctk.CTkLabel(card, text=status, font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=status_color, fg_color=status_bg,
                     corner_radius=8, padx=8, pady=3).place(relx=1, x=-12, y=14, anchor="ne")

        ctk.CTkLabel(card, text=subtitle or "", font=ctk.CTkFont(size=12),
                     text_color="#76665A").place(x=58, y=42)

        coupon = ctk.CTkFrame(card, fg_color="#FBF5EF", corner_radius=10, height=38)
        coupon.place(x=18, y=70, relwidth=0.91)
        coupon.pack_propagate(False)
        ctk.CTkLabel(coupon, text="COUPON", font=ctk.CTkFont(size=9, weight="bold"),
                     text_color="#8A7A6E").pack(side="left", padx=(12, 8))
        ctk.CTkLabel(coupon, text=code, font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#7A4E2D").pack(side="left")

        discount_text = f"₹{discount_value:.0f}" if discount_type == "flat" else f"{discount_value:.0f}%"
        ctk.CTkLabel(card,
                     text=f"Discount: {discount_text}    •    Minimum Order: ₹{minimum:.0f}",
                     font=ctk.CTkFont(size=11), text_color="#5F5148").place(x=18, y=123)

        ctk.CTkButton(card, text="Edit", width=72, height=30, corner_radius=8,
                      fg_color="#EEE5DC", hover_color="#DED0C2", text_color="#4A392D",
                      font=ctk.CTkFont(size=9, weight="bold"),
                      command=lambda i=offer_id: self.edit_offer(i)).place(x=18, y=142)
        ctk.CTkButton(card, text="Delete", width=72, height=30, corner_radius=8,
                      fg_color="#F6E3DF", hover_color="#EAC8C1", text_color="#A33A2B",
                      font=ctk.CTkFont(size=9, weight="bold"),
                      command=lambda i=offer_id, n=title: self.delete_offer(i, n)).place(x=99, y=142)
        return card

    def add_offer(self):
        self.offer_form()

    def edit_offer(self, offer_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id,title,subtitle,code,discount_type,discount_value,minimum_order,status,color,icon FROM offers WHERE id=?", (offer_id,))
        current = cursor.fetchone()
        connection.close()
        if current:
            self.offer_form(current)

    def offer_form(self, current=None):
        editing = current is not None
        window = ctk.CTkToplevel(self)
        window.title("Edit Offer" if editing else "Add New Offer")
        window.geometry("520x760")
        window.minsize(520, 760)
        window.resizable(False, False)
        window.transient(self.winfo_toplevel())
        window.grab_set()

        ctk.CTkLabel(window, text="Edit Offer" if editing else "Add New Offer",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color="#3A2418").pack(pady=(25, 16))

        fields = {}
        labels = [
            ("Offer Title", "title"),
            ("Subtitle", "subtitle"),
            ("Coupon Code", "code"),
            ("Discount Value", "discount_value"),
            ("Minimum Order", "minimum_order")
        ]
        for label, key in labels:
            ctk.CTkLabel(window, text=label, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#4A392D").pack(anchor="w", padx=30, pady=(5, 4))
            entry = ctk.CTkEntry(window, width=460, height=40, corner_radius=10,
                                 border_color="#DCCBBB")
            entry.pack(padx=30)
            fields[key] = entry

        if editing:
            _, title, subtitle, code, dtype, dvalue, minimum, status_value, color, icon = current
            values = {"title": title, "subtitle": subtitle, "code": code,
                      "discount_value": str(int(dvalue) if float(dvalue).is_integer() else dvalue),
                      "minimum_order": str(int(minimum) if float(minimum).is_integer() else minimum)}
            for key, value in values.items():
                fields[key].insert(0, value)

        ctk.CTkLabel(window, text="Discount Type", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#4A392D").pack(anchor="w", padx=30, pady=(9, 4))
        dtype = ctk.CTkComboBox(window, values=["Percentage", "Flat Amount"], width=460, height=40,
                                corner_radius=10)
        dtype.pack(padx=30)
        dtype.set("Flat Amount" if editing and current[4] == "flat" else "Percentage")

        ctk.CTkLabel(window, text="Status", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#4A392D").pack(anchor="w", padx=30, pady=(9, 4))
        status = ctk.CTkComboBox(window, values=["Active", "Inactive"], width=460, height=40,
                                 corner_radius=10)
        status.pack(padx=30)
        status.set(current[7] if editing else "Active")

        def save():
            title = fields["title"].get().strip()
            subtitle = fields["subtitle"].get().strip()
            code = fields["code"].get().strip().upper()
            discount_text = fields["discount_value"].get().strip().replace("₹", "").replace("%", "")
            minimum_text = fields["minimum_order"].get().strip().replace("₹", "")

            if not title or not code or not discount_text or not minimum_text:
                messagebox.showwarning("Required Fields", "Please fill all required fields.", parent=window)
                return

            try:
                discount_value = float(discount_text)
                minimum_order = float(minimum_text)
            except ValueError:
                messagebox.showerror("Invalid Value", "Discount and Minimum Order must be numbers.", parent=window)
                return

            selected_type = "flat" if dtype.get() == "Flat Amount" else "percent"
            if discount_value <= 0 or minimum_order < 0:
                messagebox.showwarning("Invalid Value", "Discount must be greater than 0 and minimum order cannot be negative.", parent=window)
                return
            if selected_type == "percent" and discount_value > 100:
                messagebox.showwarning("Invalid Percentage", "Percentage discount cannot be more than 100%.", parent=window)
                return

            connection = get_connection()
            cursor = connection.cursor()
            try:
                if editing:
                    cursor.execute("""
                        UPDATE offers SET title=?, subtitle=?, code=?, discount_type=?,
                        discount_value=?, minimum_order=?, status=? WHERE id=?
                    """, (title, subtitle, code, selected_type, discount_value,
                          minimum_order, status.get(), current[0]))
                    success_text = "Offer updated successfully!"
                else:
                    cursor.execute("""
                        INSERT INTO offers
                        (title, subtitle, code, discount_type, discount_value,
                         minimum_order, status, color, icon)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (title, subtitle, code, selected_type, discount_value,
                          minimum_order, status.get(), "#7A4E2D", "🎁"))
                    success_text = "Offer added successfully!"
                connection.commit()
            except sqlite3.IntegrityError:
                connection.rollback()
                connection.close()
                messagebox.showerror("Duplicate Coupon", "This coupon code already exists.", parent=window)
                return
            except Exception as error:
                connection.rollback()
                connection.close()
                messagebox.showerror("Save Error", f"Could not save offer.\n\n{error}", parent=window)
                return
            connection.close()

            window.destroy()
            self.render_offers()
            messagebox.showinfo("Success", success_text, parent=self.winfo_toplevel())

        ctk.CTkButton(window, text="✓  Save Offer", width=460, height=46, corner_radius=11,
                      fg_color="#7A4E2D", hover_color="#5F3A21",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=save).pack(padx=30, pady=(18, 8))
        ctk.CTkButton(window, text="Cancel", width=460, height=38, corner_radius=10,
                      fg_color="#EEE5DC", hover_color="#DED0C2", text_color="#4A392D",
                      command=window.destroy).pack(padx=30)

    def delete_offer(self, offer_id, title):
        if not messagebox.askyesno("Delete Offer", f"Delete '{title}'?", parent=self):
            return
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM offers WHERE id=?", (offer_id,))
        connection.commit()
        connection.close()
        self.render_offers()

    def update_summary(self, offers=None):
        if offers is None:
            offers = get_all_offers()
        total = len(offers)
        active = sum(1 for x in offers if x[7] == "Active")
        percentage = sum(1 for x in offers if x[4] == "percent")
        flat = sum(1 for x in offers if x[4] == "flat")
        self.total_card.value_label.configure(text=str(total))
        self.active_card.value_label.configure(text=str(active))
        self.discount_card.value_label.configure(text=str(percentage))
        self.flat_card.value_label.configure(text=str(flat))


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Brew & Bytes Café - Offers Management")
    app.geometry("1250x800")
    app.minsize(1050, 650)
    page = OffersManagement(app)
    page.pack(fill="both", expand=True)
    app.mainloop()
