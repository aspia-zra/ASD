# tkinter layout
# calls repair functions from models folder
# stopped at slide 35
# questons: pack object HERE, when to use and when have I used
# window sizes
# error hqndling for previous dates


import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from models.repairs import Repair
from db.db_connect import db 


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")
class RepairsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Make page expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):

        # ===== TITLE =====
        title = ctk.CTkLabel(
            self,
            text="Maintenance Management",
            font=("Arial", 34, "bold")
        )
        title.grid(row=0, column=0, pady=30)

        # ===== MAIN CONTENT =====
        content = ctk.CTkFrame(self)
        content.grid(row=1, column=0, sticky="nsew")

        content.grid_columnconfigure((0, 1), weight=1)
        content.grid_rowconfigure(0, weight=1)

        # ===== FORM =====
        form = ctk.CTkFrame(content)
        form.grid(row=0, column=0, sticky="nsew")

        form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form, text="Apartment ID", font=("Arial", 18)).grid(row=0, column=0, sticky="e", padx=20, pady=15)
        self.apartment_entry = ctk.CTkEntry(form, height=40, font=("Arial", 16))
        self.apartment_entry.grid(row=0, column=1, sticky="ew", padx=20, pady=15)

        ctk.CTkLabel(form, text="Worker ID", font=("Arial", 18)).grid(row=1, column=0, sticky="e", padx=20, pady=15)
        self.worker_entry = ctk.CTkEntry(form, height=40, font=("Arial", 16))
        self.worker_entry.grid(row=1, column=1, sticky="ew", padx=20, pady=15)

        ctk.CTkLabel(form, text="Maintenance Date (YYYY-MM-DD)", font=("Arial", 18)).grid(row=2, column=0, sticky="e", padx=20, pady=15)
        self.date_entry = ctk.CTkEntry(form, height=40, font=("Arial", 16))
        self.date_entry.grid(row=2, column=1, sticky="ew", padx=20, pady=15)

        # ===== BUTTONS =====
        buttons = ctk.CTkFrame(content)
        buttons.grid(row=0, column=1, sticky="nsew")

        for text, command in [
            ("Book Maintenance", self.book_maintenance),
            ("Record Resolution", self.record_resolution),
            ("Check Worker Availability", self.check_availability),
            ("Check Worker Role", self.check_role),
            ("Calculate Total Cost", self.calculate_total_cost),
            ("Generate Maintenance Report", self.generate_report),
        ]:
            ctk.CTkButton(
                buttons,
                text=text,
                height=50,
                font=("Arial", 18),
                command=command
            ).pack(fill="x", padx=40, pady=15)
   
    # --- Button callbacks ---
    def book_maintenance(self):
        apartment_id = self.apartment_entry.get().strip()
        worker_id = self.worker_entry.get().strip()
        date = self.date_entry.get().strip()

        if not apartment_id or not worker_id or not date:
            messagebox.showerror("Error", "Please complete all fields before booking maintenance.")
            return

        Repair.log_maintenance(db, apartment_id, worker_id, date)
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
        available = Repair.check_availability(db, worker_id, date)
        msg = "Available" if available else "Not available"
        messagebox.showinfo("Worker Availability", f"Worker {worker_id} is {msg} on {date}.")

    def check_role(self):
        worker_id = self.worker_entry.get().strip()

        if not worker_id:
            messagebox.showerror("Error", "Please enter a Worker ID first.")
            return

        valid = Repair.check_role(db, worker_id)
        msg = "Correct role" if valid else "Incorrect role"
        messagebox.showinfo("Worker Role Check", f"Worker {worker_id}: {msg}.")

    def calculate_total_cost(self):
        apartment_id = self.apartment_entry.get()
        total = Repair.calculate_total_cost(db, apartment_id)
        messagebox.showinfo("Total Cost", f"Total maintenance cost for apartment {apartment_id}: {total}")
        
    def generate_report(self):
        apartment_id = self.apartment_entry.get().strip()

        if not apartment_id:
            messagebox.showerror("Error", "Please enter an Apartment ID before generating a report.")
            return
        logs = Repair.generate_report(db)
        report_text = ""
        for log in logs:
            report_text += f"LogID: {log['logID']}, AptID: {log['apartmentID']}, WorkerID: {log['userID']}, Date: {log['maintenanceDate']}, Cost: {log['Cost']}, Notes: {log['Notes']}\n"
        # Show in a simple popup
        report_window = tk.Toplevel(self)
        report_window.title("Maintenance Report")
        text_box = tk.Text(report_window, wrap="word", width=100, height=30)
        text_box.pack()
        text_box.insert("1.0", report_text)