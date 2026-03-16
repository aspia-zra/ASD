import customtkinter as ctk
from tkinter import ttk
from controllers.finance_controller import FinanceController
import theme

class FinanceView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=theme.BACKGROUND)
        self.controller = controller
        self.finance_controller = FinanceController()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()
        self._create_scrollable_content()

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color=theme.SURFACE, height=80, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", pady=(0,20))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        ctk.CTkLabel(header, text="Finance Dashboard", font=theme.TITLE_FONT,
                     text_color=theme.PRIMARY).grid(row=0, column=0, pady=20, padx=30, sticky="w")
        refresh_btn = ctk.CTkButton(header, text="↻ Refresh", command=self.refresh_data,
                                     fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_DARK,
                                     text_color="white", width=100, corner_radius=8)
        refresh_btn.grid(row=0, column=1, pady=20, padx=30, sticky="e")

    def _create_scrollable_content(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=theme.BACKGROUND,
                                                    scrollbar_button_color=theme.PRIMARY,
                                                    scrollbar_button_hover_color=theme.PRIMARY_DARK)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self._create_summary_cards()
        self._create_upcoming_dues()
        self._create_recent_transactions()

    def _create_summary_cards(self):
        cards_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        cards_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        self.summary_cards = {}
        titles = ["Total Outstanding", "Pending", "Overdue", "Paid"]
        keys = ["total_outstanding", "pending_total", "overdue_total", "paid_total"]
        for i, (title, key) in enumerate(zip(titles, keys)):
            card = ctk.CTkFrame(cards_frame, fg_color=theme.SURFACE, corner_radius=15)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(card, text=title, font=theme.BODY_FONT,
                         text_color=theme.TEXT_SECONDARY).pack(pady=(15,5))
            label = ctk.CTkLabel(card, text="£0.00", font=("Helvetica", 28, "bold"),
                                 text_color=theme.PRIMARY)
            label.pack(pady=(0,15))
            self.summary_cards[key] = label

        # Collection rate card below
        rate_frame = ctk.CTkFrame(self.scroll_frame, fg_color=theme.SURFACE, corner_radius=15)
        rate_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        rate_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(rate_frame, text="Collection Rate", font=theme.HEADING_FONT,
                     text_color=theme.PRIMARY).pack(pady=(15,10))
        self.collection_rate_label = ctk.CTkLabel(rate_frame, text="0%",
                                                  font=("Helvetica", 36, "bold"),
                                                  text_color=theme.PRIMARY)
        self.collection_rate_label.pack(pady=10)

    def _create_upcoming_dues(self):
        frame = ctk.CTkFrame(self.scroll_frame, fg_color=theme.SURFACE, corner_radius=15)
        frame.grid(row=2, column=0, padx=10, pady=20, sticky="ew")
        ctk.CTkLabel(frame, text="Upcoming Due Dates (Next 7 Days)",
                     font=theme.HEADING_FONT, text_color=theme.PRIMARY).pack(pady=(15,10))

        self.dues_frame = ctk.CTkScrollableFrame(frame, fg_color=theme.BACKGROUND,
                                                  height=150, corner_radius=10)
        self.dues_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def _create_recent_transactions(self):
        frame = ctk.CTkFrame(self.scroll_frame, fg_color=theme.SURFACE, corner_radius=15)
        frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(frame, text="Recent Transactions", font=theme.HEADING_FONT,
                     text_color=theme.PRIMARY).pack(pady=(15,10))

        columns = ("Invoice", "Tenant", "Apartment", "Amount", "Due Date", "Status")
        self.transaction_tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=theme.BACKGROUND, foreground=theme.TEXT_PRIMARY,
                        rowheight=30, fieldbackground=theme.BACKGROUND)
        style.configure("Treeview.Heading", background=theme.PRIMARY, foreground="white",
                        relief="flat", font=theme.BODY_FONT)
        col_widths = [100, 150, 100, 100, 100, 100]
        for col, w in zip(columns, col_widths):
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=w, anchor="center")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        self.transaction_tree.pack(side="left", padx=(20,0), pady=20, fill="both", expand=True)
        scrollbar.pack(side="right", padx=(0,20), pady=20, fill="y")

        self.refresh_data()

    def refresh_data(self):
        summary = self.finance_controller.get_dashboard_summary()
        self.summary_cards["total_outstanding"].configure(text=summary['total_outstanding'])
        self.summary_cards["pending_total"].configure(text=summary['pending_total'])
        self.summary_cards["overdue_total"].configure(text=summary['overdue_total'])
        self.summary_cards["paid_total"].configure(text=summary['paid_total'])
        self.collection_rate_label.configure(text=summary['collection_rate'])

        # Update upcoming dues
        for widget in self.dues_frame.winfo_children():
            widget.destroy()
        dues = self.finance_controller.get_upcoming_due()
        if not dues:
            ctk.CTkLabel(self.dues_frame, text="No upcoming dues",
                         font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY).pack(pady=20)
        else:
            for due in dues:
                item = ctk.CTkFrame(self.dues_frame, fg_color="transparent")
                item.pack(fill="x", padx=5, pady=2)
                details = f"{due['tenant']} - {due['apartment']}"
                ctk.CTkLabel(item, text=details, font=theme.BODY_FONT,
                             text_color=theme.TEXT_PRIMARY, anchor="w").pack(side="left")
                amt_date = f"{due['amount']} (Due: {due['due_date']})"
                ctk.CTkLabel(item, text=amt_date, font=theme.SMALL_FONT,
                             text_color=theme.PRIMARY).pack(side="right")

        # Update transactions
        for row in self.transaction_tree.get_children():
            self.transaction_tree.delete(row)
        trans = self.finance_controller.get_recent_transactions()
        for t in trans:
            self.transaction_tree.insert("", "end", values=(
                t['invoice_id'], t['tenant'], t['apartment'],
                t['amount'], t['due_date'], t['status']
            ), tags=(t['status'].lower(),))
        self.transaction_tree.tag_configure('paid', foreground=theme.SUCCESS)
        self.transaction_tree.tag_configure('pending', foreground=theme.WARNING)
        self.transaction_tree.tag_configure('overdue', foreground=theme.DANGER)