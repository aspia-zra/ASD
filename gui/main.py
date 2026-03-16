import tkinter as tk
from db.db_connect import Database
from gui.mnav import navbar
from gui.page_mdash import dashboard
from gui.page_repairs import RepairsPage
from gui.page_complaints import ComplaintsPage


class App:

    def __init__(self, root, db):

        self.root = root
        self.db = db

        self.content = root
        self.show_dashboard()


    def clear(self):

        for w in self.content.winfo_children():
            w.destroy()

    def show_dashboard(self):

        self.clear()
        dashboard(self.content, self.db)

    def show_repairs(self):

        self.clear()
        RepairsPage(self.content, self.db).pack(fill="both", expand=True)

    def show_complaints(self):

        self.clear()
        ComplaintsPage(self.content, self.db).pack(fill="both", expand=True)


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Maintenance System")
    root.geometry("1000x700")

    db = Database()

    App(root, db)

    root.mainloop()