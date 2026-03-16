import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox
from db.db_connect import Database
from models.complaints import Complaints

class ComplaintsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.models = Complaints()

        self.db = Database()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_navbar()
        self.create_form()

    def submit_complaint(self):
        reason = self.Entrycomplaint.get()
        severity = self.severity.get()
        apartmentnumber = self.EntryAPID.get()
        complaintdetail = self.EntryComplaintDetails.get("1.0", "end")
        
        inserted = self.models.add_complaint(reason, severity, apartmentnumber, complaintdetail)
        if inserted:
            messagebox.showinfo("Success", "Complaint submitted successfully")
            self.load_complaint_history()

    def load_complaint_history(self):
        # Get apartment number from the entry
        apartmentnumber = self.EntryAPID.get()
        # If no apartment number entered, do nothing yet
        if not apartmentnumber:
            return
        # Get tenant ID from the model
        tenantID = self.models.get_tenantID(apartmentnumber)
        if not tenantID:
            return

        # Get complaints from the model
        complaints = self.models.get_recent_complaints(tenantID)

        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert rows
        for complaint in complaints:
            reason = complaint["reason"]
            timestamp = complaint["timestamp"]
            severity = complaint["severity"]
            status = complaint["status"]
            self.tree.insert("", "end", values=(reason, timestamp, severity, status))

    def create_navbar(self):
        self.navbar = ctk.CTkFrame(self, width=200)
        self.navbar.grid(row=0, column=0, sticky="ns")
        self.navbar.grid_columnconfigure(0, weight=1)
        #nav bar 
        navtitle_label = ctk.CTkLabel(self.navbar, text="Paragon Apartments", font=("Arial", 24))
        navtitle_label.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20,)

        profile = ctk.CTkButton(self.navbar, fg_color="#202e75", hover_color="#0f0f30",text="Profile")
        profile.grid(row = 1, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        notif = ctk.CTkButton(self.navbar, fg_color="#202e75", hover_color="#0f0f30",text="Notifications")
        notif.grid(row = 2, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        settings = ctk.CTkButton(self.navbar, fg_color="#202e75", hover_color="#0f0f30",text="Settings")
        settings.grid(row = 3, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        payments = ctk.CTkButton(self.navbar, fg_color="#202e75", hover_color="#0f0f30",text="Payments")
        payments.grid(row = 4, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        complaints = ctk.CTkButton(self.navbar, fg_color="#202e75", hover_color="#0f0f30",text="Complaints")
        complaints.grid(row = 5, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        repairs = ctk.CTkButton(self.navbar, fg_color="#202e75", hover_color="#0f0f30",text="Repairs",command=self.open_repairs)
        repairs.grid(row = 6, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        logout = ctk.CTkButton(self.navbar, fg_color="#202e75",hover_color="#7a070d",text="Logout")
        logout.grid(row = 8, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")
    
    def create_form(self):
        self.form = ctk.CTkFrame(self)
        self.form.grid(row=0, column=1, sticky="nsew")
        self.form.grid_columnconfigure(3, weight=1)
        #form start
        title_label = ctk.CTkLabel(self.form, text="Complaints", font=("Arial", 18))
        title_label.grid(row = 0, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")
        # complaint reason
        self.labelcomplaint = ctk.CTkLabel(self.form, text="Complaint Reason:")
        self.labelcomplaint.grid(row = 1, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.Entrycomplaint = ctk.CTkEntry(self.form,width=200  , placeholder_text="Enter Complaint Reason")
        self.Entrycomplaint.grid(row = 1, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #severity of complaint
        self.labelseverity = ctk.CTkLabel(self.form, text="Severity of Complaint:")
        self.labelseverity.grid(row = 2, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.severity = ctk.CTkOptionMenu(self.form, values=["1", "2", "3", "4", "5"])
        self.severity.grid(row = 2, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #apartment Id entry
        self.labelAPID = ctk.CTkLabel(self.form, text="Apartment Number:") 
        self.labelAPID.grid(row = 3, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.EntryAPID = ctk.CTkEntry(self.form, placeholder_text="Enter your Apartment Number")
        self.EntryAPID.grid(row = 3, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.labelComplaintDetails = ctk.CTkLabel(self.form, text="Complaint Details:")
        self.labelComplaintDetails.grid(row = 4, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.EntryComplaintDetails = ctk.CTkTextbox(self.form,width=200, height=100, fg_color="#454547")
        self.EntryComplaintDetails.grid(row = 4, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew") 

        button = ctk.CTkButton(self.form,
                               bg_color="#202e75",
                               hover_color="#144518",
                               text="Submit a Complaint",
                               command=self.submit_complaint
                               )
        button.grid(row = 5, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #complaint history
        history_label = ctk.CTkLabel(self.form, text="Complaint History", font=("Arial", 18))
        history_label.grid(row = 7, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")

        columns = ("Complaint Number: ", "Report Date", "Severity", "Status")

        self.tree = ttk.Treeview(self.form, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.grid(row = 8, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")
        self.load_complaint_history()

