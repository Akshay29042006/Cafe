import customtkinter as ctk
from tkinter import messagebox

from database import (
    get_menu_items,
    add_menu_item,
    update_menu_item,
    delete_menu_item
)


class MenuManagement(ctk.CTkFrame):

    def __init__(self, parent, refresh_callback=None):
        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.refresh_callback = refresh_callback
        self.selected_item_id = None

        self.create_header()
        self.create_form()
        self.create_menu_list()

        self.load_menu_items()

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            height=80,
            fg_color="#FFFFFF",
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

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
            text="☕ Menu Management",
            font=("Arial", 24, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_area,
            text="Add, edit and manage your café products",
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(
            anchor="w"
        )

        ctk.CTkButton(
            header,
            text="🔄 Refresh",
            width=100,
            height=36,
            fg_color="#70452D",
            hover_color="#553222",
            corner_radius=9,
            command=self.load_menu_items
        ).pack(
            side="right",
            padx=25
        )

    # =====================================================
    # FORM
    # =====================================================

    def create_form(self):

        form_card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        form_card.pack(
            fill="x",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            form_card,
            text="✏️ Product Details",
            font=("Arial", 18, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 15)
        )

        fields = ctk.CTkFrame(
            form_card,
            fg_color="transparent"
        )

        fields.pack(
            fill="x",
            padx=20
        )

        # -------------------------------------------------
        # PRODUCT NAME
        # -------------------------------------------------

        name_frame = ctk.CTkFrame(
            fields,
            fg_color="transparent"
        )

        name_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        ctk.CTkLabel(
            name_frame,
            text="Product Name",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(
            anchor="w"
        )

        self.name_entry = ctk.CTkEntry(
            name_frame,
            height=40,
            placeholder_text="e.g. Cappuccino",
            corner_radius=8,
            border_color="#D8C8BA"
        )

        self.name_entry.pack(
            fill="x",
            pady=(5, 0)
        )

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        category_frame = ctk.CTkFrame(
            fields,
            fg_color="transparent"
        )

        category_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8
        )

        ctk.CTkLabel(
            category_frame,
            text="Category",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(
            anchor="w"
        )

        self.category_combo = ctk.CTkComboBox(
            category_frame,
            values=[
                "Coffee",
                "Pizza",
                "Burgers",
                "Desserts",
                "Beverages",
                "Snacks",
                "Other"
            ],
            height=40,
            corner_radius=8,
            border_color="#D8C8BA",
            button_color="#70452D",
            button_hover_color="#553222"
        )

        self.category_combo.pack(
            fill="x",
            pady=(5, 0)
        )

        self.category_combo.set("Coffee")

        # -------------------------------------------------
        # PRICE
        # -------------------------------------------------

        price_frame = ctk.CTkFrame(
            fields,
            fg_color="transparent"
        )

        price_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8
        )

        ctk.CTkLabel(
            price_frame,
            text="Price (₹)",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(
            anchor="w"
        )

        self.price_entry = ctk.CTkEntry(
            price_frame,
            height=40,
            placeholder_text="e.g. 180",
            corner_radius=8,
            border_color="#D8C8BA"
        )

        self.price_entry.pack(
            fill="x",
            pady=(5, 0)
        )

        # -------------------------------------------------
        # ICON
        # -------------------------------------------------

        icon_frame = ctk.CTkFrame(
            fields,
            fg_color="transparent"
        )

        icon_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(8, 0)
        )

        ctk.CTkLabel(
            icon_frame,
            text="Product Icon",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(
            anchor="w"
        )

        self.icon_entry = ctk.CTkEntry(
            icon_frame,
            height=40,
            placeholder_text="☕ 🍕 🍔",
            corner_radius=8,
            border_color="#D8C8BA"
        )

        self.icon_entry.pack(
            fill="x",
            pady=(5, 0)
        )

        # -------------------------------------------------
        # DESCRIPTION
        # -------------------------------------------------

        desc_frame = ctk.CTkFrame(
            form_card,
            fg_color="transparent"
        )

        desc_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 0)
        )

        ctk.CTkLabel(
            desc_frame,
            text="Description",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(
            anchor="w"
        )

        self.description_entry = ctk.CTkEntry(
            desc_frame,
            height=40,
            placeholder_text="Short description of the product",
            corner_radius=8,
            border_color="#D8C8BA"
        )

        self.description_entry.pack(
            fill="x",
            pady=(5, 0)
        )

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        buttons = ctk.CTkFrame(
            form_card,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.add_button = ctk.CTkButton(
            buttons,
            text="➕ Add Product",
            width=145,
            height=40,
            fg_color="#70452D",
            hover_color="#553222",
            corner_radius=8,
            command=self.add_product
        )

        self.add_button.pack(
            side="left",
            padx=(0, 8)
        )

        self.update_button = ctk.CTkButton(
            buttons,
            text="💾 Update Product",
            width=155,
            height=40,
            fg_color="#3E7B50",
            hover_color="#315F3D",
            corner_radius=8,
            command=self.update_product
        )

        self.update_button.pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            buttons,
            text="↩ Clear",
            width=100,
            height=40,
            fg_color="#9A8A80",
            hover_color="#786B63",
            corner_radius=8,
            command=self.clear_form
        ).pack(
            side="left",
            padx=8
        )

        self.status_switch = ctk.CTkSwitch(
            buttons,
            text="Available",
            font=("Arial", 11, "bold"),
            text_color="#4A3A30",
            progress_color="#70452D"
        )

        self.status_switch.pack(
            side="right",
            padx=10
        )

        self.status_switch.select()

    # =====================================================
    # MENU LIST
    # =====================================================

    def create_menu_list(self):

        self.list_card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        self.list_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        top = ctk.CTkFrame(
            self.list_card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            top,
            text="🍽️ Current Menu",
            font=("Arial", 18, "bold"),
            text_color="#302017"
        ).pack(
            side="left"
        )

        self.count_label = ctk.CTkLabel(
            top,
            text="0 Products",
            font=("Arial", 10, "bold"),
            text_color="#897A70"
        )

        self.count_label.pack(
            side="right"
        )

        self.menu_scroll = ctk.CTkScrollableFrame(
            self.list_card,
            fg_color="#FBF8F3"
        )

        self.menu_scroll.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # =====================================================
    # LOAD PRODUCTS
    # =====================================================

    def load_menu_items(self):

        for widget in self.menu_scroll.winfo_children():
            widget.destroy()

        try:
            items = get_menu_items()
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Could not load menu:\n{e}"
            )
            return

        self.count_label.configure(
            text=f"{len(items)} Products"
        )

        if not items:
            ctk.CTkLabel(
                self.menu_scroll,
                text="No products found.",
                font=("Arial", 14),
                text_color="#897A70"
            ).pack(
                pady=50
            )
            return

        for item in items:
            self.create_product_card(item)

    # =====================================================
    # PRODUCT CARD
    # =====================================================

    def create_product_card(self, item):

        # Expected database format:
        # id, name, category, price, description, image, available

        item_id = item[0]
        name = item[1]
        category = item[2]
        price = item[3]
        description = item[4] or ""
        icon = item[5] or "☕"
        available = item[6]

        card = ctk.CTkFrame(
            self.menu_scroll,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E8DDD4"
        )

        card.pack(
            fill="x",
            pady=6
        )

        # Icon
        icon_box = ctk.CTkFrame(
            card,
            width=65,
            height=65,
            fg_color="#F3E5D7",
            corner_radius=12
        )

        icon_box.pack(
            side="left",
            padx=12,
            pady=10
        )

        icon_box.pack_propagate(False)

        ctk.CTkLabel(
            icon_box,
            text=icon,
            font=("Arial", 28)
        ).pack(
            expand=True
        )

        # Information
        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="both",
            expand=True,
            pady=10
        )

        ctk.CTkLabel(
            info,
            text=name,
            font=("Arial", 14, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text=f"{category}  •  ₹{price:.2f}",
            font=("Arial", 11, "bold"),
            text_color="#70452D"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        ctk.CTkLabel(
            info,
            text=description if description else "No description",
            font=("Arial", 9),
            text_color="#897A70"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        # Availability
        if available:
            status_text = "● Available"
            status_color = "#3E7B50"
        else:
            status_text = "● Unavailable"
            status_color = "#A84D3A"

        ctk.CTkLabel(
            card,
            text=status_text,
            font=("Arial", 10, "bold"),
            text_color=status_color
        ).pack(
            side="left",
            padx=10
        )

        # Edit
        ctk.CTkButton(
            card,
            text="✏️ Edit",
            width=75,
            height=34,
            fg_color="#70452D",
            hover_color="#553222",
            corner_radius=8,
            command=lambda i=item: self.select_product(i)
        ).pack(
            side="right",
            padx=5
        )

        # Delete
        ctk.CTkButton(
            card,
            text="🗑️",
            width=45,
            height=34,
            fg_color="#A84D3A",
            hover_color="#853B2C",
            corner_radius=8,
            command=lambda i=item_id, n=name: self.delete_product(i, n)
        ).pack(
            side="right",
            padx=(5, 12)
        )

    # =====================================================
    # SELECT PRODUCT
    # =====================================================

    def select_product(self, item):

        self.selected_item_id = item[0]

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, item[1])

        self.category_combo.set(item[2])

        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, str(item[3]))

        self.description_entry.delete(0, "end")
        self.description_entry.insert(0, item[4] or "")

        self.icon_entry.delete(0, "end")
        self.icon_entry.insert(0, item[5] or "☕")

        if item[6]:
            self.status_switch.select()
        else:
            self.status_switch.deselect()

        self.add_button.configure(
            state="disabled"
        )

        self.update_button.configure(
            state="normal"
        )

        self.name_entry.focus()

    # =====================================================
    # ADD PRODUCT
    # =====================================================

    def add_product(self):

        name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()
        price_text = self.price_entry.get().strip()
        description = self.description_entry.get().strip()
        icon = self.icon_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Product Name",
                "Please enter product name."
            )
            return

        if not price_text:
            messagebox.showwarning(
                "Missing Price",
                "Please enter product price."
            )
            return

        try:
            price = float(price_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Price",
                "Price must be a valid number."
            )
            return

        if price < 0:
            messagebox.showerror(
                "Invalid Price",
                "Price cannot be negative."
            )
            return

        available = 1 if self.status_switch.get() else 0

        try:
            add_menu_item(
                name,
                category,
                price,
                description,
                icon,
                available
            )

            messagebox.showinfo(
                "Success",
                f"{name} added successfully!"
            )

            self.clear_form()
            self.load_menu_items()

            if self.refresh_callback:
                self.refresh_callback()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not add product:\n{e}"
            )

    # =====================================================
    # UPDATE PRODUCT
    # =====================================================

    def update_product(self):

        if self.selected_item_id is None:
            messagebox.showwarning(
                "Select Product",
                "Please select a product to update."
            )
            return

        name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()
        price_text = self.price_entry.get().strip()
        description = self.description_entry.get().strip()
        icon = self.icon_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Product Name",
                "Please enter product name."
            )
            return

        try:
            price = float(price_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Price",
                "Price must be a valid number."
            )
            return

        if price < 0:
            messagebox.showerror(
                "Invalid Price",
                "Price cannot be negative."
            )
            return

        available = 1 if self.status_switch.get() else 0

        try:
            update_menu_item(
                self.selected_item_id,
                name,
                category,
                price,
                description,
                icon,
                available
            )

            messagebox.showinfo(
                "Updated",
                f"{name} updated successfully!"
            )

            self.clear_form()
            self.load_menu_items()

            if self.refresh_callback:
                self.refresh_callback()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not update product:\n{e}"
            )

    # =====================================================
    # DELETE PRODUCT
    # =====================================================

    def delete_product(self, item_id, name):

        confirm = messagebox.askyesno(
            "Delete Product",
            f"Are you sure you want to delete:\n\n{name}?"
        )

        if not confirm:
            return

        try:
            delete_menu_item(item_id)

            messagebox.showinfo(
                "Deleted",
                f"{name} deleted successfully!"
            )

            if self.selected_item_id == item_id:
                self.clear_form()

            self.load_menu_items()

            if self.refresh_callback:
                self.refresh_callback()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not delete product:\n{e}"
            )

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.selected_item_id = None

        self.name_entry.delete(0, "end")

        self.category_combo.set("Coffee")

        self.price_entry.delete(0, "end")

        self.description_entry.delete(0, "end")

        self.icon_entry.delete(0, "end")

        self.status_switch.select()

        self.add_button.configure(
            state="normal"
        )

        self.update_button.configure(
            state="normal"
        )