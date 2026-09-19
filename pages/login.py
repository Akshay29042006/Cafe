import customtkinter as ctk
from tkinter import messagebox

from database import authenticate_user, get_connection


class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, on_login):
        super().__init__(
            parent,
            fg_color="#F8F3EA"
        )

        self.parent = parent
        self.on_login = on_login
        self.selected_role = "Customer"

        self.create_ui()

    # =====================================================
    # UI
    # =====================================================

    def create_ui(self):

        main = ctk.CTkFrame(
            self,
            fg_color="#F8F3EA"
        )

        main.pack(
            fill="both",
            expand=True
        )

        # =================================================
        # LEFT SIDE
        # =================================================

        left = ctk.CTkFrame(
            main,
            fg_color="#3B2417",
            corner_radius=0,
            width=480
        )

        left.pack(
            side="left",
            fill="y"
        )

        left.pack_propagate(False)

        ctk.CTkLabel(
            left,
            text="☕",
            font=("Arial", 72),
            text_color="#F4B860"
        ).pack(
            pady=(110, 10)
        )

        ctk.CTkLabel(
            left,
            text="BREW & BYTES",
            font=("Arial", 32, "bold"),
            text_color="#FFFFFF"
        ).pack()

        ctk.CTkLabel(
            left,
            text="CAFÉ",
            font=("Arial", 18, "bold"),
            text_color="#F4B860"
        ).pack(
            pady=(0, 30)
        )

        ctk.CTkLabel(
            left,
            text="Good coffee.\nGreat food.\nBetter moments.",
            font=("Arial", 20),
            text_color="#E8DED3",
            justify="center"
        ).pack(
            pady=20
        )

        ctk.CTkLabel(
            left,
            text="☕ Crafted with passion",
            font=("Arial", 14),
            text_color="#BDAFA2"
        ).pack(
            side="bottom",
            pady=35
        )

        # =================================================
        # RIGHT SIDE
        # =================================================

        right = ctk.CTkFrame(
            main,
            fg_color="#FFFFFF",
            corner_radius=0
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            right,
            text="Welcome Back 👋",
            font=("Arial", 34, "bold"),
            text_color="#2E2118"
        ).pack(
            pady=(75, 5)
        )

        ctk.CTkLabel(
            right,
            text="Login to continue to your café account",
            font=("Arial", 15),
            text_color="#8C8178"
        ).pack(
            pady=(0, 35)
        )

        # =================================================
        # ROLE
        # =================================================

        role_frame = ctk.CTkFrame(
            right,
            fg_color="#F5F0E8",
            corner_radius=15,
            width=440,
            height=70
        )

        role_frame.pack(
            pady=5
        )

        role_frame.pack_propagate(False)

        self.admin_button = ctk.CTkButton(
            role_frame,
            text="👨‍💼  Admin",
            font=("Arial", 15, "bold"),
            fg_color="#D9C8B4",
            hover_color="#CBB59D",
            text_color="#3B2417",
            corner_radius=10,
            command=lambda: self.select_role("Admin")
        )

        self.admin_button.pack(
            side="left",
            padx=8,
            pady=10,
            fill="both",
            expand=True
        )

        self.customer_button = ctk.CTkButton(
            role_frame,
            text="👤  Customer",
            font=("Arial", 15, "bold"),
            fg_color="#3B2417",
            hover_color="#533522",
            text_color="#FFFFFF",
            corner_radius=10,
            command=lambda: self.select_role("Customer")
        )

        self.customer_button.pack(
            side="right",
            padx=8,
            pady=10,
            fill="both",
            expand=True
        )

        # =================================================
        # EMAIL
        # =================================================

        ctk.CTkLabel(
            right,
            text="Email Address",
            font=("Arial", 14, "bold"),
            text_color="#3B3028"
        ).pack(
            anchor="w",
            padx=120,
            pady=(30, 5)
        )

        self.email_entry = ctk.CTkEntry(
            right,
            width=440,
            height=48,
            placeholder_text="Enter your email",
            font=("Arial", 14),
            border_width=1,
            border_color="#D7CCC0",
            fg_color="#FBF9F6",
            text_color="#2E2118",
            corner_radius=10
        )

        self.email_entry.pack()

        # =================================================
        # PASSWORD
        # =================================================

        ctk.CTkLabel(
            right,
            text="Password",
            font=("Arial", 14, "bold"),
            text_color="#3B3028"
        ).pack(
            anchor="w",
            padx=120,
            pady=(18, 5)
        )

        self.password_entry = ctk.CTkEntry(
            right,
            width=440,
            height=48,
            placeholder_text="Enter your password",
            show="●",
            font=("Arial", 14),
            border_width=1,
            border_color="#D7CCC0",
            fg_color="#FBF9F6",
            text_color="#2E2118",
            corner_radius=10
        )

        self.password_entry.pack()

        # =================================================
        # OPTIONS
        # =================================================

        options = ctk.CTkFrame(
            right,
            fg_color="transparent",
            width=440
        )

        options.pack(
            pady=15
        )

        self.remember = ctk.CTkCheckBox(
            options,
            text="Remember me",
            font=("Arial", 13),
            text_color="#6E6258",
            fg_color="#3B2417",
            hover_color="#533522"
        )

        self.remember.pack(
            side="left"
        )

        ctk.CTkLabel(
            options,
            text="Forgot Password?",
            font=("Arial", 13, "underline"),
            text_color="#A86D32"
        ).pack(
            side="right"
        )

        # =================================================
        # LOGIN BUTTON
        # =================================================

        ctk.CTkButton(
            right,
            text="LOGIN  →",
            width=440,
            height=52,
            font=("Arial", 16, "bold"),
            fg_color="#3B2417",
            hover_color="#5A3823",
            text_color="#FFFFFF",
            corner_radius=12,
            command=self.login
        ).pack(
            pady=(5, 15)
        )

        # =================================================
        # REGISTER
        # =================================================

        register_frame = ctk.CTkFrame(
            right,
            fg_color="transparent"
        )

        register_frame.pack()

        ctk.CTkLabel(
            register_frame,
            text="Don't have an account?",
            font=("Arial", 13),
            text_color="#80756C"
        ).pack(
            side="left"
        )

        self.register_button = ctk.CTkButton(
            register_frame,
            text="Create Account",
            font=("Arial", 13, "bold"),
            text_color="#A86D32",
            fg_color="transparent",
            hover_color="#F3E8DA",
            width=125,
            height=30,
            corner_radius=8,
            command=self.open_register
        )

        self.register_button.pack(
            side="left"
        )

    # =====================================================
    # ROLE
    # =====================================================

    def select_role(self, role):

        self.selected_role = role

        if role == "Admin":

            self.admin_button.configure(
                fg_color="#3B2417",
                text_color="#FFFFFF"
            )

            self.customer_button.configure(
                fg_color="#D9C8B4",
                text_color="#3B2417"
            )

        else:

            self.customer_button.configure(
                fg_color="#3B2417",
                text_color="#FFFFFF"
            )

            self.admin_button.configure(
                fg_color="#D9C8B4",
                text_color="#3B2417"
            )

    # =====================================================
    # LOGIN
    # =====================================================

    def login(self):

        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter email and password."
            )

            return

        user = authenticate_user(
            email,
            password,
            self.selected_role
        )

        if user:

            self.on_login(
                self.selected_role
            )

        else:

            messagebox.showerror(
                "Login Failed",
                f"Invalid {self.selected_role} email or password."
            )

    # =====================================================
    # OPEN REGISTER WINDOW
    # =====================================================

    def open_register(self):

        self.register_window = ctk.CTkToplevel(
            self
        )

        self.register_window.title(
            "Create Customer Account"
        )

        self.register_window.geometry(
            "520x680"
        )

        self.register_window.resizable(
            False,
            False
        )

        self.register_window.configure(
            fg_color="#F8F3EA"
        )

        self.register_window.transient(
            self.winfo_toplevel()
        )

        self.register_window.grab_set()

        # =================================================
        # HEADER
        # =================================================

        header = ctk.CTkFrame(
            self.register_window,
            fg_color="#3B2417",
            corner_radius=0,
            height=125
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="☕",
            font=("Arial", 38),
            text_color="#F4B860"
        ).pack(
            pady=(12, 0)
        )

        ctk.CTkLabel(
            header,
            text="Create Your Account",
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack()

        ctk.CTkLabel(
            header,
            text="Join Brew & Bytes Café",
            font=("Arial", 12),
            text_color="#D8C9BC"
        ).pack(
            pady=(2, 8)
        )

        # =================================================
        # FORM
        # =================================================

        form = ctk.CTkFrame(
            self.register_window,
            fg_color="transparent"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=18
        )

        # =================================================
        # NAME
        # =================================================

        ctk.CTkLabel(
            form,
            text="Full Name",
            font=("Arial", 13, "bold"),
            text_color="#3B3028"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.register_name = ctk.CTkEntry(
            form,
            height=43,
            placeholder_text="Enter your full name",
            font=("Arial", 13),
            border_color="#D7CCC0",
            fg_color="#FFFFFF",
            text_color="#2E2118",
            corner_radius=9
        )

        self.register_name.pack(
            fill="x"
        )

        # =================================================
        # EMAIL
        # =================================================

        ctk.CTkLabel(
            form,
            text="Email Address",
            font=("Arial", 13, "bold"),
            text_color="#3B3028"
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.register_email = ctk.CTkEntry(
            form,
            height=43,
            placeholder_text="Enter your email",
            font=("Arial", 13),
            border_color="#D7CCC0",
            fg_color="#FFFFFF",
            text_color="#2E2118",
            corner_radius=9
        )

        self.register_email.pack(
            fill="x"
        )

        # =================================================
        # PASSWORD
        # =================================================

        ctk.CTkLabel(
            form,
            text="Password",
            font=("Arial", 13, "bold"),
            text_color="#3B3028"
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.register_password = ctk.CTkEntry(
            form,
            height=43,
            placeholder_text="Create a password",
            show="●",
            font=("Arial", 13),
            border_color="#D7CCC0",
            fg_color="#FFFFFF",
            text_color="#2E2118",
            corner_radius=9
        )

        self.register_password.pack(
            fill="x"
        )

        # =================================================
        # CONFIRM PASSWORD
        # =================================================

        ctk.CTkLabel(
            form,
            text="Confirm Password",
            font=("Arial", 13, "bold"),
            text_color="#3B3028"
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.register_confirm = ctk.CTkEntry(
            form,
            height=43,
            placeholder_text="Re-enter your password",
            show="●",
            font=("Arial", 13),
            border_color="#D7CCC0",
            fg_color="#FFFFFF",
            text_color="#2E2118",
            corner_radius=9
        )

        self.register_confirm.pack(
            fill="x"
        )

        # =================================================
        # INFO
        # =================================================

        ctk.CTkLabel(
            form,
            text="✓ Account type: Customer",
            font=("Arial", 12, "bold"),
            text_color="#6E6258"
        ).pack(
            anchor="w",
            pady=(12, 0)
        )

        ctk.CTkLabel(
            form,
            text="Password must contain at least 6 characters.",
            font=("Arial", 11),
            text_color="#9A8D82"
        ).pack(
            anchor="w",
            pady=(2, 10)
        )

        # =================================================
        # REGISTER BUTTON
        # =================================================

        ctk.CTkButton(
            form,
            text="CREATE ACCOUNT  ✓",
            height=48,
            font=("Arial", 15, "bold"),
            fg_color="#3B2417",
            hover_color="#5A3823",
            text_color="white",
            corner_radius=10,
            command=self.register_customer
        ).pack(
            fill="x",
            pady=(5, 8)
        )

        # =================================================
        # BACK
        # =================================================

        ctk.CTkButton(
            form,
            text="← Back to Login",
            height=35,
            font=("Arial", 12, "bold"),
            fg_color="transparent",
            hover_color="#EDE2D6",
            text_color="#A86D32",
            command=self.close_register
        ).pack()

    # =====================================================
    # REGISTER CUSTOMER
    # =====================================================

    def register_customer(self):

        name = self.register_name.get().strip()
        email = self.register_email.get().strip().lower()
        password = self.register_password.get()
        confirm_password = self.register_confirm.get()

        # -------------------------------------------------
        # EMPTY CHECK
        # -------------------------------------------------

        if not name or not email or not password or not confirm_password:

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields.",
                parent=self.register_window
            )

            return

        # -------------------------------------------------
        # NAME VALIDATION
        # -------------------------------------------------

        if len(name) < 2:

            messagebox.showwarning(
                "Invalid Name",
                "Please enter a valid full name.",
                parent=self.register_window
            )

            return

        # -------------------------------------------------
        # EMAIL VALIDATION
        # -------------------------------------------------

        if "@" not in email or "." not in email:

            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address.",
                parent=self.register_window
            )

            return

        # -------------------------------------------------
        # PASSWORD VALIDATION
        # -------------------------------------------------

        if len(password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters.",
                parent=self.register_window
            )

            return

        # -------------------------------------------------
        # CONFIRM PASSWORD
        # -------------------------------------------------

        if password != confirm_password:

            messagebox.showerror(
                "Password Mismatch",
                "Password and Confirm Password do not match.",
                parent=self.register_window
            )

            return

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # -------------------------------------------------
            # CHECK EXISTING EMAIL
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE LOWER(email) = ?
                """,
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                connection.close()

                messagebox.showwarning(
                    "Email Already Registered",
                    "This email is already registered.\n\n"
                    "Please use another email or login with this account.",
                    parent=self.register_window
                )

                return

            # -------------------------------------------------
            # INSERT CUSTOMER
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password,
                    role
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    password,
                    "Customer"
                )
            )

            connection.commit()

            connection.close()

            # -------------------------------------------------
            # SUCCESS
            # -------------------------------------------------

            messagebox.showinfo(
                "Registration Successful 🎉",
                f"Welcome to Brew & Bytes Café, {name}!\n\n"
                "Your Customer account has been created successfully.\n\n"
                "You can now login with your email and password.",
                parent=self.register_window
            )

            # Put registered email on login screen
            self.email_entry.delete(
                0,
                "end"
            )

            self.email_entry.insert(
                0,
                email
            )

            # Select Customer
            self.select_role(
                "Customer"
            )

            self.close_register()

            # Focus password
            self.password_entry.focus()

        except Exception as error:

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass

            messagebox.showerror(
                "Registration Error",
                f"Could not create account.\n\n{error}",
                parent=self.register_window
            )

    # =====================================================
    # CLOSE REGISTER
    # =====================================================

    def close_register(self):

        try:

            self.register_window.grab_release()

        except Exception:
            pass

        self.register_window.destroy()