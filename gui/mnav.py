# navbar for the maintenance dashboard

from tkinter import *
from . import page_mdash, page_repairs

# want to import settings but dont see a settings page bro and a complaints page

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

###################################################################

def navbar(main):
    sidebar = Frame(main, bg=SIDEBAR_COLOR, width=220)
    sidebar.pack(side="left", fill="y")

# im commenting out this code from the original nav for now
    # card = Frame(sidebar, bg=CARD_COLOR)
    # card.pack(padx=10, pady=10, fill="both")

    # form = Frame(card, bg=CARD_COLOR)
    # form.pack(padx=30, pady=30)

    # Button(card, text="Register Tenant", font=FONT_BTN,
    #           bg=ACCENT_COLOR, fg="white", width=20,
    #           relief="flat", command=open_settings).pack(pady=20)

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

    ## BUTTONS
    
    # dashboard button
    submitdash = Button(sidebar, 
        text="Dashboard", 
        bg=SIDEBAR_COLOR, 
        fg=TEXT_COLOR,
        command=lambda: open_mdash(main))
    submitdash.pack(pady=10)
    submitdash.bind("<Enter>", lambda e: submitdash.config(bg=SUB_ACCENT))
    submitdash.bind("<Leave>", lambda e: submitdash.config(bg=SUB_ACCENT))

    # repairs button
    repairsBtn = Button( 
        sidebar, 
        text="Repairs", 
        bg=SIDEBAR_COLOR, 
        fg=TEXT_COLOR, 
        relief=FLAT, 
        command=lambda: open_repairs(main) 
    ) 
    repairsBtn.pack(pady=10, fill="x") 
    repairsBtn.bind("<Enter>", lambda e: repairsBtn.config(bg=SUB_ACCENT)) 
    repairsBtn.bind("<Leave>", lambda e: repairsBtn.config(bg=SIDEBAR_COLOR)) 
        
        
    # complaints button
    complaintsBtn = Button( 
        sidebar, 
        text="Complaints", 
        bg=SIDEBAR_COLOR, 
        fg=TEXT_COLOR, 
        relief=FLAT, 
        command=lambda: open_complaints(main) 
    ) 
    complaintsBtn.pack(pady=10, fill="x") 
    complaintsBtn.bind("<Enter>", lambda e: complaintsBtn.config(bg=SUB_ACCENT)) 
    complaintsBtn.bind("<Leave>", lambda e: complaintsBtn.config(bg=SIDEBAR_COLOR))
        
    # settings button
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




# completed functions to connect to other pages, commented out the unmerged pages


# commented out bcs i dont see a settings page on this commit

# def open_settings(main):
#     for widget in main.winfo_children():
#         widget.destroy()
#     settings.settings(main)
    
def open_mdash(main):
    for widget in main.winfo_children():
        widget.destroy()
    page_mdash.dashboard(main)
    
def open_repairs(main):
    for widget in main.winfo_children():
        widget.destroy()
    page_repairs.repairs(main)
    
    
#commented out bcs i haven't linked drashtis stuff yet

# def open_complaints(main):
#     for widget in main.winfo_children():
#         widget.destroy()
#     page_complaints.complaints(main)
    
    
    
    
# is there a logout button somewhere?    