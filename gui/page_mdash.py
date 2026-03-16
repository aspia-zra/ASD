# maintenance dashboard page, links with complaints and repairs page

# question: how do we even link merccys reports page ... do i add it to mdash, aren't they reports for everyone?
# imaan hasn't put the functions in a models file ... idk MVC

from tkinter import *
from . import NavBar
from models import mdashmodel

# themes
BG_COLOR = "#f5f3ff"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#1f1f1f"
ACCENT_COLOR = "#7c3aed"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")


# logic
def dashboard(main):

    # clear window
    for widget in main.winfo_children():
        widget.destroy()

    # create navbar
    container = NavBar.navbar(main)

    # page title
    title = Label(container, text="Maintenance Dashboard",
                  font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
    title.pack(pady=20)

    # main dashboard frame
    dashboardFrame = Frame(container, bg=BG_COLOR)
    dashboardFrame.pack(pady=20)

    dashboardFrame.columnconfigure(0, weight=1)
    dashboardFrame.columnconfigure(1, weight=1)

    # LEFT BOX – OPEN REQUESTS

    openFrame = Frame(dashboardFrame, bg=CARD_COLOR, padx=20, pady=20)
    openFrame.grid(row=0, column=0, padx=20, pady=20)

    openTitle = Label(openFrame, text="Open Requests",
                      font=FONT_HEADER, bg=CARD_COLOR, fg=TEXT_COLOR)
    openTitle.pack(pady=10)

    # list of requests
    requestList = Listbox(openFrame, width=40, height=10)
    requestList.pack(pady=10)

    # load requests from model
    requests = mdashmodel.get_open_requests()

    for r in requests:
        requestList.insert(END, f"Apt {r['apartmentID']} - {r['Description']} (Priority {r['Severity']})")

    # buttons
    btnFrame = Frame(openFrame, bg=CARD_COLOR)
    btnFrame.pack(pady=10)

    Button(btnFrame, text="Mark Complete",
           bg=ACCENT_COLOR, fg="white",
           font=FONT_BTN).pack(side=LEFT, padx=5)

    Button(btnFrame, text="Change Status",
           bg=ACCENT_COLOR, fg="white",
           font=FONT_BTN).pack(side=LEFT, padx=5)

    Button(btnFrame, text="Add Repair",
           bg=ACCENT_COLOR, fg="white",
           font=FONT_BTN,
           command=lambda: open_repairs(main)).pack(side=LEFT, padx=5)


    # RIGHT BOX – COMPLETED LOGS


    completedFrame = Frame(dashboardFrame, bg=CARD_COLOR, padx=20, pady=20)
    completedFrame.grid(row=0, column=1, padx=20, pady=20)

    completedTitle = Label(completedFrame, text="Last 5 Completed Jobs",
                           font=FONT_HEADER, bg=CARD_COLOR, fg=TEXT_COLOR)
    completedTitle.pack(pady=10)

    completedList = Listbox(completedFrame, width=40, height=10)
    completedList.pack(pady=10)

    # load completed jobs
    jobs = mdashmodel.get_last_completed()

    for j in jobs:
        completedList.insert(
            END,
            f"Apt {j['apartmentID']} - {j['timeTaken']}h - £{j['Cost']}"
        )

# OPEN REPAIRS PAGE (add a repair)


def open_repairs(main):

    for widget in main.winfo_children():
        widget.destroy()

    from . import RepairsPage
    RepairsPage.repairs(main)

# another one for complaints page, commented out bcs i haven't linked drashtis page yet