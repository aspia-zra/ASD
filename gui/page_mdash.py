from tkinter import *
from . import NavBar
from models.repair import Repair


# themes
BG_COLOR = "#f5f3ff"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#1f1f1f"
ACCENT_COLOR = "#7c3aed"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 10, "bold")


def dashboard(main, db):

    for widget in main.winfo_children():
        widget.destroy()

    container = NavBar.navbar(main)

    title = Label(container, text="Maintenance Dashboard",
                  font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
    title.pack(pady=20)

    dashboardFrame = Frame(container, bg=BG_COLOR)
    dashboardFrame.pack(pady=20)

    dashboardFrame.columnconfigure(0, weight=1)
    dashboardFrame.columnconfigure(1, weight=1)

#open requests

    openFrame = Frame(dashboardFrame, bg=CARD_COLOR, padx=20, pady=20)
    openFrame.grid(row=0, column=0, padx=20, pady=20)

    Label(openFrame, text="Open Requests",
          font=FONT_HEADER, bg=CARD_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=6, pady=10)

    headers = ["Issue", "Apartment", "Date", "Worker", "Priority", ""]
    for i, h in enumerate(headers):
        Label(openFrame, text=h, font=FONT_LABEL,
              bg=CARD_COLOR).grid(row=1, column=i, padx=5, pady=5)

    requests = Repair.get_openrequests(db)

    for idx, r in enumerate(requests):

        row = idx + 2

        Label(openFrame, text=r["id"], bg=CARD_COLOR).grid(row=row, column=0)
        Label(openFrame, text=r["apartment"], bg=CARD_COLOR).grid(row=row, column=1)
        Label(openFrame, text=r["date"], bg=CARD_COLOR).grid(row=row, column=2)
        Label(openFrame, text=r["worker"], bg=CARD_COLOR).grid(row=row, column=3)
        Label(openFrame, text=r["priority"], bg=CARD_COLOR).grid(row=row, column=4)

        Button(
            openFrame,
            text="Complete",
            bg=ACCENT_COLOR,
            fg="white",
            font=FONT_BTN,
            command=lambda r=r, row=row: show_complete_inputs(openFrame, r, row, db, main)
        ).grid(row=row, column=5, padx=5)


#completed

    completedFrame = Frame(dashboardFrame, bg=CARD_COLOR, padx=20, pady=20)
    completedFrame.grid(row=0, column=1, padx=20, pady=20)

    Label(completedFrame, text="Completed Jobs",
          font=FONT_HEADER, bg=CARD_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=4, pady=10)

    headers = ["Issue", "Apartment", "Time", "Cost"]
    for i, h in enumerate(headers):
        Label(completedFrame, text=h, font=FONT_LABEL,
              bg=CARD_COLOR).grid(row=1, column=i, padx=5, pady=5)

    jobs = Repair.get_completed_requests(db)

    for idx, j in enumerate(jobs):

        row = idx + 2

        Label(completedFrame, text=j["id"], bg=CARD_COLOR).grid(row=row, column=0)
        Label(completedFrame, text=j["apartment"], bg=CARD_COLOR).grid(row=row, column=1)

        time = j.get("timeTaken", "-")
        cost = j.get("cost", "-")

        Label(completedFrame, text=time, bg=CARD_COLOR).grid(row=row, column=2)
        Label(completedFrame, text=cost, bg=CARD_COLOR).grid(row=row, column=3)

def show_complete_inputs(frame, request, row, db, main):

    timeEntry = Entry(frame, width=5)
    timeEntry.grid(row=row, column=2)

    notesEntry = Entry(frame, width=15)
    notesEntry.grid(row=row, column=3)

    costEntry = Entry(frame, width=6)
    costEntry.grid(row=row, column=4)

    Button(
        frame,
        text="Done",
        bg=ACCENT_COLOR,
        fg="white",
        font=FONT_BTN,
        command=lambda: finish_request(
            request,
            timeEntry.get(),
            notesEntry.get(),
            costEntry.get(),
            db,
            main
        )
    ).grid(row=row, column=5)


def finish_request(request, time, notes, cost, db, main):

    Repair.complete_request(
        db,
        request["id"],
        request["type"],
        time,
        notes,
        cost
    )

    dashboard(main, db)


#helper

def open_repairs(main):

    for widget in main.winfo_children():
        widget.destroy()

    from . import RepairsPage
    RepairsPage.repairs(main)


def open_complaints(main):

    for widget in main.winfo_children():
        widget.destroy()

    from . import ComplaintsPage
    ComplaintsPage.complaints(main)