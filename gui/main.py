# gui/main.py
# this controls navigation
# root is repairs so i can test it for now.



import tkinter as tk

# when running as a package module (python -m gui.main) use a relative import;
# if the file is executed directly (not recommended) fall back to absolute.
try:
    from .page_repairs import RepairsPage
except ImportError:
    # executed as a script from the gui directory
    from page_repairs import RepairsPage


def main():
    root = tk.Tk()
    root.title("Paragon Apartment Repairs")
    root.geometry("1000x700")

    repairs_page = RepairsPage(root)
    repairs_page.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()


######### controls what is showing when. we need a navbar to copy paste
# login page has no nav
# after login, go to relevant dashboard
# dashboard has nav, which should accept a callback to switch to other pages




""" import tkinter as tk
from gui.page_login import LoginPage
from gui.page_repairs import RepairsPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Maintenance System")
        self.geometry("900x600")

        self.current_page = None
        self.show_login()

    def clear_page(self):
        if self.current_page:
            self.current_page.destroy()

    def show_login(self):
        self.clear_page()
        self.current_page = LoginPage(self, self.show_repairs)
        self.current_page.pack(fill="both", expand=True)

    def show_repairs(self):
        self.clear_page()
        self.current_page = RepairsPage(self)
        self.current_page.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop() """