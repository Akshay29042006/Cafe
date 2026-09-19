import customtkinter as ctk

from database import initialize_database
from pages.login import LoginPage
from pages.admin_dashboard import AdminDashboard
from pages.customer_dashboard import CustomerDashboard


# =========================================================
# APP SETTINGS
# =========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# =========================================================
# MAIN APPLICATION
# =========================================================

class CafeApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Brew & Bytes Café")

        self.geometry("1400x800")

        self.minsize(
            1100,
            650
        )

        self.center_window()

        self.show_login()

    # =====================================================
    # CENTER WINDOW
    # =====================================================

    def center_window(self):

        self.update_idletasks()

        width = 1400
        height = 800

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # =====================================================
    # CLEAR SCREEN
    # =====================================================

    def clear_screen(self):

        for widget in self.winfo_children():
            widget.destroy()

    # =====================================================
    # LOGIN
    # =====================================================

    def show_login(self):

        self.clear_screen()

        login_page = LoginPage(
            self,
            self.login_success
        )

        login_page.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # LOGIN SUCCESS
    # =====================================================

    def login_success(self, role):

        if role == "Admin":
            self.show_admin_dashboard()

        elif role == "Customer":
            self.show_customer_dashboard()

    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    def show_admin_dashboard(self):

        self.clear_screen()

        dashboard = AdminDashboard(
            self,
            self.show_login
        )

        dashboard.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # CUSTOMER DASHBOARD
    # =====================================================

    def show_customer_dashboard(self):

        self.clear_screen()

        dashboard = CustomerDashboard(
            self,
            self.show_login
        )

        dashboard.pack(
            fill="both",
            expand=True
        )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    initialize_database()

    app = CafeApp()

    app.mainloop()