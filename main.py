import customtkinter as ctk
from gui.reports_view import ReportsView
from gui.finance_view import FinanceView
from gui.payment_page import PaymentPage
import theme

class PAMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Paragon Apartment Management System")
        self.geometry("1200x700")
        ctk.set_appearance_mode("light")

        # Configure grid
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_content()
        self.show_view("Reports")

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=theme.PRIMARY, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        logo = ctk.CTkLabel(self.sidebar, text="PAMS", font=("Helvetica", 28, "bold"),
                            text_color="white")
        logo.pack(pady=(30, 40))

        nav_buttons = [
            ("Reports", "Reports"),
            ("Finance", "Finance"),
            ("Payments", "Payments"),
        ]

        self.nav_buttons = {}
        for text, name in nav_buttons:
            btn = ctk.CTkButton(self.sidebar, text=text,
                                command=lambda n=name: self.show_view(n),
                                fg_color="transparent", hover_color=theme.PRIMARY_DARK,
                                text_color="white", anchor="w", height=40, corner_radius=0)
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[name] = btn

    def _create_main_content(self):
        self.content_frame = ctk.CTkFrame(self, fg_color=theme.BACKGROUND, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.views = {}

    def show_view(self, view_name):
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.configure(fg_color=theme.PRIMARY_DARK)
            else:
                btn.configure(fg_color="transparent")

        if view_name not in self.views:
            if view_name == "Reports":
                self.views[view_name] = ReportsView(self.content_frame, self)
            elif view_name == "Finance":
                self.views[view_name] = FinanceView(self.content_frame, self)
            elif view_name == "Payments":
                self.views[view_name] = PaymentPage(self.content_frame, self)

            if view_name in self.views:
                self.views[view_name].grid(row=0, column=0, sticky="nsew")

        if view_name in self.views:
            self.views[view_name].tkraise()

if __name__ == "__main__":
    app = PAMSApp()
    app.mainloop()