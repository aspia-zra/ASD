from tkinter import *
from . import Admindash, settings

#Themes- work on font
BG_COLOR = "#f5f3ff"
SIDEBAR_COLOR = "#ede9fe"
CARD_COLOR = "#ffffff"
ACCENT_COLOR = "#7c3aed"
SUB_ACCENT = "#a78bfa"
TEXT_COLOR = "#1f1f1f"
ENTRY_BG = "#f3e8ff"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")

# Left handside Navbar section
def navbar(main):
    sidebar = Frame(main, bg=SIDEBAR_COLOR, width=220)
    sidebar.pack(side="left", fill="y")


    card = Frame(sidebar, bg=CARD_COLOR)
    card.pack(padx=10, pady=10, fill="both")

    form = Frame(card, bg=CARD_COLOR)
    form.pack(padx=30, pady=30)

    Button(card, text="Register Tenant", font=FONT_BTN,
              bg=ACCENT_COLOR, fg="white", width=20,
              relief="flat", command=open_settings).pack(pady=20)

    # Logo Section
    logo_frame = Frame(sidebar, bg=SIDEBAR_COLOR)
    logo_frame.pack(pady=20)

    profile_label = Label(
        logo_frame,
        text="+",
        font=("Helvetica", 28),
        bg=SIDEBAR_COLOR,
        fg=TEXT_COLOR
    )
    profile_label.pack(side="left", padx=10)

    text_label = Label(
        logo_frame,
        text="Paragon\nApartments",
        bg=SIDEBAR_COLOR,
        fg=TEXT_COLOR,
        font=("Helvetica", 18, "bold")
    )
    text_label.pack(pady=20)
    text_label.pack(padx=5)

    ## Dashhboard button
    submitdash = Button(sidebar, 
        text="Dashboard", 
        bg=SIDEBAR_COLOR, 
        fg=TEXT_COLOR,
        command=lambda: open_admindash(main))
    submitdash.pack(pady=10)
    submitdash.bind("<Enter>", lambda e: submitdash.config(bg=SUB_ACCENT))
    submitdash.bind("<Leave>", lambda e: submitdash.config(bg=SUB_ACCENT))

    ## Settings button
    submitsettings = Button(sidebar, 
        text="Settings", 
        bg=SIDEBAR_COLOR, 
        fg=TEXT_COLOR,
        relief= FLAT, 
        bd =0,
        command=lambda: open_settings(main))
    submitsettings.pack(pady=10)
    submitsettings.bind("<Enter>", lambda e: submitsettings.config(bg=SUB_ACCENT))
    submitsettings.bind("<Leave>", lambda e: submitsettings.config(bg=SUB_ACCENT))

    container = Frame(main, bg=BG_COLOR)
    container.pack(side="right", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    return container

# Functions to connect to other pages
def open_admindash(main):
    for widget in main.winfo_children():
        widget.destroy()
    
    Admindash.dashboard(main)

def open_settings(main):
    for widget in main.winfo_children():
        widget.destroy()
    
    settings.settings(main)