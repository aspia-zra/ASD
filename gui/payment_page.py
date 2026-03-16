import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk


class PaymentPage(ctk.CTkFrame):

    def __init__(self, parent, controller=None):
        super().__init__(parent)

        self.controller = controller

        # main layout 
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # navbar placeholder 
        self.navbar_frame = ctk.CTkFrame(self, width=200, fg_color="#202e75", corner_radius=0)
        self.navbar_frame.grid(row=0, column=0, sticky="ns")
        self.navbar_frame.grid_propagate(False)

        ctk.CTkLabel(
            self.navbar_frame,
            text="Paragon\nApartments",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).grid(row=0, column=0, pady=30, padx=20)

        nav_buttons = ["Dashboard", "Notifications", "Settings", "Payments", "Complaints", "Repairs"]

        for i, name in enumerate(nav_buttons):
            ctk.CTkButton(
                self.navbar_frame,
                text=name,
                fg_color="#202e75",
                hover_color="#0f0f30",
                text_color="white",
                font=("Arial", 12),
                width=160,
                corner_radius=8
            ).grid(row=i+1, column=0, padx=20, pady=8, sticky="ew")

        ctk.CTkButton(
            self.navbar_frame,
            text="Logout",
            fg_color="#202e75",
            hover_color="#7a070d",
            text_color="white",
            font=("Arial", 12, "bold"),
            width=160,
            corner_radius=8
        ).grid(row=9, column=0, padx=20, pady=20, sticky="ew")

        # main content area
        self.content = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(3, weight=1)

        
        self.alert_label = ctk.CTkLabel(
            self.content,
            text="⚠️ There are overdue invoices! Please review.",
            fg_color="#c0392b",
            text_color="white",
            font=("Arial", 12, "bold"),
            corner_radius=0,
            height=35
        )

        
        ctk.CTkLabel(
            self.content,
            text="Payment & Billing",
            font=("Arial", 22, "bold"),
            text_color="#202e75"
        ).grid(row=1, column=0, pady=(20, 2))

        ctk.CTkLabel(
            self.content,
            text="Finance Manager — Manage all tenant invoices",
            font=("Arial", 12),
            text_color="gray"
        ).grid(row=2, column=0, pady=(0, 15))

        
        btn_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(0, 15))

        ctk.CTkButton(
            btn_frame,
            text="Mark as Paid",
            width=150,
            height=38,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            fg_color="#202e75",
            hover_color="#0f0f30",
            command=self.mark_as_paid
        ).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            btn_frame,
            text="Generate Receipt",
            width=150,
            height=38,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            fg_color="#1a7a4a",
            hover_color="#145e38",
            command=self.generate_receipt
        ).grid(row=0, column=1, padx=8)

        ctk.CTkButton(
            btn_frame,
            text="Show Overdue",
            width=150,
            height=38,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            fg_color="#c0392b",
            hover_color="#922b21",
            command=self.show_overdue
        ).grid(row=0, column=2, padx=8)

        ctk.CTkButton(
            btn_frame,
            text="Refresh",
            width=100,
            height=38,
            corner_radius=10,
            font=("Arial", 12),
            fg_color="#555555",
            hover_color="#333333",
            command=self.load_invoices
        ).grid(row=0, column=3, padx=8)

        ctk.CTkButton(
            btn_frame,
            text="Reset",
            width=100,
            height=38,
            corner_radius=10,
            font=("Arial", 12),
            fg_color="#7d6608",
            hover_color="#5d4e06",
            command=self.reset_invoice
        ).grid(row=0, column=4, padx=8)

        
        table_frame = ctk.CTkFrame(self.content, fg_color="white", corner_radius=12)
        table_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 10))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.content.grid_rowconfigure(4, weight=1)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        self.table = ttk.Treeview(
            table_frame,
            columns=("InvoiceID", "Tenant", "Amount", "DueDate", "Status"),
            show="headings",
            height=15
        )

        self.table.heading("InvoiceID", text="Invoice ID")
        self.table.heading("Tenant", text="Tenant Name")
        self.table.heading("Amount", text="Amount (£)")
        self.table.heading("DueDate", text="Due Date")
        self.table.heading("Status", text="Status")

        self.table.column("InvoiceID", width=90, anchor="center")
        self.table.column("Tenant", width=180)
        self.table.column("Amount", width=110, anchor="center")
        self.table.column("DueDate", width=120, anchor="center")
        self.table.column("Status", width=110, anchor="center")

        self.table.tag_configure("overdue", background="#fde8e8")
        self.table.tag_configure("paid", background="#e8f8ee")
        self.table.tag_configure("pending", background="#fff9e6")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

        
        self.status_label = ctk.CTkLabel(
            self.content,
            text="",
            font=("Arial", 11),
            text_color="gray"
        )
        self.status_label.grid(row=5, column=0, pady=(0, 10))

        self.load_invoices()

    def load_invoices(self):
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            from models.payment_model import get_all_invoices, check_any_overdue
            invoices = get_all_invoices()

            for invoice in invoices:
                invoice_id = invoice[0]
                tenant_name = invoice[1]
                amount = f"£{invoice[2]:.2f}"
                due_date = str(invoice[3])
                status = invoice[4]

                tag = status.lower()
                self.table.insert("", "end", values=(invoice_id, tenant_name, amount, due_date, status), tags=(tag,))

            if check_any_overdue():
                self.alert_label.grid(row=0, column=0, sticky="ew")
            else:
                self.alert_label.grid_remove()

            self.status_label.configure(text=f"{len(invoices)} invoices loaded")

        except Exception as e:
            self.status_label.configure(text="Could not load invoices — check database connection")
            print("Error loading invoices:", e)

    def mark_as_paid(self):
        selected = self.table.selection()

        if selected == ():
            messagebox.showwarning("Warning", "Please select an invoice first")
            return

        invoice_id = self.table.item(selected[0])["values"][0]
        status = self.table.item(selected[0])["values"][4]

        if status == "paid":
            messagebox.showinfo("Info", "This invoice is already paid")
            return

        try:
            from models.payment_model import mark_invoice_paid
            mark_invoice_paid(invoice_id)
            messagebox.showinfo("Success", f"Invoice {invoice_id} marked as paid")
            self.load_invoices()

        except Exception as e:
            messagebox.showerror("Error", "Could not update invoice")
            print("Error marking paid:", e)

    def generate_receipt(self):
        selected = self.table.selection()

        if selected == ():
            messagebox.showwarning("Warning", "Please select an invoice first")
            return

        values = self.table.item(selected[0])["values"]
        invoice_id = values[0]
        tenant_name = values[1]
        amount = values[2]
        due_date = values[3]
        status = values[4]

        try:
            from utils.receipt_generator import generate_receipt
            filename = generate_receipt(invoice_id, tenant_name, amount, due_date, status)
            messagebox.showinfo("Receipt Generated", f"Receipt saved as {filename}")

        except Exception as e:
            messagebox.showerror("Error", "Could not generate receipt")
            print("Error generating receipt:", e)

    def reset_invoice(self):
        selected = self.table.selection()

        if selected == ():
            messagebox.showwarning("Warning", "Please select an invoice first")
            return

        invoice_id = self.table.item(selected[0])["values"][0]

        try:
            from models.payment_model import reset_invoice_status
            reset_invoice_status(invoice_id)
            messagebox.showinfo("Reset", f"Invoice {invoice_id} reset to pending")
            self.load_invoices()

        except Exception as e:
            messagebox.showerror("Error", "Could not reset invoice")
            print("Error resetting invoice:", e)

    def show_overdue(self):
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            from models.payment_model import get_overdue_invoices
            invoices = get_overdue_invoices()

            for invoice in invoices:
                invoice_id = invoice[0]
                tenant_name = invoice[1]
                amount = f"£{invoice[2]:.2f}"
                due_date = str(invoice[3])
                status = invoice[4]

                self.table.insert("", "end", values=(invoice_id, tenant_name, amount, due_date, status), tags=("overdue",))

            self.status_label.configure(text=f"{len(invoices)} overdue invoices")

        except Exception as e:
            self.status_label.configure(text="Could not load overdue invoices")
            print("Error:", e)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.title("Paragon - Payments")
    root.geometry("1000x700")
    app = PaymentPage(root)
    app.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()