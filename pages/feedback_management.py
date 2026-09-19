import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime


DB_NAME = "cafe.db"


class FeedbackManagement(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F6F1E9")

        self.all_feedback = []
        self.build_ui()
        self.load_feedback()

    def db_connect(self):
        return sqlite3.connect(DB_NAME)

    def build_ui(self):
        # Header
        header = ctk.CTkFrame(
            self,
            fg_color="#3A2418",
            corner_radius=18,
            height=115
        )
        header.pack(fill="x", padx=24, pady=(22, 14))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="💬  Feedback Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFF8F0"
        ).place(x=25, y=20)

        ctk.CTkLabel(
            header,
            text="Review customer ratings and feedback",
            font=ctk.CTkFont(size=14),
            text_color="#E8D8C8"
        ).place(x=27, y=68)

        # Summary cards
        summary = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        summary.pack(fill="x", padx=24, pady=(0, 14))

        self.total_card = self.create_summary_card(
            summary, "💬", "Total Feedback", "0"
        )
        self.total_card.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.rating_card = self.create_summary_card(
            summary, "⭐", "Average Rating", "0.0 / 5"
        )
        self.rating_card.pack(side="left", fill="x", expand=True, padx=8)

        self.five_card = self.create_summary_card(
            summary, "🏆", "5 Star Reviews", "0"
        )
        self.five_card.pack(side="left", fill="x", expand=True, padx=8)

        self.low_card = self.create_summary_card(
            summary, "⚠", "Low Ratings", "0"
        )
        self.low_card.pack(side="left", fill="x", expand=True, padx=(8, 0))

        # Toolbar
        toolbar = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15,
            height=62
        )
        toolbar.pack(fill="x", padx=24, pady=(0, 12))
        toolbar.pack_propagate(False)

        ctk.CTkLabel(
            toolbar,
            text="Filter",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3A2418"
        ).pack(side="left", padx=(18, 8))

        self.filter_combo = ctk.CTkComboBox(
            toolbar,
            values=[
                "All Ratings",
                "5 Stars",
                "4 Stars",
                "3 Stars",
                "2 Stars",
                "1 Star"
            ],
            width=135,
            height=36,
            corner_radius=10,
            border_color="#DCCBBB",
            button_color="#7A4E2D",
            button_hover_color="#5F3A21",
            text_color="#3A2418",
            fg_color="#FBF8F4",
            command=self.apply_filter
        )
        self.filter_combo.set("All Ratings")
        self.filter_combo.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search customer or feedback...",
            width=270,
            height=36,
            corner_radius=10,
            border_color="#DCCBBB",
            fg_color="#FBF8F4"
        )
        self.search_entry.pack(side="left", padx=12)
        self.search_entry.bind("<KeyRelease>", lambda event: self.apply_filter())

        ctk.CTkButton(
            toolbar,
            text="↻ Refresh",
            width=105,
            height=36,
            corner_radius=10,
            fg_color="#7A4E2D",
            hover_color="#5F3A21",
            command=self.load_feedback
        ).pack(side="right", padx=18)

        # Feedback list
        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#9A755A",
            scrollbar_button_hover_color="#7A4E2D"
        )
        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 20)
        )

    def create_summary_card(self, parent, icon, title, value):
        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=15,
            height=92
        )
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=23),
            text_color="#7A4E2D"
        ).place(x=16, y=18)

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color="#8A7A6E"
        ).place(x=55, y=15)

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#3A2418"
        )
        value_label.place(x=55, y=39)

        card.value_label = value_label
        return card

    def load_feedback(self):
        try:
            conn = self.db_connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    f.id,
                    f.user_id,
                    COALESCE(u.name, 'Customer') AS customer_name,
                    COALESCE(u.email, '') AS customer_email,
                    f.rating,
                    f.message,
                    f.created_at
                FROM feedback f
                LEFT JOIN users u ON u.id = f.user_id
                ORDER BY f.id DESC
                """
            )

            self.all_feedback = cursor.fetchall()
            conn.close()

            self.update_summary()
            self.apply_filter()

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Could not load feedback.\n\n{e}"
            )

    def update_summary(self):
        total = len(self.all_feedback)

        ratings = [
            int(row[4])
            for row in self.all_feedback
            if row[4] is not None
        ]

        average = sum(ratings) / len(ratings) if ratings else 0
        five_star = sum(1 for r in ratings if r == 5)
        low_rating = sum(1 for r in ratings if r <= 2)

        self.total_card.value_label.configure(text=str(total))
        self.rating_card.value_label.configure(
            text=f"{average:.1f} / 5"
        )
        self.five_card.value_label.configure(text=str(five_star))
        self.low_card.value_label.configure(text=str(low_rating))

    def apply_filter(self, _value=None):
        selected = self.filter_combo.get()
        search = self.search_entry.get().strip().lower()

        filtered = []

        rating_map = {
            "5 Stars": 5,
            "4 Stars": 4,
            "3 Stars": 3,
            "2 Stars": 2,
            "1 Star": 1
        }

        selected_rating = rating_map.get(selected)

        for row in self.all_feedback:
            customer_name = str(row[2] or "").lower()
            customer_email = str(row[3] or "").lower()
            message = str(row[5] or "").lower()
            rating = int(row[4] or 0)

            if selected_rating is not None and rating != selected_rating:
                continue

            if search:
                if (
                    search not in customer_name
                    and search not in customer_email
                    and search not in message
                ):
                    continue

            filtered.append(row)

        self.render_feedback(filtered)

    def render_feedback(self, rows):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not rows:
            empty = ctk.CTkFrame(
                self.list_frame,
                fg_color="#FFFFFF",
                corner_radius=16,
                height=110
            )
            empty.pack(fill="x", pady=5)
            empty.pack_propagate(False)

            ctk.CTkLabel(
                empty,
                text="☕ No feedback found",
                font=ctk.CTkFont(size=17, weight="bold"),
                text_color="#5A4030"
            ).pack(pady=(28, 2))

            ctk.CTkLabel(
                empty,
                text="Try another rating or search term.",
                font=ctk.CTkFont(size=12),
                text_color="#8A7A6E"
            ).pack()

            return

        for row in rows:
            self.create_feedback_card(row)

    def create_feedback_card(self, row):
        feedback_id, user_id, customer_name, email, rating, message, created_at = row

        card = ctk.CTkFrame(
            self.list_frame,
            fg_color="#FFFFFF",
            corner_radius=16
        )
        card.pack(fill="x", pady=6)

        # Left rating block
        rating_block = ctk.CTkFrame(
            card,
            fg_color="#FBF8F4",
            corner_radius=12,
            width=105,
            height=92
        )
        rating_block.pack(side="left", padx=14, pady=14)
        rating_block.pack_propagate(False)

        ctk.CTkLabel(
            rating_block,
            text=f"{int(rating or 0)} / 5",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#7A4E2D"
        ).pack(pady=(14, 0))

        stars = "★" * int(rating or 0) + "☆" * (5 - int(rating or 0))

        ctk.CTkLabel(
            rating_block,
            text=stars,
            font=ctk.CTkFont(size=13),
            text_color="#C58A20"
        ).pack()

        # Main content
        body = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        body.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(2, 10),
            pady=13
        )

        top = ctk.CTkFrame(
            body,
            fg_color="transparent"
        )
        top.pack(fill="x")

        ctk.CTkLabel(
            top,
            text=f"👤 {customer_name}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3A2418"
        ).pack(side="left")

        date_text = self.format_date(created_at)

        ctk.CTkLabel(
            top,
            text=date_text,
            font=ctk.CTkFont(size=10),
            text_color="#8A7A6E"
        ).pack(side="right")

        if email:
            ctk.CTkLabel(
                body,
                text=email,
                font=ctk.CTkFont(size=10),
                text_color="#8A7A6E"
            ).pack(anchor="w", pady=(1, 3))

        ctk.CTkLabel(
            body,
            text=message or "No message",
            font=ctk.CTkFont(size=12),
            text_color="#4A392D",
            anchor="w",
            justify="left",
            wraplength=650
        ).pack(fill="x", pady=(2, 4))

        # Delete
        ctk.CTkButton(
            card,
            text="🗑",
            width=42,
            height=38,
            corner_radius=10,
            fg_color="#F6E3DF",
            hover_color="#EAC8C1",
            text_color="#A33A2B",
            font=ctk.CTkFont(size=16),
            command=lambda fid=feedback_id: self.delete_feedback(fid)
        ).pack(side="right", padx=15, pady=15)

    def delete_feedback(self, feedback_id):
        confirm = messagebox.askyesno(
            "Delete Feedback",
            "Are you sure you want to delete this feedback?"
        )

        if not confirm:
            return

        try:
            conn = self.db_connect()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM feedback WHERE id = ?",
                (feedback_id,)
            )

            conn.commit()
            conn.close()

            self.load_feedback()

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Could not delete feedback.\n\n{e}"
            )

    def format_date(self, value):
        if not value:
            return ""

        try:
            dt = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S"
            )
            return dt.strftime(
                "%d %b %Y • %I:%M %p"
            )
        except ValueError:
            return str(value)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Brew & Bytes Café - Feedback Management")
    app.geometry("1200x800")
    app.minsize(950, 650)

    page = FeedbackManagement(app)
    page.pack(fill="both", expand=True)

    app.mainloop()
