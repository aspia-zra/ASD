# tkinter layout
# calls repair functions from models folder
# stopped at slide 35
# questons: pack object HERE, when to use and when have I used
# window sizes



import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from models.repairs import Repair
from db.db_connect import db 


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class RepairsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.pack(expand=True)
        container = tk.Frame(self)
        container.pack(expand=True)

        # Title
        title = tk.Label(
            container,
            text="Maintenance Management",
            font=("Arial", 22, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Form frame (for inputs)
        form = tk.Frame(container)
        form.grid(row=1, column=0, columnspan=2)

        # --- Apartment ID ---
        tk.Label(form, text="Apartment ID").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.apartment_entry = tk.Entry(form, width=25)
        self.apartment_entry.grid(row=0, column=1, pady=5)

        # --- Worker ID ---
        tk.Label(form, text="Worker ID").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.worker_entry = tk.Entry(form, width=25)
        self.worker_entry.grid(row=1, column=1, pady=5)

        # --- Maintenance Date ---
        tk.Label(form, text="Maintenance Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.date_entry = tk.Entry(form, width=25)
        self.date_entry.grid(row=2, column=1, pady=5)

        # Buttons frame
        buttons = tk.Frame(container)
        buttons.grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(buttons, text="Book Maintenance", width=30, command=self.log_maintenance).pack(pady=5)
        tk.Button(buttons, text="Record Resolution", width=30, command=self.record_resolution).pack(pady=5)
        tk.Button(buttons, text="Check Worker Availability", width=30, command=self.check_availability).pack(pady=5)
        tk.Button(buttons, text="Check Worker Role", width=30, command=self.check_role).pack(pady=5)
        tk.Button(buttons, text="Calculate Total Cost", width=30, command=self.calculate_total_cost).pack(pady=5)
        tk.Button(buttons, text="Generate Maintenance Report", width=30, command=self.generate_report).pack(pady=5)

    # --- Button callbacks ---
    def book_maintenance(self):
        apartment_id = self.apartment_entry.get()
        worker_id = self.worker_entry.get()
        date = self.date_entry.get()
        Repair.logMaintenance(db, apartment_id, worker_id, date)
        messagebox.showinfo("Success", "Maintenance visit booked!")

    def record_resolution(self):
        log_id = simpledialog.askinteger("Log ID", "Enter Log ID:")
        time_taken = simpledialog.askfloat("Time Taken", "Hours spent:")
        cost = simpledialog.askfloat("Cost", "Repair cost:")
        notes = simpledialog.askstring("Notes", "Any notes?")
        Repair.record_resolution(db, log_id, time_taken, cost, notes)
        messagebox.showinfo("Success", "Resolution logged!")

    def check_availability(self):
        worker_id = self.worker_entry.get()
        date = self.date_entry.get()
        available = Repair.check_worker_availability(db, worker_id, date)
        msg = "Available" if available else "Not available"
        messagebox.showinfo("Worker Availability", f"Worker {worker_id} is {msg} on {date}.")

    def check_role(self):
        worker_id = self.worker_entry.get()
        valid = Repair.check_worker_role_needed(db, worker_id)
        msg = "Correct role" if valid else "Incorrect role"
        messagebox.showinfo("Worker Role Check", f"Worker {worker_id}: {msg}.")

    def calculate_total_cost(self):
        apartment_id = self.apartment_entry.get()
        total = Repair.calculate_total_cost(db, apartment_id)
        messagebox.showinfo("Total Cost", f"Total maintenance cost for apartment {apartment_id}: {total}")

    def generate_report(self):
        logs = Repair.generateMaintenanceReport(db)
        report_text = ""
        for log in logs:
            report_text += f"LogID: {log['logID']}, AptID: {log['apartmentID']}, WorkerID: {log['userID']}, Date: {log['maintenanceDate']}, Cost: {log['Cost']}, Notes: {log['Notes']}\n"
        # Show in a simple popup
        report_window = tk.Toplevel(self)
        report_window.title("Maintenance Report")
        tk.Text(report_window, wrap="word", width=100, height=30).insert("1.0", report_text)
        tk.Text(report_window, wrap="word", width=100, height=30).pack()