import os
import shutil
import sqlite3
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

from database import get_connection


class SettingsManagement(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.parent_window = parent
        self.admin_id = None

        self.ensure_settings_table()
        self.load_admin()

        self.create_header()
        self.create_content()

        self.load_all_data()

    # =====================================================
    # SETTINGS TABLE
    # =====================================================

    def ensure_settings_table(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cafe_settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        defaults = {
            "cafe_name": "Brew & Bytes Café",
            "contact_number": "",
            "cafe_email": "",
            "address": "",
            "opening_hours": "09:00 AM - 10:00 PM",
            "currency": "₹",
            "appearance": "Light"
        }

        for key, value in defaults.items():

            cursor.execute(
                """
                INSERT OR IGNORE INTO cafe_settings
                (key, value)
                VALUES (?, ?)
                """,
                (key, value)
            )

        connection.commit()
        connection.close()

    # =====================================================
    # SETTINGS HELPERS
    # =====================================================

    def get_setting(self, key, default=""):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT value
            FROM cafe_settings
            WHERE key = ?
            """,
            (key,)
        )

        row = cursor.fetchone()

        connection.close()

        if row and row[0] is not None:
            return row[0]

        return default

    def save_setting(self, key, value):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO cafe_settings
            (key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
            """,
            (key, value)
        )

        connection.commit()
        connection.close()

    # =====================================================
    # FIND ADMIN
    # =====================================================

    def load_admin(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                role,
                created_at
            FROM users
            WHERE role = 'Admin'
            ORDER BY id
            LIMIT 1
        """)

        self.admin = cursor.fetchone()

        connection.close()

        if self.admin:
            self.admin_id = self.admin[0]

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            height=115,
            fg_color="#F6F1E9",
            corner_radius=0
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(22, 8)
        )

        header.pack_propagate(False)

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            left,
            text="⚙  Settings",
            font=("Arial", 28, "bold"),
            text_color="#2F1B12"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        ctk.CTkLabel(
            left,
            text="Manage your café administration settings",
            font=("Arial", 12),
            text_color="#897A70"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=155,
            height=48,
            corner_radius=12,
            fg_color="#3A2116",
            hover_color="#553222",
            text_color="white",
            font=("Arial", 12, "bold"),
            command=self.load_all_data
        ).pack(
            side="right",
            pady=8
        )

    # =====================================================
    # MAIN CONTENT
    # =====================================================

    def create_content(self):

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#B98A68",
            scrollbar_button_hover_color="#7A4E2D",
            corner_radius=0
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 22)
        )

        self.content.grid_columnconfigure(
            0,
            weight=0,
            minsize=300
        )

        self.content.grid_columnconfigure(
            1,
            weight=1
        )

        # -------------------------------------------------
        # LEFT TOP - ADMIN PROFILE
        # -------------------------------------------------

        self.profile_card = self.create_card(
            self.content,
            0,
            0
        )

        # -------------------------------------------------
        # LEFT BOTTOM - PASSWORD
        # -------------------------------------------------

        self.password_card = self.create_card(
            self.content,
            0,
            1
        )

        # -------------------------------------------------
        # RIGHT TOP - CAFE INFORMATION
        # -------------------------------------------------

        self.cafe_card = self.create_card(
            self.content,
            1,
            0
        )

        # -------------------------------------------------
        # RIGHT BOTTOM - DATABASE
        # -------------------------------------------------

        self.database_card = self.create_card(
            self.content,
            1,
            1
        )

        self.build_profile_card()
        self.build_password_card()
        self.build_cafe_card()
        self.build_database_card()

    # =====================================================
    # CARD
    # =====================================================

    def create_card(self, parent, column, row):

        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=18,
            border_width=1,
            border_color="#E9DED2"
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=(0, 7) if column == 0 else (7, 0),
            pady=(0, 7) if row == 0 else (7, 0)
        )

        return card

    # =====================================================
    # CARD TITLE
    # =====================================================

    def card_title(self, parent, icon, title, subtitle):

        ctk.CTkLabel(
            parent,
            text=f"{icon}  {title}",
            font=("Arial", 20, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=24,
            pady=(15, 2)
        )

        ctk.CTkLabel(
            parent,
            text=subtitle,
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 8)
        )

    # =====================================================
    # INPUT
    # =====================================================

    def create_input(
        self,
        parent,
        label,
        show=None,
        height=36
    ):

        ctk.CTkLabel(
            parent,
            text=label,
            font=("Arial", 11, "bold"),
            text_color="#4D3A2F"
        ).pack(
            anchor="w",
            padx=24,
            pady=(4, 3)
        )

        entry = ctk.CTkEntry(
            parent,
            height=height,
            corner_radius=10,
            border_width=1,
            border_color="#D8C5B5",
            fg_color="#FBF8F4",
            text_color="#302017",
            font=("Arial", 12),
            show=show
        )

        entry.pack(
            fill="x",
            padx=24,
            pady=(0, 2)
        )

        return entry

    # =====================================================
    # PROFILE
    # =====================================================

    def build_profile_card(self):

        self.card_title(
            self.profile_card,
            "👤",
            "Admin Profile",
            "Update the administrator account information"
        )

        self.admin_name_entry = self.create_input(
            self.profile_card,
            "Name"
        )

        self.admin_email_entry = self.create_input(
            self.profile_card,
            "Email"
        )

        if self.admin:
            self.admin_role_label = ctk.CTkLabel(
                self.profile_card,
                text=f"Role: {self.admin[3]}",
                font=("Arial", 10),
                text_color="#897A70"
            )
            self.admin_role_label.pack(
                anchor="w",
                padx=24,
                pady=(4, 6)
            )

        ctk.CTkButton(
            self.profile_card,
            text="Save Profile",
            height=36,
            corner_radius=10,
            fg_color="#7A4E2D",
            hover_color="#5F3A21",
            text_color="white",
            font=("Arial", 12, "bold"),
            command=self.save_profile
        ).pack(
            fill="x",
            padx=24,
            pady=(7, 20)
        )

    # =====================================================
    # PASSWORD
    # =====================================================

    def build_password_card(self):

        self.card_title(
            self.password_card,
            "🔐",
            "Change Password",
            "Change the admin login password"
        )

        self.current_password_entry = self.create_input(
            self.password_card,
            "Current Password",
            show="•"
        )

        self.new_password_entry = self.create_input(
            self.password_card,
            "New Password",
            show="•"
        )

        self.confirm_password_entry = self.create_input(
            self.password_card,
            "Confirm New Password",
            show="•"
        )

        ctk.CTkButton(
            self.password_card,
            text="Update Password",
            height=36,
            corner_radius=10,
            fg_color="#7A4E2D",
            hover_color="#5F3A21",
            text_color="white",
            font=("Arial", 12, "bold"),
            command=self.change_password
        ).pack(
            fill="x",
            padx=24,
            pady=(5, 5)
        )

        ctk.CTkLabel(
            self.password_card,
            text="Use at least 6 characters.",
            font=("Arial", 10),
            text_color="#897A70"
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 8)
        )

    # =====================================================
    # CAFE INFORMATION
    # =====================================================

    def build_cafe_card(self):

        self.card_title(
            self.cafe_card,
            "☕",
            "Café Information",
            "Basic information displayed for your café"
        )

        self.cafe_name_entry = self.create_input(
            self.cafe_card,
            "Café Name"
        )

        self.contact_entry = self.create_input(
            self.cafe_card,
            "Contact Number"
        )

        self.cafe_email_entry = self.create_input(
            self.cafe_card,
            "Café Email"
        )

        ctk.CTkLabel(
            self.cafe_card,
            text="Address",
            font=("Arial", 11, "bold"),
            text_color="#4D3A2F"
        ).pack(
            anchor="w",
            padx=24,
            pady=(4, 3)
        )

        self.address_text = ctk.CTkTextbox(
            self.cafe_card,
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#D8C5B5",
            fg_color="#FBF8F4",
            text_color="#302017",
            font=("Arial", 12)
        )

        self.address_text.pack(
            fill="x",
            padx=24,
            pady=(0, 3)
        )

        bottom_row = ctk.CTkFrame(
            self.cafe_card,
            fg_color="transparent"
        )

        bottom_row.pack(
            fill="x",
            padx=24,
            pady=(2, 0)
        )

        left = ctk.CTkFrame(
            bottom_row,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6)
        )

        ctk.CTkLabel(
            left,
            text="Opening Hours",
            font=("Arial", 11, "bold"),
            text_color="#4D3A2F"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.opening_entry = ctk.CTkEntry(
            left,
            height=40,
            corner_radius=10,
            border_width=1,
            border_color="#D8C5B5",
            fg_color="#FBF8F4",
            font=("Arial", 11)
        )

        self.opening_entry.pack(
            fill="x"
        )

        right = ctk.CTkFrame(
            bottom_row,
            fg_color="transparent",
            width=100
        )

        right.pack(
            side="right",
            fill="y",
            padx=(6, 0)
        )

        ctk.CTkLabel(
            right,
            text="Currency",
            font=("Arial", 11, "bold"),
            text_color="#4D3A2F"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.currency_combo = ctk.CTkComboBox(
            right,
            values=["₹", "$", "€", "£"],
            height=40,
            width=95,
            corner_radius=10,
            border_width=1,
            border_color="#D8C5B5",
            fg_color="#FBF8F4",
            button_color="#7A4E2D",
            button_hover_color="#5F3A21",
            font=("Arial", 11)
        )

        self.currency_combo.pack()

        ctk.CTkButton(
            self.cafe_card,
            text="Save Café Information",
            height=36,
            corner_radius=10,
            fg_color="#7A4E2D",
            hover_color="#5F3A21",
            text_color="white",
            font=("Arial", 12, "bold"),
            command=self.save_cafe_information
        ).pack(
            fill="x",
            padx=24,
            pady=(7, 12)
        )

    # =====================================================
    # DATABASE
    # =====================================================

    def build_database_card(self):

        self.card_title(
            self.database_card,
            "🗄",
            "Database Information",
            "Current café database summary"
        )

        self.db_status = ctk.CTkLabel(
            self.database_card,
            text="●  Connected",
            height=42,
            corner_radius=10,
            fg_color="#E5F3E9",
            text_color="#2E7D4F",
            font=("Arial", 12, "bold")
        )

        self.db_status.pack(
            fill="x",
            padx=24,
            pady=(0, 12)
        )

        self.db_counts_label = ctk.CTkLabel(
            self.database_card,
            text="",
            justify="left",
            anchor="w",
            font=("Arial", 11),
            text_color="#5E5148"
        )

        self.db_counts_label.pack(
            fill="x",
            padx=24,
            pady=3
        )

        self.db_path_label = ctk.CTkLabel(
            self.database_card,
            text="",
            justify="left",
            anchor="w",
            wraplength=600,
            font=("Arial", 10),
            text_color="#897A70"
        )

        self.db_path_label.pack(
            fill="x",
            padx=24,
            pady=(8, 4)
        )

        buttons = ctk.CTkFrame(
            self.database_card,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=24,
            pady=(5, 10)
        )

        ctk.CTkButton(
            buttons,
            text="↻  Refresh Database Info",
            height=36,
            corner_radius=10,
            fg_color="#3A2116",
            hover_color="#553222",
            text_color="white",
            font=("Arial", 11, "bold"),
            command=self.refresh_database_info
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6)
        )

        ctk.CTkButton(
            buttons,
            text="Backup Database",
            height=36,
            corner_radius=10,
            fg_color="#E9DED2",
            hover_color="#DCCABB",
            text_color="#4A2B1E",
            font=("Arial", 11, "bold"),
            command=self.backup_database
        ).pack(
            side="right",
            fill="x",
            expand=True,
            padx=(6, 0)
        )

    # =====================================================
    # LOAD ALL
    # =====================================================

    def load_all_data(self):

        self.load_admin()

        if self.admin:
            self.admin_name_entry.delete(0, "end")
            self.admin_name_entry.insert(0, self.admin[1])

            self.admin_email_entry.delete(0, "end")
            self.admin_email_entry.insert(0, self.admin[2])

        self.cafe_name_entry.delete(0, "end")
        self.cafe_name_entry.insert(
            0,
            self.get_setting(
                "cafe_name",
                "Brew & Bytes Café"
            )
        )

        self.contact_entry.delete(0, "end")
        self.contact_entry.insert(
            0,
            self.get_setting("contact_number")
        )

        self.cafe_email_entry.delete(0, "end")
        self.cafe_email_entry.insert(
            0,
            self.get_setting("cafe_email")
        )

        self.address_text.delete("1.0", "end")
        self.address_text.insert(
            "1.0",
            self.get_setting("address")
        )

        self.opening_entry.delete(0, "end")
        self.opening_entry.insert(
            0,
            self.get_setting(
                "opening_hours",
                "09:00 AM - 10:00 PM"
            )
        )

        self.currency_combo.set(
            self.get_setting(
                "currency",
                "₹"
            )
        )

        self.refresh_database_info()

    # =====================================================
    # SAVE PROFILE
    # =====================================================

    def save_profile(self):

        if not self.admin_id:
            messagebox.showerror(
                "Error",
                "Admin account not found.",
                parent=self.winfo_toplevel()
            )
            return

        name = self.admin_name_entry.get().strip()
        email = self.admin_email_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Name",
                "Please enter admin name.",
                parent=self.winfo_toplevel()
            )
            return

        if not email or "@" not in email:
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address.",
                parent=self.winfo_toplevel()
            )
            return

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE users
                SET name = ?, email = ?
                WHERE id = ?
                """,
                (name, email, self.admin_id)
            )

            connection.commit()

            messagebox.showinfo(
                "Saved",
                "Admin profile updated successfully!",
                parent=self.winfo_toplevel()
            )

            self.load_admin()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Email Already Exists",
                "This email is already used by another account.",
                parent=self.winfo_toplevel()
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not save profile:\n{e}",
                parent=self.winfo_toplevel()
            )

        finally:
            connection.close()

    # =====================================================
    # CHANGE PASSWORD
    # =====================================================

    def change_password(self):

        if not self.admin_id:
            messagebox.showerror(
                "Error",
                "Admin account not found.",
                parent=self.winfo_toplevel()
            )
            return

        current = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm = self.confirm_password_entry.get()

        if not current:
            messagebox.showwarning(
                "Missing Password",
                "Please enter current password.",
                parent=self.winfo_toplevel()
            )
            return

        if not new_password:
            messagebox.showwarning(
                "Missing Password",
                "Please enter a new password.",
                parent=self.winfo_toplevel()
            )
            return

        if len(new_password) < 6:
            messagebox.showwarning(
                "Weak Password",
                "New password must contain at least 6 characters.",
                parent=self.winfo_toplevel()
            )
            return

        if new_password != confirm:
            messagebox.showerror(
                "Password Mismatch",
                "New password and confirmation do not match.",
                parent=self.winfo_toplevel()
            )
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE id = ?
            """,
            (self.admin_id,)
        )

        row = cursor.fetchone()

        if not row or row[0] != current:
            connection.close()

            messagebox.showerror(
                "Incorrect Password",
                "Current password is incorrect.",
                parent=self.winfo_toplevel()
            )
            return

        cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE id = ?
            """,
            (new_password, self.admin_id)
        )

        connection.commit()
        connection.close()

        self.current_password_entry.delete(0, "end")
        self.new_password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")

        messagebox.showinfo(
            "Password Updated",
            "Admin password changed successfully!",
            parent=self.winfo_toplevel()
        )

    # =====================================================
    # SAVE CAFE INFORMATION
    # =====================================================

    def save_cafe_information(self):

        values = {
            "cafe_name": self.cafe_name_entry.get().strip(),
            "contact_number": self.contact_entry.get().strip(),
            "cafe_email": self.cafe_email_entry.get().strip(),
            "address": self.address_text.get("1.0", "end").strip(),
            "opening_hours": self.opening_entry.get().strip(),
            "currency": self.currency_combo.get().strip()
        }

        if not values["cafe_name"]:
            messagebox.showwarning(
                "Missing Café Name",
                "Please enter café name.",
                parent=self.winfo_toplevel()
            )
            return

        if values["cafe_email"] and "@" not in values["cafe_email"]:
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid café email.",
                parent=self.winfo_toplevel()
            )
            return

        try:

            for key, value in values.items():
                self.save_setting(key, value)

            messagebox.showinfo(
                "Saved",
                "Café information saved successfully!",
                parent=self.winfo_toplevel()
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not save café information:\n{e}",
                parent=self.winfo_toplevel()
            )

    # =====================================================
    # DATABASE INFO
    # =====================================================

    def refresh_database_info(self):

        try:

            connection = get_connection()
            cursor = connection.cursor()

            tables = [
                ("Users", "users"),
                ("Menu Items", "menu"),
                ("Orders", "orders"),
                ("Order Items", "order_items"),
                ("Café Tables", "cafe_tables"),
                ("Reservations", "reservations"),
                ("Inventory Items", "inventory"),
                ("Feedback", "feedback")
            ]

            parts = []

            for label, table in tables:

                try:
                    cursor.execute(
                        f"SELECT COUNT(*) FROM {table}"
                    )
                    count = cursor.fetchone()[0]
                    parts.append(f"{label}: {count}")
                except Exception:
                    parts.append(f"{label}: 0")

            connection.close()

            line1 = "   •   ".join(parts[:4])
            line2 = "   •   ".join(parts[4:])

            self.db_counts_label.configure(
                text=f"{line1}\n{line2}"
            )

            db_path = os.path.abspath("cafe.db")

            if os.path.exists(db_path):

                size_kb = os.path.getsize(db_path) / 1024

                self.db_path_label.configure(
                    text=(
                        f"Database: {db_path}\n"
                        f"Size: {size_kb:.1f} KB"
                    )
                )

            else:

                self.db_path_label.configure(
                    text=f"Database: {db_path}\nSize: Not available"
                )

            self.db_status.configure(
                text="●  Connected",
                fg_color="#E5F3E9",
                text_color="#2E7D4F"
            )

        except Exception as e:

            self.db_status.configure(
                text="●  Connection Error",
                fg_color="#FBE8E6",
                text_color="#A33A2B"
            )

            self.db_path_label.configure(
                text=f"Database error: {e}"
            )

    # =====================================================
    # BACKUP DATABASE
    # =====================================================

    def backup_database(self):

        db_path = os.path.abspath("cafe.db")

        if not os.path.exists(db_path):
            messagebox.showerror(
                "Backup Error",
                "cafe.db was not found.",
                parent=self.winfo_toplevel()
            )
            return

        backup_dir = os.path.join(
            os.path.dirname(db_path),
            "database_backups"
        )

        os.makedirs(
            backup_dir,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_path = os.path.join(
            backup_dir,
            f"cafe_backup_{timestamp}.db"
        )

        try:

            shutil.copy2(
                db_path,
                backup_path
            )

            messagebox.showinfo(
                "Backup Created",
                f"Database backup created successfully!\n\n"
                f"{backup_path}",
                parent=self.winfo_toplevel()
            )

        except Exception as e:

            messagebox.showerror(
                "Backup Error",
                f"Could not create backup:\n{e}",
                parent=self.winfo_toplevel()
            )


# =====================================================
# OPTIONAL DIRECT TEST
# =====================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Settings - Brew & Bytes")
    app.geometry("1250x900")
    app.minsize(1100, 850)

    page = SettingsManagement(app)
    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()
