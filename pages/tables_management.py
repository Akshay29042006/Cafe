import customtkinter as ctk
from tkinter import messagebox

from database import get_connection


class TablesManagement(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F6F1E9"
        )

        self.parent = parent

        self.create_header()
        self.create_summary()
        self.create_tables_section()

        self.load_tables()

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            height=88,
            fg_color="#F6F1E9",
            corner_radius=0
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(12, 0)
        )

        header.pack_propagate(False)

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_area.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            title_area,
            text="🪑  Tables Management",
            font=("Arial", 25, "bold"),
            text_color="#302017"
        ).pack(
            anchor="w",
            pady=(8, 0)
        )

        ctk.CTkLabel(
            title_area,
            text="Manage café tables and their availability",
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        ctk.CTkButton(
            header,
            text="+  Add Table",
            width=138,
            height=42,
            font=("Arial", 12, "bold"),
            fg_color="#70452D",
            hover_color="#5A3823",
            text_color="white",
            corner_radius=11,
            command=self.open_add_table
        ).pack(
            side="right",
            padx=(10, 0),
            pady=10
        )

        ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=138,
            height=42,
            font=("Arial", 12, "bold"),
            fg_color="#3B2417",
            hover_color="#5A3823",
            text_color="white",
            corner_radius=11,
            command=self.load_tables
        ).pack(
            side="right",
            pady=10
        )

    # =====================================================
    # SUMMARY CARDS
    # =====================================================

    def create_summary(self):

        summary = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        summary.pack(
            fill="x",
            padx=30,
            pady=(4, 12)
        )

        self.total_value = self.create_stat_card(
            summary,
            "🪑",
            "Total Tables"
        )

        self.available_value = self.create_stat_card(
            summary,
            "✓",
            "Available"
        )

        self.occupied_value = self.create_stat_card(
            summary,
            "●",
            "Occupied"
        )

        self.reserved_value = self.create_stat_card(
            summary,
            "▣",
            "Reserved"
        )

        for column in range(4):
            summary.grid_columnconfigure(
                column,
                weight=1
            )

    def create_stat_card(
        self,
        parent,
        icon,
        title
    ):

        card = ctk.CTkFrame(
            parent,
            height=96,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        card.grid(
            row=0,
            column=len(parent.winfo_children()),
            sticky="nsew",
            padx=5
        )

        card.grid_propagate(False)

        icon_box = ctk.CTkFrame(
            card,
            width=56,
            height=56,
            fg_color="#F2E3D3",
            corner_radius=13
        )

        icon_box.pack(
            side="left",
            padx=(16, 12),
            pady=20
        )

        icon_box.pack_propagate(False)

        ctk.CTkLabel(
            icon_box,
            text=icon,
            font=("Arial", 24, "bold"),
            text_color="#70452D"
        ).pack(
            expand=True
        )

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="both",
            expand=True,
            pady=17
        )

        ctk.CTkLabel(
            info,
            text=title,
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(
            anchor="w"
        )

        value = ctk.CTkLabel(
            info,
            text="0",
            font=("Arial", 23, "bold"),
            text_color="#302017"
        )

        value.pack(
            anchor="w",
            pady=(1, 0)
        )

        return value

    # =====================================================
    # TABLE SECTION
    # =====================================================

    def create_tables_section(self):

        section = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=17
        )

        section.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        # Section header
        section_header = ctk.CTkFrame(
            section,
            height=58,
            fg_color="transparent"
        )

        section_header.pack(
            fill="x",
            padx=24,
            pady=(4, 0)
        )

        section_header.pack_propagate(False)

        ctk.CTkLabel(
            section_header,
            text="All Café Tables",
            font=("Arial", 19, "bold"),
            text_color="#302017"
        ).pack(
            side="left",
            pady=10
        )

        ctk.CTkLabel(
            section_header,
            text="Update table status from here",
            font=("Arial", 10),
            text_color="#B08069"
        ).pack(
            side="right",
            pady=10
        )

        # Column header
        columns = ctk.CTkFrame(
            section,
            height=42,
            fg_color="#F3ECE4",
            corner_radius=10
        )

        columns.pack(
            fill="x",
            padx=24,
            pady=(0, 7)
        )

        columns.pack_propagate(False)

        ctk.CTkLabel(
            columns,
            text="TABLE",
            width=190,
            anchor="w",
            font=("Arial", 10, "bold"),
            text_color="#6F5C50"
        ).pack(
            side="left",
            padx=(18, 0)
        )

        ctk.CTkLabel(
            columns,
            text="SEATS",
            width=105,
            anchor="w",
            font=("Arial", 10, "bold"),
            text_color="#6F5C50"
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            columns,
            text="STATUS",
            width=145,
            anchor="w",
            font=("Arial", 10, "bold"),
            text_color="#6F5C50"
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            columns,
            text="CHANGE STATUS",
            width=300,
            anchor="w",
            font=("Arial", 10, "bold"),
            text_color="#6F5C50"
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            columns,
            text="ACTION",
            width=100,
            anchor="w",
            font=("Arial", 10, "bold"),
            text_color="#6F5C50"
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            columns,
            text="DELETE",
            anchor="w",
            font=("Arial", 10, "bold"),
            text_color="#6F5C50"
        ).pack(
            side="left"
        )

        # Scrollable list area.
        # All 10 tables are loaded; scroll when the window height is limited.
        self.table_list = ctk.CTkScrollableFrame(
            section,
            fg_color="transparent",
            scrollbar_button_color="#B88A6A",
            scrollbar_button_hover_color="#8B5E3C"
        )

        self.table_list.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 12)
        )

    # =====================================================
    # LOAD TABLES
    # =====================================================

    def load_tables(self):

        for widget in self.table_list.winfo_children():
            widget.destroy()

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    table_number,
                    seats,
                    status
                FROM cafe_tables
                ORDER BY table_number
            """)

            tables = cursor.fetchall()

            connection.close()

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Could not load tables.\n\n{error}"
            )

            return

        total = len(tables)
        available = sum(
            1 for table in tables
            if table[3] == "Available"
        )
        occupied = sum(
            1 for table in tables
            if table[3] == "Occupied"
        )
        reserved = sum(
            1 for table in tables
            if table[3] == "Reserved"
        )

        self.total_value.configure(
            text=str(total)
        )

        self.available_value.configure(
            text=str(available)
        )

        self.occupied_value.configure(
            text=str(occupied)
        )

        self.reserved_value.configure(
            text=str(reserved)
        )

        if not tables:

            ctk.CTkLabel(
                self.table_list,
                text="No café tables found.",
                font=("Arial", 13),
                text_color="#897A70"
            ).pack(
                pady=30
            )

            return

        for table in tables:
            self.create_table_row(table)

    # =====================================================
    # TABLE ROW
    # =====================================================

    def create_table_row(self, table):

        table_id = table[0]
        table_number = table[1]
        seats = table[2]
        status = table[3]

        row = ctk.CTkFrame(
            self.table_list,
            height=50,
            fg_color="#FBF8F3",
            corner_radius=9
        )

        row.pack(
            fill="x",
            pady=3
        )

        row.pack_propagate(False)

        # Table name
        ctk.CTkLabel(
            row,
            text=f"Table {table_number}",
            width=190,
            anchor="w",
            font=("Arial", 11, "bold"),
            text_color="#302017"
        ).pack(
            side="left",
            padx=(18, 0)
        )

        # Seats
        ctk.CTkLabel(
            row,
            text=f"{seats} seats",
            width=105,
            anchor="w",
            font=("Arial", 10),
            text_color="#806F63"
        ).pack(
            side="left"
        )

        # Current status
        status_colors = {
            "Available": "#3E7B50",
            "Occupied": "#B85F32",
            "Reserved": "#8A7040"
        }

        ctk.CTkLabel(
            row,
            text=status,
            width=115,
            height=30,
            fg_color="#E7F3EA" if status == "Available"
            else "#F7E8DE" if status == "Occupied"
            else "#F1EBDD",
            corner_radius=15,
            font=("Arial", 10, "bold"),
            text_color=status_colors.get(
                status,
                "#70452D"
            )
        ).pack(
            side="left",
            padx=(0, 20)
        )

        # Status dropdown
        status_combo = ctk.CTkComboBox(
            row,
            width=180,
            height=34,
            values=[
                "Available",
                "Occupied",
                "Reserved"
            ],
            font=("Arial", 10),
            dropdown_font=("Arial", 10),
            fg_color="#FFFFFF",
            border_color="#D9C8B9",
            button_color="#70452D",
            button_hover_color="#5A3823",
            text_color="#302017",
            corner_radius=8
        )

        status_combo.set(status)

        status_combo.pack(
            side="left",
            padx=(0, 18)
        )

        # Update button
        ctk.CTkButton(
            row,
            text="Update",
            width=92,
            height=34,
            font=("Arial", 10, "bold"),
            fg_color="#3B2417",
            hover_color="#5A3823",
            text_color="white",
            corner_radius=8,
            command=lambda:
                self.update_table_status(
                    table_id,
                    status_combo
                )
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            row,
            text="Delete",
            width=78,
            height=34,
            font=("Arial", 10, "bold"),
            fg_color="#A33E32",
            hover_color="#7F2F27",
            text_color="white",
            corner_radius=8,
            command=lambda:
                self.delete_table(
                    table_id,
                    table_number
                )
        ).pack(
            side="left"
        )

    # =====================================================
    # ADD TABLE
    # =====================================================

    def open_add_table(self):

        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Café Table")
        dialog.geometry("430x330")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#F6F1E9")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="🪑  Add New Table",
            font=("Arial", 21, "bold"),
            text_color="#302017"
        ).pack(
            pady=(25, 5)
        )

        ctk.CTkLabel(
            dialog,
            text="Create a new table for your café",
            font=("Arial", 11),
            text_color="#897A70"
        ).pack(
            pady=(0, 18)
        )

        ctk.CTkLabel(
            dialog,
            text="Table Number",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(
            anchor="w",
            padx=45
        )

        number_entry = ctk.CTkEntry(
            dialog,
            width=340,
            height=40,
            placeholder_text="Example: 11",
            corner_radius=9
        )

        number_entry.pack(
            padx=45,
            pady=(5, 14)
        )

        ctk.CTkLabel(
            dialog,
            text="Number of Seats",
            font=("Arial", 11, "bold"),
            text_color="#5E5148"
        ).pack(
            anchor="w",
            padx=45
        )

        seats_entry = ctk.CTkEntry(
            dialog,
            width=340,
            height=40,
            placeholder_text="Example: 4",
            corner_radius=9
        )

        seats_entry.pack(
            padx=45,
            pady=(5, 18)
        )

        def save_table():

            number_text = number_entry.get().strip()
            seats_text = seats_entry.get().strip()

            if not number_text or not seats_text:
                messagebox.showwarning(
                    "Missing Details",
                    "Please enter table number and seats."
                )
                return

            try:
                table_number = int(number_text)
                seats = int(seats_text)

                if table_number <= 0 or seats <= 0:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Invalid Details",
                    "Table number and seats must be positive numbers."
                )
                return

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "SELECT id FROM cafe_tables WHERE table_number = ?",
                    (table_number,)
                )

                if cursor.fetchone():
                    connection.close()

                    messagebox.showwarning(
                        "Duplicate Table",
                        f"Table {table_number} already exists."
                    )
                    return

                cursor.execute(
                    """
                    INSERT INTO cafe_tables
                    (table_number, seats, status)
                    VALUES (?, ?, ?)
                    """,
                    (
                        table_number,
                        seats,
                        "Available"
                    )
                )

                connection.commit()
                connection.close()

                dialog.destroy()
                self.load_tables()

                messagebox.showinfo(
                    "Table Added",
                    f"Table {table_number} has been added successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Add Table Error",
                    f"Could not add table.\n\n{error}"
                )

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=45
        )

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=145,
            height=40,
            fg_color="#D8CEC5",
            hover_color="#C8BBB0",
            text_color="#4A382E",
            corner_radius=9,
            command=dialog.destroy
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            buttons,
            text="Add Table",
            width=175,
            height=40,
            fg_color="#70452D",
            hover_color="#5A3823",
            text_color="white",
            corner_radius=9,
            command=save_table
        ).pack(
            side="right"
        )

        number_entry.focus_set()

    # =====================================================
    # DELETE TABLE
    # =====================================================

    def delete_table(self, table_id, table_number):

        confirm = messagebox.askyesno(
            "Delete Table",
            f"Are you sure you want to delete Table {table_number}?\n\n"
            "This action cannot be undone."
        )

        if not confirm:
            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Do not allow deletion if this table is used in reservations.
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM reservations
                WHERE table_id = ?
                """,
                (table_id,)
            )

            reservation_count = cursor.fetchone()[0]

            if reservation_count > 0:

                connection.close()

                messagebox.showwarning(
                    "Cannot Delete Table",
                    f"Table {table_number} has {reservation_count} "
                    "reservation(s) linked to it.\n\n"
                    "Cancel/remove those reservations first."
                )

                return

            cursor.execute(
                "DELETE FROM cafe_tables WHERE id = ?",
                (table_id,)
            )

            connection.commit()
            connection.close()

            self.load_tables()

            messagebox.showinfo(
                "Table Deleted",
                f"Table {table_number} has been deleted."
            )

        except Exception as error:

            messagebox.showerror(
                "Delete Table Error",
                f"Could not delete table.\n\n{error}"
            )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    def update_table_status(
        self,
        table_id,
        status_combo
    ):

        new_status = status_combo.get().strip()

        if new_status not in (
            "Available",
            "Occupied",
            "Reserved"
        ):
            messagebox.showwarning(
                "Invalid Status",
                "Please select a valid table status."
            )
            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE cafe_tables
                SET status = ?
                WHERE id = ?
            """, (
                new_status,
                table_id
            ))

            connection.commit()
            connection.close()

            self.load_tables()

        except Exception as error:

            messagebox.showerror(
                "Update Error",
                f"Could not update table status.\n\n{error}"
            )
