# gui/main.py
# entry point for the application

import tkinter as tk

# imports
from .page_mdash import dashboard
from db.db_connect import Database

def main():

    root = tk.Tk()
    root.title("Paragon Apartment Maintenance")
    root.geometry("1000x700")

    # create database connection
    db = Database()

    # load dashboard first
    dashboard(root, db)

    root.mainloop()


if __name__ == "__main__":
    main()