from tkinter import messagebox
import customtkinter as ctk

from . import Admindash, settings, finance_view
from .ReportsFrontVer import adminreportView, managerreportView, financereportView, maintreportView
from .pages_mngdash import mngdashboard
from models import user_session
from models.front_desk import FrontDesk
from . import theme, page_mdash

BG_COLOR = theme.BACKGROUND


class navbar(ctk.CTkFrame):
    def __init__(self, parent, controller, mode="manager"):
        super().__init__(parent, fg_color=theme.SECONDARY)
        self.controller = controller
        self.mode = mode
        self.model = FrontDesk()

        self.grid(row=0, column=0, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_navbar()

    def create_navbar(self):
        mode = getattr(self.controller, "navbar_mode", self.mode)
        mode = str(mode or "").lower()

        if mode == "admin":
            self.admin_nav()
            return

        if mode in {"management", "manager"}:
            self.mng_nav()
            return

        if mode == "frontdesk":
            self.front_nav()
            return
        
        if mode == "finance":
            self.finance_nav()
            return

        self.maintenance_dashboard_nav()

    def _reset_navbar(self):
        if hasattr(self, "navbar") and self.navbar.winfo_exists():
            self.navbar.destroy()

        self.navbar = ctk.CTkFrame(self, fg_color="transparent")
        self.navbar.grid(row=0, column=0, sticky="ns")
        self.navbar.grid_rowconfigure(7, weight=1)
        self.navbar.grid_columnconfigure(0, weight=1)

        navtitle_label = ctk.CTkLabel(
            self.navbar,
            text="Paragon Apartments",
            fg_color="transparent",
            text_color=theme.PRIMARY,
            font=(theme.TITLE_FONT, 20),
        )
        navtitle_label.grid(row=0, column=0, padx=20, pady=(20, 40), sticky="w")

    def _nav_button_config(self):
        return {
            "fg_color": theme.PRIMARY,
            "hover_color": theme.PRIMARY_DARK,
            "text_color": theme.SURFACE,
            "height": 40,
            "corner_radius": 8,
            "anchor": "w",
        }

    def _invoke_controller(self, *method_names):
        for method_name in method_names:
            method = getattr(self.controller, method_name, None)
            if callable(method):
                host = getattr(self.controller, "root", None)
                if host is not None and hasattr(host, "after_idle"):
                    host.after_idle(method)
                else:
                    self.after_idle(method)
                return True

        return False

    def admin_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()

        ctk.CTkButton(self.navbar, command=self.open_admindash, text="Dashboard", **btnConfig).grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_adminreports, text="Reports View", **btnConfig).grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_maintdash, text="Maintenance View", **btnConfig).grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_financedash, text="Finance View", **btnConfig).grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_frontdash, text="Front-desk View", **btnConfig).grid(row=5, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_settings, text="Settings", **btnConfig).grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, fg_color=theme.PRIMARY, hover_color=theme.DANGER, text="Logout", command=self.logoutbtn).grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def mng_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()

        if user_session.user_type == "manager":
            dashboard_text = "Apartment Management"
            dashboard_command = self.open_mngdash
        else:
            dashboard_text = "Dashboard"
            dashboard_command = self.open_admindash

        ctk.CTkButton(self.navbar, command=dashboard_command, text=dashboard_text, **btnConfig).grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_managerReports, text="Reports View", **btnConfig).grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_maintdash, text="Maintenance View", **btnConfig).grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_financedash, text="Finance View", **btnConfig).grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_frontdash, text="Front-desk View", **btnConfig).grid(row=5, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_settings, text="Settings", **btnConfig).grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, fg_color=theme.PRIMARY, hover_color=theme.DANGER, text="Logout", command=self.logoutbtn).grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def maintenance_dashboard_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()

        ctk.CTkButton(self.navbar, command=self.open_maintdash, text="Maintenance Dashboard", **btnConfig).grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_complaints, text="Complaints", **btnConfig).grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_repairs, text="Repairs", **btnConfig).grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_settings, text="Settings", **btnConfig).grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, fg_color=theme.PRIMARY, hover_color=theme.DANGER, text="Logout", command=self.logoutbtn).grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def front_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()

        ctk.CTkButton(self.navbar, command=self.open_frontdash, text="Dashboard", **btnConfig).grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_complaints, text="Complaints", **btnConfig).grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_repairs, text="Repairs", **btnConfig).grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_assign_apartment, text="Assign Apartment", **btnConfig).grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, fg_color=theme.PRIMARY, hover_color=theme.DANGER, text="Logout", command=self.logoutbtn).grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def finance_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()

        ctk.CTkButton(self.navbar, command=self.open_financedash, text="Finance Dashboard", **btnConfig).grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_financeReports, text="Reports", **btnConfig).grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_payments, text="Payments", **btnConfig).grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_settings, text="Settings", **btnConfig).grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, fg_color=theme.PRIMARY, hover_color=theme.DANGER, text="Logout", command=self.logoutbtn).grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def open_mngdash(self):
        self.controller.clear_page()
        self.controller.current_page = mngdashboard(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_admindash(self):
        if self._invoke_controller("show_admin_dashboard", "show_dashboard"):
            return
        self.controller.clear_page()
        self.controller.current_page = Admindash.admindashboard(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_adminreports(self):
        self.controller.clear_page()
        self.controller.current_page = adminreportView.ReportsView(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_managerReports(self):
        self.controller.clear_page()
        self.controller.current_page = managerreportView.ReportsView(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_financeReports(self):
        self.controller.clear_page()
        self.controller.current_page = financereportView.ReportsView(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_maintReports(self):
        self.controller.clear_page()
        self.controller.current_page = maintreportView.ReportsView(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_maintdash(self):
        if self._invoke_controller("open_maintenance_dashboard", "show_maintenance_dashboard"):
            return
        self.controller.clear_page()
        self.controller.current_page = page_mdash.DashboardPage(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_financedash(self):
        self.controller.clear_page()
        self.controller.current_page = finance_view.FinanceView(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_payments(self):
        from gui.payment_page import PaymentPage
        self.controller.clear_page()
        self.controller.current_page = PaymentPage(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_frontdash(self):
        from .updatedfrontdesk import FrontDeskGUI
        self.controller.clear_page()
        self.controller.current_page = FrontDeskGUI(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_settings(self):
        if self._invoke_controller("show_settings", "open_settings"):
            return
        self.controller.clear_page()
        self.controller.current_page = settings.settings(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_assign_apartment(self):
        from .page_assign_apartment import AssignApartmentPage
        self.controller.clear_page()
        self.controller.current_page = AssignApartmentPage(self.controller, self.controller, self.model)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_repairs(self):
        self._invoke_controller("show_repairs", "open_repairs", "open_repairs_page")

    def open_complaints(self):
        self._invoke_controller("show_complaints", "open_complaints", "open_complaints_page")

    def logoutbtn(self):
        if self._invoke_controller("logout", "show_login"):
            return
        messagebox.showinfo("Logout", "Logout action is not available yet.")
       
       
         
