# top nav ...
from tkinter import *

BG_COLOR = "#f5f3ff"
NAV_COLOR = "#ffffff"
TEXT_COLOR = "#1f1f1f"
ACCENT_COLOR = "#7c3aed"

FONT_BTN = ("Segoe UI", 10, "bold")


def navbar(root, show_dashboard, show_repairs, show_complaints):

    root.configure(bg=BG_COLOR)

    nav = Frame(root, bg=NAV_COLOR, height=60)
    nav.pack(fill="x")

    Button(
        nav,
        text="Dashboard",
        font=FONT_BTN,
        bg=NAV_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        command=show_dashboard
    ).pack(side="left", padx=20, pady=15)

    Button(
        nav,
        text="Repairs",
        font=FONT_BTN,
        bg=NAV_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        command=show_repairs
    ).pack(side="left", padx=20)

    Button(
        nav,
        text="Complaints",
        font=FONT_BTN,
        bg=NAV_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        command=show_complaints
    ).pack(side="left", padx=20)

    content = Frame(root, bg=BG_COLOR)
    content.pack(fill="both", expand=True)

    return content