import customtkinter as ctk
from tkinter import ttk
from controllers.report_controller import ReportController
import theme

class ReportsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=theme.BACKGROUND)
        self.controller = controller
        self.report_controller = ReportController()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()
        self._create_tab_view()

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color=theme.SURFACE, height=80, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", pady=(0,20))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Reports Dashboard", font=theme.TITLE_FONT,
                     text_color=theme.PRIMARY).grid(row=0, column=0, pady=20)

    def _create_tab_view(self):
        self.tab_view = ctk.CTkTabview(self, fg_color=theme.BACKGROUND,
                                        segmented_button_fg_color=theme.SURFACE,
                                        segmented_button_selected_color=theme.PRIMARY,
                                        segmented_button_selected_hover_color=theme.PRIMARY_DARK,
                                        text_color=theme.TEXT_PRIMARY)
        self.tab_view.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.tab_view.add("Occupancy")
        self.tab_view.add("Financial")
        self.tab_view.add("Maintenance")
        self.tab_view.add("Complaints")
        self._configure_occupancy_tab()
        self._configure_financial_tab()
        self._configure_maintenance_tab()
        self._configure_complaints_tab()

    def _configure_occupancy_tab(self):
        tab = self.tab_view.tab("Occupancy")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        filter_frame = ctk.CTkFrame(tab, fg_color=theme.SURFACE, corner_radius=10)
        filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        filter_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(filter_frame, text="Filter by City:", font=theme.BODY_FONT,
                     text_color=theme.TEXT_PRIMARY).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        cities = ["All", "Bristol", "Cardiff", "London", "Manchester"]
        self.city_var = ctk.StringVar(value="All")
        ctk.CTkComboBox(filter_frame, values=cities, variable=self.city_var,
                        command=self._load_occupancy_data,
                        fg_color=theme.BACKGROUND, border_color=theme.PRIMARY_LIGHT,
                        button_color=theme.PRIMARY, button_hover_color=theme.PRIMARY_DARK
                        ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        table_frame = ctk.CTkFrame(tab, fg_color=theme.SURFACE, corner_radius=10)
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        columns = ("Apartment", "Type", "Status", "City", "Tenant")
        self.occupancy_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=theme.BACKGROUND, foreground=theme.TEXT_PRIMARY,
                        rowheight=30, fieldbackground=theme.BACKGROUND)
        style.configure("Treeview.Heading", background=theme.PRIMARY, foreground="white",
                        relief="flat", font=theme.BODY_FONT)
        for col in columns:
            self.occupancy_tree.heading(col, text=col)
            self.occupancy_tree.column(col, width=120, anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.occupancy_tree.yview)
        self.occupancy_tree.configure(yscrollcommand=scrollbar.set)
        self.occupancy_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._load_occupancy_data()

    def _load_occupancy_data(self, *args):
        city = None if self.city_var.get() == "All" else self.city_var.get()
        data = self.report_controller.get_occupancy_data(city)
        for row in self.occupancy_tree.get_children():
            self.occupancy_tree.delete(row)
        for item in data:
            self.occupancy_tree.insert("", "end", values=(
                item['apartment'], item['type'], item['status'],
                item['city'], item['tenant']
            ))

    def _configure_financial_tab(self):
        tab = self.tab_view.tab("Financial")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        self._create_financial_summary(tab)
        table_frame = ctk.CTkFrame(tab, fg_color=theme.SURFACE, corner_radius=10)
        table_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        columns = ("Invoice", "Amount", "Due Date", "Status", "Tenant")
        self.financial_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        style = ttk.Style()
        style.configure("Treeview", background=theme.BACKGROUND, foreground=theme.TEXT_PRIMARY,
                        rowheight=30, fieldbackground=theme.BACKGROUND)
        style.configure("Treeview.Heading", background=theme.PRIMARY, foreground="white",
                        relief="flat", font=theme.BODY_FONT)
        for col in columns:
            self.financial_tree.heading(col, text=col)
            self.financial_tree.column(col, width=120, anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.financial_tree.yview)
        self.financial_tree.configure(yscrollcommand=scrollbar.set)
        self.financial_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._load_financial_data()

    def _create_financial_summary(self, parent):
        data, _ = self.report_controller.get_financial_data()
        summary_frame = ctk.CTkFrame(parent, fg_color=theme.SURFACE, corner_radius=10)
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        for i in range(4):
            summary_frame.grid_columnconfigure(i, weight=1)
        self.financial_summary_labels = {}
        titles = ["Total Outstanding", "Pending", "Overdue", "Paid"]
        for i, title in enumerate(titles):
            card = ctk.CTkFrame(summary_frame, fg_color=theme.BACKGROUND, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(card, text=title, font=theme.SMALL_FONT,
                         text_color=theme.TEXT_SECONDARY).pack(pady=(10,0))
            label = ctk.CTkLabel(card, text="£0.00", font=theme.HEADING_FONT,
                                 text_color=theme.PRIMARY)
            label.pack(pady=(0,10))
            self.financial_summary_labels[title] = label
        self._update_financial_summary()

    def _update_financial_summary(self):
        data, summary = self.report_controller.get_financial_data()
        self.financial_summary_labels["Total Outstanding"].configure(text=summary['total_outstanding'])
        self.financial_summary_labels["Pending"].configure(text=summary['total_pending'])
        self.financial_summary_labels["Overdue"].configure(text=summary['total_overdue'])
        self.financial_summary_labels["Paid"].configure(text=summary['total_paid'])

    def _load_financial_data(self):
        data, _ = self.report_controller.get_financial_data()
        for row in self.financial_tree.get_children():
            self.financial_tree.delete(row)
        for item in data:
            self.financial_tree.insert("", "end", values=(
                item['invoice'], item['amount'], item['due_date'],
                item['status'], item['tenant']
            ))
        self._update_financial_summary()

    def _configure_maintenance_tab(self):
        tab = self.tab_view.tab("Maintenance")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        self._create_maintenance_summary(tab)
        table_frame = ctk.CTkFrame(tab, fg_color=theme.SURFACE, corner_radius=10)
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        columns = ("Log ID", "Apartment", "Date", "Hours", "Cost", "Notes")
        self.maintenance_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        style = ttk.Style()
        style.configure("Treeview", background=theme.BACKGROUND, foreground=theme.TEXT_PRIMARY,
                        rowheight=30, fieldbackground=theme.BACKGROUND)
        style.configure("Treeview.Heading", background=theme.PRIMARY, foreground="white",
                        relief="flat", font=theme.BODY_FONT)
        for col in columns:
            self.maintenance_tree.heading(col, text=col)
            self.maintenance_tree.column(col, width=100, anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.maintenance_tree.yview)
        self.maintenance_tree.configure(yscrollcommand=scrollbar.set)
        self.maintenance_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._load_maintenance_data()

    def _create_maintenance_summary(self, parent):
        data, summary = self.report_controller.get_maintenance_data()
        summary_frame = ctk.CTkFrame(parent, fg_color=theme.SURFACE, corner_radius=10)
        summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        for i in range(3):
            summary_frame.grid_columnconfigure(i, weight=1)
        self.maintenance_summary_labels = {}
        titles = ["Total Cost", "Total Hours", "Avg Cost/Hour"]
        values = [summary['total_cost'], str(summary['total_hours']), summary['avg_cost_per_hour']]
        for i, title in enumerate(titles):
            card = ctk.CTkFrame(summary_frame, fg_color=theme.BACKGROUND, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(card, text=title, font=theme.SMALL_FONT,
                         text_color=theme.TEXT_SECONDARY).pack(pady=(10,0))
            label = ctk.CTkLabel(card, text=values[i], font=theme.HEADING_FONT,
                                 text_color=theme.PRIMARY)
            label.pack(pady=(0,10))
            self.maintenance_summary_labels[title] = label

    def _load_maintenance_data(self):
        data, summary = self.report_controller.get_maintenance_data()
        for row in self.maintenance_tree.get_children():
            self.maintenance_tree.delete(row)
        for item in data:
            self.maintenance_tree.insert("", "end", values=(
                item['log_id'], item['apartment'], item['date'],
                item['hours'], item['cost'], item['notes']
            ))
        self.maintenance_summary_labels["Total Cost"].configure(text=summary['total_cost'])
        self.maintenance_summary_labels["Total Hours"].configure(text=str(summary['total_hours']))
        self.maintenance_summary_labels["Avg Cost/Hour"].configure(text=summary['avg_cost_per_hour'])

    def _configure_complaints_tab(self):
        tab = self.tab_view.tab("Complaints")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        self._create_complaint_summary(tab)
        table_frame = ctk.CTkFrame(tab, fg_color=theme.SURFACE, corner_radius=10)
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        columns = ("ID", "Description", "Severity", "Status", "Date", "Tenant")
        self.complaint_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        style = ttk.Style()
        style.configure("Treeview", background=theme.BACKGROUND, foreground=theme.TEXT_PRIMARY,
                        rowheight=30, fieldbackground=theme.BACKGROUND)
        style.configure("Treeview.Heading", background=theme.PRIMARY, foreground="white",
                        relief="flat", font=theme.BODY_FONT)
        for col in columns:
            self.complaint_tree.heading(col, text=col)
            self.complaint_tree.column(col, width=120, anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.complaint_tree.yview)
        self.complaint_tree.configure(yscrollcommand=scrollbar.set)
        self.complaint_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._load_complaint_data()

    def _create_complaint_summary(self, parent):
        data, summary = self.report_controller.get_complaint_data()
        summary_frame = ctk.CTkFrame(parent, fg_color=theme.SURFACE, corner_radius=10)
        summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        for i in range(4):
            summary_frame.grid_columnconfigure(i, weight=1)
        self.complaint_summary_labels = {}
        titles = ["Total", "Open", "High Severity", "Medium Severity"]
        values = [summary['total'], summary['open'], summary['severity_high'], summary['severity_medium']]
        for i, title in enumerate(titles):
            card = ctk.CTkFrame(summary_frame, fg_color=theme.BACKGROUND, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(card, text=title, font=theme.SMALL_FONT,
                         text_color=theme.TEXT_SECONDARY).pack(pady=(10,0))
            label = ctk.CTkLabel(card, text=str(values[i]), font=theme.HEADING_FONT,
                                 text_color=theme.PRIMARY)
            label.pack(pady=(0,10))
            self.complaint_summary_labels[title] = label

    def _load_complaint_data(self):
        data, summary = self.report_controller.get_complaint_data()
        for row in self.complaint_tree.get_children():
            self.complaint_tree.delete(row)
        for item in data:
            self.complaint_tree.insert("", "end", values=(
                item['complaint_id'], item['description'], item['severity'],
                item['status'], item['date'], item['tenant']
            ))
        self.complaint_summary_labels["Total"].configure(text=str(summary['total']))
        self.complaint_summary_labels["Open"].configure(text=str(summary['open']))
        self.complaint_summary_labels["High Severity"].configure(text=str(summary['severity_high']))
        self.complaint_summary_labels["Medium Severity"].configure(text=str(summary['severity_medium']))