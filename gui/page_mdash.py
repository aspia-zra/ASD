import customtkinter as ctk
from tkinter import *
from models.repairs import Repair
from gui.page_repairs import create_navbar


BG_COLOR = "#f5f3ff"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#1f1f1f"
ACCENT_COLOR = "#7c3aed"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 10, "bold")


def dashboard(parent, db):

    for widget in parent.winfo_children():
        widget.destroy()

    page = ctk.CTkFrame(parent)
    page.pack(fill="both", expand=True)

    page.grid_rowconfigure(0, weight=1)
    page.grid_columnconfigure(1, weight=1)

    def show_dashboard():
        dashboard(parent, db)

    def show_repairs():
        from gui.page_repairs import RepairsPage

        for w in parent.winfo_children():
            w.destroy()

        RepairsPage(parent, db).pack(fill="both", expand=True)

    def show_complaints():
        from gui.page_complaints import ComplaintsPage

        for w in parent.winfo_children():
            w.destroy()

        ComplaintsPage(parent, db).pack(fill="both", expand=True)

    def show_settings():
        from . import settings

        for w in parent.winfo_children():
            w.destroy()

        settings.settings(parent)

    create_navbar(page, show_dashboard, show_repairs, show_complaints, show_settings)

    # main content area (same as repairs container)
    container = ctk.CTkFrame(page)
    container.grid(row=0, column=1, sticky="nsew", padx=40, pady=20)

    title = ctk.CTkLabel(
        container,
        text="Maintenance Dashboard",
        font=FONT_TITLE
    )
    title.pack(pady=30)

    dashboardFrame = Frame(container, bg=BG_COLOR)
    dashboardFrame.pack(pady=20)

    dashboardFrame.columnconfigure(0, weight=1)
    dashboardFrame.columnconfigure(1, weight=1)

    # open requests
    openFrame = Frame(dashboardFrame, bg=CARD_COLOR, padx=20, pady=20)
    openFrame.grid(row=0, column=0, padx=20, pady=20)

    Label(openFrame, text="Open Requests",
          font=FONT_HEADER, bg=CARD_COLOR).grid(row=0, column=0, columnspan=6, pady=10)

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

    # completed jobs
    completedFrame = Frame(dashboardFrame, bg=CARD_COLOR, padx=20, pady=20)
    completedFrame.grid(row=0, column=1, padx=20, pady=20)

    Label(completedFrame, text="Completed Jobs",
          font=FONT_HEADER, bg=CARD_COLOR).grid(row=0, column=0, columnspan=4, pady=10)

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