# gui/main.py
import tkinter as tk
from gui.page_repairs import RepairsPage

root = tk.Tk()
root.title("Paragon Apartment Repairs")
root.geometry("600x400")

repairs_page = RepairsPage(root)
repairs_page.pack(fill="both", expand=True)

root.mainloop()