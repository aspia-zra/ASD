import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from models.repairs import Repair
from db.db_connect import db


ctk.set_default_color_theme("dark-blue")


class RepairsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
# wrappers
        title = ctk.CTkLabel(
            self,
            text="Repair Booking",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=30)

        container = ctk.CTkFrame(self)
        container.pack(pady=20, padx=40, fill="both", expand=True)

        container.grid_columnconfigure(0, weight=1)

        form = ctk.CTkFrame(container)
        form.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

        form.grid_columnconfigure(1, weight=1)

# form components
        #issue
        ctk.CTkLabel(form, text="Issue / Notes", font=("Segoe UI", 16)).grid(
            row=0, column=0, padx=20, pady=15, sticky="e"
        )

        self.issue_entry = ctk.CTkEntry(form, height=40)
        self.issue_entry.grid(row=0, column=1, padx=20, pady=15, sticky="ew")

        # apartment
        ctk.CTkLabel(form, text="Apartment ID", font=("Segoe UI", 16)).grid(
            row=1, column=0, padx=20, pady=15, sticky="e"
        )

        self.apartment_entry = ctk.CTkEntry(form, height=40)
        self.apartment_entry.grid(row=1, column=1, padx=20, pady=15, sticky="ew")

        # date
        ctk.CTkLabel(form, text="Repair Date (YYYY-MM-DD)", font=("Segoe UI", 16)).grid(
            row=2, column=0, padx=20, pady=15, sticky="e"
        )

        self.date_entry = ctk.CTkEntry(form, height=40)
        self.date_entry.grid(row=2, column=1, padx=20, pady=15, sticky="ew")

        # priority
        ctk.CTkLabel(form, text="Priority", font=("Segoe UI", 16)).grid(
            row=3, column=0, padx=20, pady=15, sticky="e"
        )

        self.priority_box = ctk.CTkComboBox(
            form,
            values=["Low", "Medium", "High"]
        )
        self.priority_box.grid(row=3, column=1, padx=20, pady=15, sticky="ew")

        #util
        button_frame = ctk.CTkFrame(container)
        button_frame.grid(row=1, column=0, pady=20)

        ctk.CTkButton(
            button_frame,
            text="Display Cost",
            height=45,
            command=self.display_cost
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            button_frame,
            text="Book Now",
            height=45,
            command=self.book_repair
        ).grid(row=0, column=1, padx=20)

# date error handling

    def valid_date(self, date_string):

        try:
            repair_date = datetime.strptime(date_string, "%Y-%m-%d").date()
            today = datetime.today().date()

            if repair_date < today:
                return False

            return True

        except ValueError:
            return False

    def display_cost(self):

        apartment_id = self.apartment_entry.get().strip()

        if not apartment_id:
            messagebox.showerror("Error", "Enter an apartment ID first.")
            return

        cost = Repair.calculate_total_cost(db, apartment_id)

        messagebox.showinfo(
            "Estimated Cost",
            f"Total maintenance cost for apartment {apartment_id}: £{cost}"
        )

    def book_repair(self):

        issue = self.issue_entry.get().strip()
        apartment_id = self.apartment_entry.get().strip()
        date = self.date_entry.get().strip()
        priority = self.priority_box.get()

        if not issue or not apartment_id or not date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not self.valid_date(date):
            messagebox.showerror(
                "Invalid Date",
                "Repair date cannot be in the past and must follow YYYY-MM-DD."
            )
            return

        try:

            # Worker assignment could be automatic later
            worker_id = None

            Repair.log_maintenance(
                db,
                apartment_id,
                worker_id,
                date
            )

            # EMAIL PLACEHOLDER
            # send_email_to_tenant(apartment_id, date)

            messagebox.showinfo(
                "Success",
                "Repair booked successfully. Tenant notification sent."
            )

            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):

        self.issue_entry.delete(0, "end")
        self.apartment_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.priority_box.set("")