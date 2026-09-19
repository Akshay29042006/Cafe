import customtkinter as ctk
import sqlite3


DATABASE_NAME = "cafe.db"


class InventoryManagement(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.selected_item_id = None

        self.create_header()
        self.create_main_area()

        self.load_inventory()

    # =====================================================
    # DATABASE
    # =====================================================

    def get_connection(self):
        return sqlite3.connect(DATABASE_NAME)

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(
            side="left"
        )

        ctk.CTkLabel(
            left,
            text="Inventory Management",
            font=("Arial", 28, "bold"),
            text_color="#2F1B12"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Manage café stock, quantities and low-stock alerts",
            font=("Arial", 12),
            text_color="#877970"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=120,
            height=38,
            corner_radius=10,
            fg_color="#70452D",
            hover_color="#5A3623",
            font=("Arial", 12, "bold"),
            command=self.load_inventory
        ).pack(
            side="right"
        )

    # =====================================================
    # MAIN AREA
    # =====================================================

    def create_main_area(self):

        main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        # -------------------------------------------------
        # LEFT FORM
        # -------------------------------------------------

        self.form_card = ctk.CTkFrame(
            main,
            width=330,
            corner_radius=18,
            fg_color="#FFFFFF"
        )

        self.form_card.pack(
            side="left",
            fill="y",
            padx=(0, 18)
        )

        self.form_card.pack_propagate(False)

        ctk.CTkLabel(
            self.form_card,
            text="📦 Stock Details",
            font=("Arial", 20, "bold"),
            text_color="#2F1B12"
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 5)
        )

        ctk.CTkLabel(
            self.form_card,
            text="Add or update inventory item",
            font=("Arial", 11),
            text_color="#877970"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 20)
        )

        # Item Name
        self.create_label(
            "Item Name"
        )

        self.item_name_entry = ctk.CTkEntry(
            self.form_card,
            height=42,
            corner_radius=10,
            placeholder_text="e.g. Coffee Beans"
        )

        self.item_name_entry.pack(
            fill="x",
            padx=22,
            pady=(0, 12)
        )

        # Category
        self.create_label(
            "Category"
        )

        self.category_combo = ctk.CTkComboBox(
            self.form_card,
            values=[
                "Coffee",
                "Dairy",
                "Bakery",
                "Vegetables",
                "Fruits",
                "Beverages",
                "Packaging",
                "Other"
            ],
            height=42,
            corner_radius=10
        )

        self.category_combo.set("Coffee")

        self.category_combo.pack(
            fill="x",
            padx=22,
            pady=(0, 12)
        )

        # Quantity
        self.create_label(
            "Quantity"
        )

        self.quantity_entry = ctk.CTkEntry(
            self.form_card,
            height=42,
            corner_radius=10,
            placeholder_text="e.g. 25"
        )

        self.quantity_entry.pack(
            fill="x",
            padx=22,
            pady=(0, 12)
        )

        # Unit
        self.create_label(
            "Unit"
        )

        self.unit_combo = ctk.CTkComboBox(
            self.form_card,
            values=[
                "kg",
                "g",
                "litre",
                "ml",
                "pcs",
                "packets",
                "boxes"
            ],
            height=42,
            corner_radius=10
        )

        self.unit_combo.set("kg")

        self.unit_combo.pack(
            fill="x",
            padx=22,
            pady=(0, 12)
        )

        # Minimum Stock
        self.create_label(
            "Minimum Stock"
        )

        self.minimum_entry = ctk.CTkEntry(
            self.form_card,
            height=42,
            corner_radius=10,
            placeholder_text="Low stock threshold"
        )

        self.minimum_entry.pack(
            fill="x",
            padx=22,
            pady=(0, 18)
        )

        # Buttons
        self.add_button = ctk.CTkButton(
            self.form_card,
            text="＋  Add Item",
            height=43,
            corner_radius=10,
            fg_color="#70452D",
            hover_color="#5A3623",
            font=("Arial", 13, "bold"),
            command=self.add_item
        )

        self.add_button.pack(
            fill="x",
            padx=22,
            pady=(0, 9)
        )

        self.update_button = ctk.CTkButton(
            self.form_card,
            text="✎  Update Selected",
            height=43,
            corner_radius=10,
            fg_color="#A66A3F",
            hover_color="#8D5633",
            font=("Arial", 13, "bold"),
            command=self.update_item
        )

        self.update_button.pack(
            fill="x",
            padx=22,
            pady=(0, 9)
        )

        self.clear_button = ctk.CTkButton(
            self.form_card,
            text="↺  Clear",
            height=40,
            corner_radius=10,
            fg_color="#E9E0D8",
            hover_color="#D8CCC1",
            text_color="#4B3529",
            font=("Arial", 12, "bold"),
            command=self.clear_form
        )

        self.clear_button.pack(
            fill="x",
            padx=22
        )

        # -------------------------------------------------
        # RIGHT AREA
        # -------------------------------------------------

        right = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        right.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.create_summary_cards(right)

        self.create_inventory_table(right)

    # =====================================================
    # LABEL
    # =====================================================

    def create_label(self, text):

        ctk.CTkLabel(
            self.form_card,
            text=text,
            font=("Arial", 11, "bold"),
            text_color="#5D463A"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 5)
        )

    # =====================================================
    # SUMMARY CARDS
    # =====================================================

    def create_summary_cards(self, parent):

        summary = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        summary.pack(
            fill="x",
            pady=(0, 18)
        )

        self.total_card = self.create_summary_card(
            summary,
            "📦",
            "Total Items",
            "0"
        )

        self.total_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        self.low_card = self.create_summary_card(
            summary,
            "⚠",
            "Low Stock",
            "0"
        )

        self.low_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8
        )

        self.out_card = self.create_summary_card(
            summary,
            "🚨",
            "Out of Stock",
            "0"
        )

        self.out_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(8, 0)
        )

    # =====================================================
    # SUMMARY CARD
    # =====================================================

    def create_summary_card(
        self,
        parent,
        icon,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            height=105,
            corner_radius=16,
            fg_color="#FFFFFF"
        )

        card.pack_propagate(False)

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=18,
            pady=(15, 0)
        )

        ctk.CTkLabel(
            top,
            text=icon,
            font=("Arial", 20)
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            top,
            text=title,
            font=("Arial", 11, "bold"),
            text_color="#877970"
        ).pack(
            side="left",
            padx=8
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 25, "bold"),
            text_color="#2F1B12"
        )

        value_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 0)
        )

        card.value_label = value_label

        return card

    # =====================================================
    # INVENTORY TABLE
    # =====================================================

    def create_inventory_table(self, parent):

        card = ctk.CTkFrame(
            parent,
            corner_radius=18,
            fg_color="#FFFFFF"
        )

        card.pack(
            fill="both",
            expand=True
        )

        header = ctk.CTkFrame(
            card,
            height=60,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(8, 0)
        )

        ctk.CTkLabel(
            header,
            text="Inventory Stock",
            font=("Arial", 19, "bold"),
            text_color="#2F1B12"
        ).pack(
            side="left"
        )

        self.status_label = ctk.CTkLabel(
            header,
            text="",
            font=("Arial", 10),
            text_color="#877970"
        )

        self.status_label.pack(
            side="right"
        )

        # Table header
        table_header = ctk.CTkFrame(
            card,
            height=45,
            corner_radius=10,
            fg_color="#F1E8DF"
        )

        table_header.pack(
            fill="x",
            padx=15,
            pady=(5, 5)
        )

        columns = [
            ("Item", 2.2),
            ("Category", 1.3),
            ("Quantity", 1.1),
            ("Unit", 0.9),
            ("Min Stock", 1.1),
            ("Status", 1.2),
            ("Action", 1.2)
        ]

        for text, weight in columns:

            ctk.CTkLabel(
                table_header,
                text=text,
                font=("Arial", 11, "bold"),
                text_color="#5D463A"
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

        # Scroll area
        self.scroll = ctk.CTkScrollableFrame(
            card,
            fg_color="transparent"
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    # =====================================================
    # LOAD INVENTORY
    # =====================================================

    def load_inventory(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                item_name,
                category,
                quantity,
                unit,
                minimum_stock
            FROM inventory
            ORDER BY
                CASE
                    WHEN quantity <= 0 THEN 0
                    WHEN quantity <= minimum_stock THEN 1
                    ELSE 2
                END,
                item_name
        """)

        items = cursor.fetchall()

        connection.close()

        total_items = len(items)

        low_stock = 0
        out_of_stock = 0

        for item in items:

            quantity = float(item[3])
            minimum = float(item[5])

            if quantity <= 0:
                out_of_stock += 1

            elif quantity <= minimum:
                low_stock += 1

            self.create_inventory_row(
                item
            )

        self.total_card.value_label.configure(
            text=str(total_items)
        )

        self.low_card.value_label.configure(
            text=str(low_stock)
        )

        self.out_card.value_label.configure(
            text=str(out_of_stock)
        )

        self.status_label.configure(
            text=f"{total_items} inventory items"
        )

    # =====================================================
    # INVENTORY ROW
    # =====================================================

    def create_inventory_row(self, item):

        item_id = item[0]
        item_name = item[1]
        category = item[2] or "Other"
        quantity = float(item[3])
        unit = item[4]
        minimum = float(item[5])

        row = ctk.CTkFrame(
            self.scroll,
            height=58,
            corner_radius=10,
            fg_color="#FBF8F5"
        )

        row.pack(
            fill="x",
            pady=4
        )

        # Item
        item_frame = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )

        item_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            item_frame,
            text=f"📦  {item_name}",
            font=("Arial", 11, "bold"),
            text_color="#2F1B12",
            anchor="w"
        ).pack(
            fill="x",
            padx=10
        )

        # Category
        ctk.CTkLabel(
            row,
            text=category,
            font=("Arial", 10),
            text_color="#6F5A4E"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

        # Quantity
        quantity_text = self.format_number(quantity)

        ctk.CTkLabel(
            row,
            text=quantity_text,
            font=("Arial", 11, "bold"),
            text_color="#2F1B12"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

        # Unit
        ctk.CTkLabel(
            row,
            text=unit,
            font=("Arial", 10),
            text_color="#6F5A4E"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

        # Minimum
        ctk.CTkLabel(
            row,
            text=self.format_number(minimum),
            font=("Arial", 10),
            text_color="#6F5A4E"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

        # Status
        if quantity <= 0:

            status_text = "OUT OF STOCK"
            status_color = "#B33A3A"

        elif quantity <= minimum:

            status_text = "LOW STOCK"
            status_color = "#C47A21"

        else:

            status_text = "IN STOCK"
            status_color = "#438A5A"

        status = ctk.CTkLabel(
            row,
            text=status_text,
            font=("Arial", 9, "bold"),
            text_color=status_color,
            fg_color=(
                "#F9E3E3"
                if quantity <= 0
                else "#FFF0D8"
                if quantity <= minimum
                else "#E5F4E8"
            ),
            corner_radius=8
        )

        status.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        # Select button
        ctk.CTkButton(
            row,
            text="Select",
            width=70,
            height=30,
            corner_radius=8,
            fg_color="#70452D",
            hover_color="#5A3623",
            font=("Arial", 10, "bold"),
            command=lambda i=item_id: self.select_item(i)
        ).pack(
            side="left",
            padx=8
        )

    # =====================================================
    # SELECT ITEM
    # =====================================================

    def select_item(self, item_id):

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                item_name,
                category,
                quantity,
                unit,
                minimum_stock
            FROM inventory
            WHERE id = ?
        """, (item_id,))

        item = cursor.fetchone()

        connection.close()

        if item is None:
            return

        self.selected_item_id = item[0]

        self.item_name_entry.delete(
            0,
            "end"
        )

        self.item_name_entry.insert(
            0,
            item[1]
        )

        self.category_combo.set(
            item[2] or "Other"
        )

        self.quantity_entry.delete(
            0,
            "end"
        )

        self.quantity_entry.insert(
            0,
            self.format_number(item[3])
        )

        self.unit_combo.set(
            item[4]
        )

        self.minimum_entry.delete(
            0,
            "end"
        )

        self.minimum_entry.insert(
            0,
            self.format_number(item[5])
        )

        self.add_button.configure(
            text="＋  Add New Item"
        )

    # =====================================================
    # ADD ITEM
    # =====================================================

    def add_item(self):

        values = self.get_form_values()

        if values is None:
            return

        item_name, category, quantity, unit, minimum = values

        try:

            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO inventory
                (
                    item_name,
                    category,
                    quantity,
                    unit,
                    minimum_stock
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                item_name,
                category,
                quantity,
                unit,
                minimum
            ))

            connection.commit()
            connection.close()

            self.show_message(
                "Success",
                "Inventory item added successfully."
            )

            self.clear_form()
            self.load_inventory()

        except Exception as e:

            self.show_message(
                "Database Error",
                str(e)
            )

    # =====================================================
    # UPDATE ITEM
    # =====================================================

    def update_item(self):

        if self.selected_item_id is None:

            self.show_message(
                "Select Item",
                "Please select an inventory item first."
            )

            return

        values = self.get_form_values()

        if values is None:
            return

        item_name, category, quantity, unit, minimum = values

        try:

            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE inventory
                SET
                    item_name = ?,
                    category = ?,
                    quantity = ?,
                    unit = ?,
                    minimum_stock = ?
                WHERE id = ?
            """, (
                item_name,
                category,
                quantity,
                unit,
                minimum,
                self.selected_item_id
            ))

            connection.commit()
            connection.close()

            self.show_message(
                "Success",
                "Inventory item updated successfully."
            )

            self.clear_form()
            self.load_inventory()

        except Exception as e:

            self.show_message(
                "Database Error",
                str(e)
            )

    # =====================================================
    # GET FORM VALUES
    # =====================================================

    def get_form_values(self):

        item_name = self.item_name_entry.get().strip()
        category = self.category_combo.get().strip()
        quantity_text = self.quantity_entry.get().strip()
        unit = self.unit_combo.get().strip()
        minimum_text = self.minimum_entry.get().strip()

        if not item_name:

            self.show_message(
                "Validation",
                "Please enter item name."
            )

            return None

        if not quantity_text:

            self.show_message(
                "Validation",
                "Please enter quantity."
            )

            return None

        if not minimum_text:

            self.show_message(
                "Validation",
                "Please enter minimum stock."
            )

            return None

        try:

            quantity = float(
                quantity_text
            )

            minimum = float(
                minimum_text
            )

        except ValueError:

            self.show_message(
                "Invalid Number",
                "Quantity and Minimum Stock must be numbers."
            )

            return None

        if quantity < 0:

            self.show_message(
                "Invalid Quantity",
                "Quantity cannot be negative."
            )

            return None

        if minimum < 0:

            self.show_message(
                "Invalid Minimum",
                "Minimum stock cannot be negative."
            )

            return None

        return (
            item_name,
            category,
            quantity,
            unit,
            minimum
        )

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.selected_item_id = None

        self.item_name_entry.delete(
            0,
            "end"
        )

        self.quantity_entry.delete(
            0,
            "end"
        )

        self.minimum_entry.delete(
            0,
            "end"
        )

        self.category_combo.set(
            "Coffee"
        )

        self.unit_combo.set(
            "kg"
        )

        self.add_button.configure(
            text="＋  Add Item"
        )

    # =====================================================
    # FORMAT NUMBER
    # =====================================================

    def format_number(self, value):

        try:

            value = float(value)

            if value.is_integer():
                return str(int(value))

            return f"{value:.2f}"

        except:

            return str(value)

    # =====================================================
    # MESSAGE WINDOW
    # =====================================================

    def show_message(
        self,
        title,
        message
    ):

        popup = ctk.CTkToplevel(
            self
        )

        popup.title(
            title
        )

        popup.geometry(
            "430x210"
        )

        popup.resizable(
            False,
            False
        )

        popup.transient(
            self.winfo_toplevel()
        )

        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="☕",
            font=("Arial", 32),
            text_color="#70452D"
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            popup,
            text=title,
            font=("Arial", 17, "bold"),
            text_color="#2F1B12"
        ).pack()

        ctk.CTkLabel(
            popup,
            text=message,
            font=("Arial", 11),
            text_color="#6F5A4E",
            wraplength=360
        ).pack(
            pady=10
        )

        ctk.CTkButton(
            popup,
            text="OK",
            width=100,
            height=35,
            corner_radius=9,
            fg_color="#70452D",
            hover_color="#5A3623",
            command=popup.destroy
        ).pack(
            pady=5
        )

    # =====================================================
    # DELETE ITEM
    # =====================================================

    def delete_item(self):

        if self.selected_item_id is None:

            self.show_message(
                "Select Item",
                "Please select an inventory item first."
            )

            return

        confirm = ctk.CTkToplevel(
            self
        )

        confirm.title(
            "Delete Inventory Item"
        )

        confirm.geometry(
            "430x220"
        )

        confirm.resizable(
            False,
            False
        )

        confirm.transient(
            self.winfo_toplevel()
        )

        confirm.grab_set()

        ctk.CTkLabel(
            confirm,
            text="🗑",
            font=("Arial", 32)
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            confirm,
            text="Delete this inventory item?",
            font=("Arial", 16, "bold"),
            text_color="#2F1B12"
        ).pack()

        ctk.CTkLabel(
            confirm,
            text="This action cannot be undone.",
            font=("Arial", 11),
            text_color="#877970"
        ).pack(
            pady=8
        )

        buttons = ctk.CTkFrame(
            confirm,
            fg_color="transparent"
        )

        buttons.pack(
            pady=10
        )

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=100,
            height=35,
            corner_radius=8,
            fg_color="#E9E0D8",
            hover_color="#D8CCC1",
            text_color="#4B3529",
            command=confirm.destroy
        ).pack(
            side="left",
            padx=6
        )

        ctk.CTkButton(
            buttons,
            text="Delete",
            width=100,
            height=35,
            corner_radius=8,
            fg_color="#B33A3A",
            hover_color="#922D2D",
            command=lambda: self.confirm_delete(confirm)
        ).pack(
            side="left",
            padx=6
        )

    # =====================================================
    # CONFIRM DELETE
    # =====================================================

    def confirm_delete(self, popup):

        try:

            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM inventory
                WHERE id = ?
            """, (
                self.selected_item_id,
            ))

            connection.commit()
            connection.close()

            popup.destroy()

            self.show_message(
                "Deleted",
                "Inventory item deleted successfully."
            )

            self.clear_form()
            self.load_inventory()

        except Exception as e:

            popup.destroy()

            self.show_message(
                "Database Error",
                str(e)
            )