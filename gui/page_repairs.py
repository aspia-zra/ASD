# tkinter layout
# calls repair functions from models folder


import tkinter as tk
from tkinter import messagebox, simpledialog
from models.repairs import Repair
from db.db_connect import db 

class RepairsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # --- Apartment ID ---
        tk.Label(self, text="Apartment ID").grid(row=0, column=0, sticky="e")
        self.apartment_entry = tk.Entry(self)
        self.apartment_entry.grid(row=0, column=1)

        # --- Worker ID ---
        tk.Label(self, text="Worker ID").grid(row=1, column=0, sticky="e")
        self.worker_entry = tk.Entry(self)
        self.worker_entry.grid(row=1, column=1)

        # --- Maintenance Date ---
        tk.Label(self, text="Maintenance Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="e")
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=2, column=1)

        # --- Buttons ---
        tk.Button(self, text="Book Maintenance", command=self.book_maintenance).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Record Resolution", command=self.record_resolution).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Check Worker Availability", command=self.check_availability).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Check Worker Role", command=self.check_role).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Calculate Total Cost for Apartment", command=self.calculate_total_cost).grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Generate Maintenance Report", command=self.generate_report).grid(row=8, column=0, columnspan=2, pady=5)

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