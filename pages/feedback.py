import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime

DB_NAME = "cafe.db"


class FeedbackPage(ctk.CTkFrame):
    def __init__(self, parent, user_id=2):
        super().__init__(parent, fg_color="#F6F1E9")
        self.user_id = user_id
        self.rating = 0
        self.star_buttons = []

        self.build_ui()
        self.load_feedback()

    def db_connect(self):
        return sqlite3.connect(DB_NAME)

    def build_ui(self):
        # ================= HEADER =================
        header = ctk.CTkFrame(
            self,
            fg_color="#3A2418",
            corner_radius=18,
            height=118
        )
        header.pack(fill="x", padx=24, pady=(20, 14))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="💬  Feedback & Rating",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFF8F0"
        ).place(x=25, y=20)

        ctk.CTkLabel(
            header,
            text="Your feedback helps us make every café experience better ☕",
            font=ctk.CTkFont(size=14),
            text_color="#E8D8C8"
        ).place(x=27, y=67)

        # ================= FORM =================
        # No CTkScrollableFrame here.
        # Fixed card prevents the form itself from sliding.
        form = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=18,
            height=345
        )
        form.pack(fill="x", padx=24, pady=(0, 18))
        form.pack_propagate(False)

        ctk.CTkLabel(
            form,
            text="Share Your Experience",
            font=ctk.CTkFont(size=21, weight="bold"),
            text_color="#3A2418"
        ).place(x=24, y=18)

        ctk.CTkLabel(
            form,
            text="How was your experience with Brew & Bytes Café?",
            font=ctk.CTkFont(size=13),
            text_color="#76665A"
        ).place(x=24, y=52)

        # Rating
        ctk.CTkLabel(
            form,
            text="Your Rating",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3A2418"
        ).place(x=24, y=86)

        star_x = 24
        for i in range(1, 6):
            btn = ctk.CTkButton(
                form,
                text="☆",
                width=43,
                height=40,
                corner_radius=10,
                fg_color="#F3E9DE",
                hover_color="#E6D4C2",
                text_color="#B47B1E",
                font=ctk.CTkFont(size=26, weight="bold"),
                command=lambda value=i: self.set_rating(value)
            )
            btn.place(x=star_x, y=112)
            self.star_buttons.append(btn)
            star_x += 50

        self.rating_label = ctk.CTkLabel(
            form,
            text="Select a rating",
            font=ctk.CTkFont(size=12),
            text_color="#8A7A6E"
        )
        self.rating_label.place(x=285, y=124)

        # Feedback
        ctk.CTkLabel(
            form,
            text="Your Feedback",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3A2418"
        ).place(x=24, y=164)

        self.feedback_box = ctk.CTkTextbox(
            form,
            height=88,
            corner_radius=11,
            border_width=1,
            border_color="#E4D6C8",
            fg_color="#FBF8F4",
            text_color="#3A2418",
            font=ctk.CTkFont(size=13)
        )
        self.feedback_box.place(
            x=24,
            y=190,
            relwidth=0.94
        )

        # Buttons
        ctk.CTkButton(
            form,
            text="Clear",
            width=120,
            height=40,
            corner_radius=11,
            fg_color="#EEE5DC",
            hover_color="#DED0C2",
            text_color="#4A392D",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.clear_form
        ).place(x=24, y=292)

        ctk.CTkButton(
            form,
            text="⭐  Submit Feedback",
            width=190,
            height=40,
            corner_radius=11,
            fg_color="#7A4E2D",
            hover_color="#5F3A21",
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.submit_feedback
        ).place(relx=1.0, x=-24, y=292, anchor="ne")

        # ================= PREVIOUS FEEDBACK =================
        previous_header = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=38
        )
        previous_header.pack(fill="x", padx=24, pady=(0, 4))
        previous_header.pack_propagate(False)

        ctk.CTkLabel(
            previous_header,
            text="Your Previous Feedback",
            font=ctk.CTkFont(size=21, weight="bold"),
            text_color="#3A2418"
        ).pack(side="left")

        # Fixed area. No internal scrollbar.
        self.feedback_list = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.feedback_list.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 18)
        )

    def set_rating(self, value):
        self.rating = value

        rating_text = {
            1: "😕 Poor",
            2: "😐 Fair",
            3: "🙂 Good",
            4: "😊 Very Good",
            5: "🤩 Excellent"
        }

        self.rating_label.configure(text=rating_text[value])

        for index, button in enumerate(self.star_buttons, start=1):
            if index <= value:
                button.configure(
                    text="★",
                    fg_color="#F5E3B5",
                    text_color="#B47B1E"
                )
            else:
                button.configure(
                    text="☆",
                    fg_color="#F3E9DE",
                    text_color="#B47B1E"
                )

    def submit_feedback(self):
        feedback_text = self.feedback_box.get("1.0", "end").strip()

        if self.rating == 0:
            messagebox.showwarning(
                "Rating Required",
                "Please select a star rating."
            )
            return

        if not feedback_text:
            messagebox.showwarning(
                "Feedback Required",
                "Please write your feedback."
            )
            return

        try:
            conn = self.db_connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO feedback (user_id, rating, message)
                VALUES (?, ?, ?)
                """,
                (self.user_id, self.rating, feedback_text)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Thank You! ☕",
                "Your feedback has been submitted successfully."
            )

            self.clear_form()
            self.load_feedback()

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Could not save feedback.\n\n{e}"
            )

    def clear_form(self):
        self.rating = 0

        for button in self.star_buttons:
            button.configure(
                text="☆",
                fg_color="#F3E9DE",
                text_color="#B47B1E"
            )

        self.rating_label.configure(text="Select a rating")
        self.feedback_box.delete("1.0", "end")

    def load_feedback(self):
        for widget in self.feedback_list.winfo_children():
            widget.destroy()

        try:
            conn = self.db_connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, rating, message, created_at
                FROM feedback
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (self.user_id,)
            )

            rows = cursor.fetchall()
            conn.close()

        except sqlite3.Error as e:
            error_card = ctk.CTkFrame(
                self.feedback_list,
                fg_color="#FFF1F0",
                corner_radius=14,
                height=65
            )
            error_card.pack(fill="x")
            error_card.pack_propagate(False)

            ctk.CTkLabel(
                error_card,
                text=f"Unable to load feedback: {e}",
                text_color="#B3261E"
            ).pack(anchor="w", padx=16, pady=20)
            return

        if not rows:
            empty = ctk.CTkFrame(
                self.feedback_list,
                fg_color="#FFFFFF",
                corner_radius=15,
                height=82
            )
            empty.pack(fill="x")
            empty.pack_propagate(False)

            ctk.CTkLabel(
                empty,
                text="☕ No feedback yet",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#5A4030"
            ).pack(pady=(17, 1))

            ctk.CTkLabel(
                empty,
                text="Your submitted feedback will appear here.",
                font=ctk.CTkFont(size=11),
                text_color="#8A7A6E"
            ).pack()
            return

        # Show latest feedback cards.
        # If many exist, the dashboard itself can be resized;
        # there is intentionally NO inner sliding scrollbar.
        for feedback_id, rating, message, created_at in rows[:4]:
            self.create_feedback_card(
                feedback_id,
                rating,
                message,
                created_at
            )

    def create_feedback_card(
        self,
        feedback_id,
        rating,
        message,
        created_at
    ):
        card = ctk.CTkFrame(
            self.feedback_list,
            fg_color="#FFFFFF",
            corner_radius=15,
            height=82
        )
        card.pack(fill="x", pady=4)
        card.pack_propagate(False)

        stars = "★" * int(rating) + "☆" * (5 - int(rating))

        ctk.CTkLabel(
            card,
            text=stars,
            font=ctk.CTkFont(size=18),
            text_color="#C58A20"
        ).place(x=18, y=11)

        ctk.CTkLabel(
            card,
            text=self.format_date(created_at),
            font=ctk.CTkFont(size=10),
            text_color="#8A7A6E"
        ).place(relx=1.0, x=-18, y=14, anchor="ne")

        ctk.CTkLabel(
            card,
            text=message or "",
            font=ctk.CTkFont(size=12),
            text_color="#4A392D",
            anchor="w",
            justify="left"
        ).place(x=18, y=44)

    def format_date(self, value):
        if not value:
            return ""

        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d %b %Y • %I:%M %p")
        except ValueError:
            return str(value)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Brew & Bytes Café - Feedback")
    app.geometry("1100x780")
    app.minsize(850, 650)

    page = FeedbackPage(app, user_id=2)
    page.pack(fill="both", expand=True)

    app.mainloop()
