
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

from gui.login_page import LoginPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Paragon Apartment System")
        self.geometry("1000x700")
        self.minsize(800, 600)

        self.current_page = None
        self.show_login()

    def clear_page(self):
        if self.current_page != None:
            self.current_page.destroy()

    def show_login(self):
        self.clear_page()
        self.current_page = LoginPage(self, self.show_dashboard)
        self.current_page.pack(fill="both", expand=True)
    
    # add dashboard page based on role

    def show_dashboard(self, user):
        self.clear_page()

        dashboard = ctk.CTkFrame(self)
        dashboard.pack(fill="both", expand=True)

        welcome_text = "Welcome " + user["fullName"] + " - " + user["Role"]

        ctk.CTkLabel(
            dashboard,
            text=welcome_text,
            font=("Arial", 22)
        ).pack(pady=100)

        self.current_page = dashboard


if __name__ == "__main__":
    app = App()
    app.mainloop()
