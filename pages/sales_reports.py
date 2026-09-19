import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

from database import get_connection


class SalesReports(ctk.CTkFrame):
    """Sales and reports page backed by the café SQLite database."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="#F6F1E9")
        self.period = ctk.StringVar(value="Last 7 Days")
        self.build_ui()

    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color="#3A2418", corner_radius=18, height=112)
        header.pack(fill="x", padx=24, pady=(22, 15))
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="📈  Sales & Reports",
                     font=ctk.CTkFont(size=29, weight="bold"),
                     text_color="#FFF8F0").place(x=25, y=20)
        ctk.CTkLabel(header, text="Track revenue, orders and best-selling items",
                     font=ctk.CTkFont(size=14), text_color="#E8D8C8").place(x=27, y=67)

        filter_box = ctk.CTkComboBox(header, values=["Today", "Last 7 Days", "Last 30 Days"],
                                     variable=self.period, width=145, height=36,
                                     corner_radius=9, fg_color="#FFF8F0",
                                     button_color="#8A5A32", button_hover_color="#70452D",
                                     text_color="#3A2418", command=lambda _: self.refresh())
        filter_box.place(relx=1, x=-25, y=38, anchor="e")

        self.summary = ctk.CTkFrame(self, fg_color="transparent")
        self.summary.pack(fill="x", padx=24, pady=(0, 15))

        self.revenue_card = self.card(self.summary, "₹", "Revenue", "₹0")
        self.revenue_card.pack(side="left", fill="x", expand=True, padx=(0, 7))
        self.orders_card = self.card(self.summary, "▣", "Orders", "0")
        self.orders_card.pack(side="left", fill="x", expand=True, padx=7)
        self.avg_card = self.card(self.summary, "↗", "Average Order", "₹0")
        self.avg_card.pack(side="left", fill="x", expand=True, padx=7)
        self.customers_card = self.card(self.summary, "♟", "Customers", "0")
        self.customers_card.pack(side="left", fill="x", expand=True, padx=(7, 0))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        self.chart_card = ctk.CTkFrame(body, fg_color="#FFFFFF", corner_radius=16)
        self.chart_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        ctk.CTkLabel(self.chart_card, text="Revenue Overview",
                     font=ctk.CTkFont(size=19, weight="bold"),
                     text_color="#302017").pack(anchor="w", padx=20, pady=(18, 2))
        self.chart_subtitle = ctk.CTkLabel(self.chart_card, text="",
                                          font=ctk.CTkFont(size=11), text_color="#91837A")
        self.chart_subtitle.pack(anchor="w", padx=20)
        self.chart = ctk.CTkCanvas(self.chart_card, bg="#FFFFFF", highlightthickness=0, height=300)
        self.chart.pack(fill="both", expand=True, padx=15, pady=12)
        self.chart.bind("<Configure>", lambda e: self.draw_chart())

        self.top_card = ctk.CTkFrame(body, width=340, fg_color="#FFFFFF", corner_radius=16)
        self.top_card.pack(side="right", fill="y", padx=(8, 0))
        self.top_card.pack_propagate(False)
        ctk.CTkLabel(self.top_card, text="🏆  Best Selling Items",
                     font=ctk.CTkFont(size=19, weight="bold"), text_color="#302017").pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(self.top_card, text="Based on quantity sold",
                     font=ctk.CTkFont(size=11), text_color="#91837A").pack(anchor="w", padx=20, pady=(0, 10))

        bottom = ctk.CTkFrame(self, fg_color="transparent", height=225)
        bottom.pack(fill="x", padx=24, pady=(0, 20))
        bottom.pack_propagate(False)

        self.breakdown = ctk.CTkFrame(bottom, fg_color="#FFFFFF", corner_radius=16)
        self.breakdown.pack(side="left", fill="both", expand=True, padx=(0, 8))
        ctk.CTkLabel(self.breakdown, text="Order Breakdown",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#302017").pack(anchor="w", padx=20, pady=(15, 8))
        self.breakdown_content = ctk.CTkFrame(self.breakdown, fg_color="transparent")
        self.breakdown_content.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        self.recent = ctk.CTkFrame(bottom, width=510, fg_color="#FFFFFF", corner_radius=16)
        self.recent.pack(side="right", fill="both", padx=(8, 0))
        self.recent.pack_propagate(False)
        ctk.CTkLabel(self.recent, text="Recent Sales",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#302017").pack(anchor="w", padx=20, pady=(15, 8))
        self.recent_content = ctk.CTkFrame(self.recent, fg_color="transparent")
        self.recent_content.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.data = {"dates": [], "sales": [], "top": [], "types": {}, "statuses": {}, "recent": []}
        self.refresh()

    def card(self, parent, icon, title, value):
        frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15, height=88)
        frame.pack_propagate(False)
        ctk.CTkLabel(frame, text=icon, font=ctk.CTkFont(size=23), text_color="#7A4E2D").place(x=16, y=18)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=10), text_color="#8A7A6E").place(x=55, y=14)
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=20, weight="bold"), text_color="#3A2418")
        label.place(x=55, y=38)
        frame.value_label = label
        return frame

    def days_for_period(self):
        return {"Today": 1, "Last 7 Days": 7, "Last 30 Days": 30}[self.period.get()]

    def refresh(self):
        try:
            days = self.days_for_period()
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COALESCE(SUM(total),0), COUNT(*), COALESCE(AVG(total),0) FROM orders WHERE date(created_at) >= date('now','localtime',?)", (f'-{days-1} day',))
            revenue, order_count, average = cur.fetchone()
            cur.execute("SELECT COUNT(DISTINCT user_id) FROM orders WHERE user_id IS NOT NULL AND date(created_at) >= date('now','localtime',?)", (f'-{days-1} day',))
            customers = cur.fetchone()[0] or 0

            cur.execute("SELECT date(created_at), COALESCE(SUM(total),0) FROM orders WHERE date(created_at) >= date('now','localtime',?) GROUP BY date(created_at) ORDER BY date(created_at)", (f'-{days-1} day',))
            rows = cur.fetchall()
            sales_map = {str(d): float(v or 0) for d, v in rows}
            dates, sales = [], []
            for i in range(days-1, -1, -1):
                d = datetime.now() - timedelta(days=i)
                key = d.strftime('%Y-%m-%d')
                dates.append(d.strftime('%d %b') if days <= 7 else d.strftime('%d'))
                sales.append(sales_map.get(key, 0))

            cur.execute("""SELECT menu.name, SUM(order_items.quantity) qty
                           FROM order_items JOIN menu ON menu.id=order_items.menu_id
                           JOIN orders ON orders.id=order_items.order_id
                           WHERE date(orders.created_at) >= date('now','localtime',?)
                           GROUP BY order_items.menu_id ORDER BY qty DESC LIMIT 5""", (f'-{days-1} day',))
            top = cur.fetchall()

            cur.execute("SELECT order_type, COUNT(*), COALESCE(SUM(total),0) FROM orders WHERE date(created_at) >= date('now','localtime',?) GROUP BY order_type", (f'-{days-1} day',))
            types = cur.fetchall()

            cur.execute("SELECT status, COUNT(*) FROM orders WHERE date(created_at) >= date('now','localtime',?) GROUP BY status", (f'-{days-1} day',))
            statuses = cur.fetchall()

            cur.execute("SELECT id, order_type, total, status, created_at FROM orders ORDER BY id DESC LIMIT 5")
            recent = cur.fetchall()
            conn.close()

            self.data = {"dates": dates, "sales": sales, "top": top, "types": types, "statuses": statuses, "recent": recent}
            self.revenue_card.value_label.configure(text=f"₹{float(revenue or 0):,.0f}")
            self.orders_card.value_label.configure(text=str(order_count or 0))
            self.avg_card.value_label.configure(text=f"₹{float(average or 0):,.0f}")
            self.customers_card.value_label.configure(text=str(customers))
            self.chart_subtitle.configure(text=f"Revenue · {self.period.get()}")
            self.render_top()
            self.render_breakdown()
            self.render_recent()
            self.draw_chart()
        except Exception as e:
            messagebox.showerror("Sales Report Error", str(e))

    def render_top(self):
        for w in self.top_card.winfo_children()[2:]: w.destroy()
        top = self.data["top"]
        if not top:
            ctk.CTkLabel(self.top_card, text="No sales data yet", text_color="#897A70").pack(pady=35)
            return
        for i, (name, qty) in enumerate(top, 1):
            row = ctk.CTkFrame(self.top_card, fg_color="#FBF8F3", corner_radius=10)
            row.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(row, text=f"{i}", width=30, font=ctk.CTkFont(size=12, weight="bold"), text_color="#7A4E2D").pack(side="left", padx=8, pady=8)
            ctk.CTkLabel(row, text=name, font=ctk.CTkFont(size=11, weight="bold"), text_color="#3D2A20").pack(side="left")
            ctk.CTkLabel(row, text=f"{int(qty)} sold", font=ctk.CTkFont(size=10), text_color="#897A70").pack(side="right", padx=10)

    def render_breakdown(self):
        for w in self.breakdown_content.winfo_children(): w.destroy()
        left = ctk.CTkFrame(self.breakdown_content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)
        right = ctk.CTkFrame(self.breakdown_content, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)
        ctk.CTkLabel(left, text="Order Type", font=ctk.CTkFont(size=10, weight="bold"), text_color="#8A7A6E").pack(anchor="w")
        for typ, count, amount in self.data["types"]:
            ctk.CTkLabel(left, text=f"{typ}: {count}  ·  ₹{amount:,.0f}", font=ctk.CTkFont(size=11), text_color="#4A392D").pack(anchor="w", pady=3)
        ctk.CTkLabel(right, text="Status", font=ctk.CTkFont(size=10, weight="bold"), text_color="#8A7A6E").pack(anchor="w")
        for status, count in self.data["statuses"]:
            ctk.CTkLabel(right, text=f"{status}: {count}", font=ctk.CTkFont(size=11), text_color="#4A392D").pack(anchor="w", pady=3)

    def render_recent(self):
        for w in self.recent_content.winfo_children(): w.destroy()
        for oid, typ, total, status, created in self.data["recent"]:
            row = ctk.CTkFrame(self.recent_content, fg_color="#FBF8F3", corner_radius=8, height=30)
            row.pack(fill="x", pady=3)
            row.pack_propagate(False)
            ctk.CTkLabel(row, text=f"#{oid}", width=45, font=ctk.CTkFont(size=10, weight="bold"), text_color="#65412E").pack(side="left")
            ctk.CTkLabel(row, text=typ, width=85, font=ctk.CTkFont(size=10), text_color="#4A392D").pack(side="left")
            ctk.CTkLabel(row, text=f"₹{float(total):,.0f}", width=80, font=ctk.CTkFont(size=10, weight="bold"), text_color="#3D2A20").pack(side="left")
            ctk.CTkLabel(row, text=status, font=ctk.CTkFont(size=10, weight="bold"), text_color="#7A4E2D").pack(side="right", padx=8)

    def draw_chart(self):
        if not hasattr(self, 'chart') or not self.chart.winfo_exists(): return
        self.chart.delete('all')
        w = max(self.chart.winfo_width(), 500); h = max(self.chart.winfo_height(), 260)
        values = self.data.get('sales', [])
        labels = self.data.get('dates', [])
        if not values: return
        max_v = max(values) or 1
        left, right, top, bottom = 50, 20, 20, 45
        plot_w, plot_h = w-left-right, h-top-bottom
        self.chart.create_line(left, top, left, h-bottom, fill="#D9C9BA")
        self.chart.create_line(left, h-bottom, w-right, h-bottom, fill="#D9C9BA")
        n = len(values); step = plot_w / max(n, 1)
        bar_w = min(42, step*0.55)
        for i, val in enumerate(values):
            x = left + step*i + (step-bar_w)/2
            bh = (val/max_v)*(plot_h-20)
            y = h-bottom-bh
            self.chart.create_rectangle(x, y, x+bar_w, h-bottom, fill="#8A5A32", outline="")
            self.chart.create_text(x+bar_w/2, y-10, text=f"₹{val:,.0f}", fill="#5F5148", font=("Arial",8,"bold"))
            self.chart.create_text(x+bar_w/2, h-bottom+17, text=labels[i], fill="#897A70", font=("Arial",8))


if __name__ == '__main__':
    app = ctk.CTk(); app.title('Brew & Bytes - Sales & Reports'); app.geometry('1250x800'); app.minsize(1050,700)
    SalesReports(app).pack(fill='both', expand=True); app.mainloop()
