import customtkinter as ctk
from tkinter import messagebox
from gui.theme import *
from models.front_desk import FrontDesk
import gui.nav as nav
from . import theme
from models import user_session


class AssignApartmentPage(ctk.CTkFrame):
    def __init__(self, parent, controller, frontdesk_model):
        super().__init__(parent, fg_color=BACKGROUND)
        self.controller = controller
        self.model = frontdesk_model

        self.nav = nav.navbar(self, parent, mode=user_session.user_type.lower())
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main content

        self.main_frame = ctk.CTkFrame(self, fg_color=BACKGROUND)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.main_frame,
            text="Assign Apartment",
            font=("Arial", 28, "bold"),
            text_color=PRIMARY
        ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        card = ctk.CTkFrame(
            self.main_frame,
            fg_color=SURFACE,
            corner_radius=12,
            width=700,
            height=500
        )
        card.grid(row=1, column=0, sticky="n", padx=10, pady=10)
        card.grid_propagate(False)

        card.grid_columnconfigure(0, weight=0)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text="Select Tenant:",
            text_color=TEXT_PRIMARY,
            font=("Arial", 16)
        ).grid(row=0, column=0, pady=20, padx=20, sticky="w")

        self.tenant_var = ctk.StringVar()
        self.tenant_dropdown = ctk.CTkOptionMenu(
            card,
            variable=self.tenant_var,
            values=[""],
            font=("Arial", 16),
            width=320,
            height=40,
            fg_color=BACKGROUND,
            button_color=PRIMARY,
            button_hover_color=PRIMARY_DARK,
            text_color=TEXT_PRIMARY,
            dropdown_fg_color=BACKGROUND,
            dropdown_text_color=TEXT_PRIMARY
        )
        self.tenant_dropdown.grid(row=0, column=1, pady=20, padx=20, sticky="ew")

        ctk.CTkLabel(
            card,
            text="Select Apartment:",
            text_color=TEXT_PRIMARY,
            font=("Arial", 16)
        ).grid(row=1, column=0, pady=20, padx=20, sticky="w")

        self.apartment_var = ctk.StringVar()
        self.apartment_dropdown = ctk.CTkOptionMenu(
            card,
            variable=self.apartment_var,
            values=[""],
            font=("Arial", 16),
            width=320,
            height=40,
            fg_color=BACKGROUND,
            button_color=PRIMARY,
            button_hover_color=PRIMARY_DARK,
            text_color=TEXT_PRIMARY,
            dropdown_fg_color=BACKGROUND,
            dropdown_text_color=TEXT_PRIMARY
        )
        self.apartment_dropdown.grid(row=1, column=1, pady=20, padx=20, sticky="ew")

        ctk.CTkLabel(
            card,
            text="Enter Duration (years):",
            text_color=TEXT_PRIMARY,
            font=("Arial", 16)
        ).grid(row=2, column=0, pady=20, padx=20, sticky="w")
        self.duration = ctk.CTkEntry(card, placeholder_text="Enter lease duration")
        self.duration.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            card,
            text="Enter Deposit Amount:",
            text_color=TEXT_PRIMARY,
            font=("Arial", 16)
        ).grid(row=3, column=0, pady=20, padx=20, sticky="w")
        self.depositAmount = ctk.CTkEntry(card, placeholder_text="Enter the deposit Amount")
        self.depositAmount.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkButton(
            card,
            text="Assign Apartment",
            fg_color=PRIMARY,
            hover_color=PRIMARY_DARK,
            text_color="white",
            font=("Arial", 16, "bold"),
            width=220,
            height=45,
            command=self.assign_apartment
        ).grid(row=4, column=0, columnspan=2, pady=30)

        self.populate_dropdowns()

        self.labelFrame = ctk.CTkFrame(card, fg_color=theme.TITLE)
        self.labelFrame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        self.labelFrame.grid_remove()
        self.labelBanner = ctk.CTkLabel(self.labelFrame, text="", text_color=theme.SURFACE)
        self.labelBanner.pack(fill="x", padx=5, pady=5)  

    def refresh(self):
        self.duration.delete(0,'end')
        self.depositAmount.delete(0,'end')
        self.populate_dropdowns()

    def populate_dropdowns(self):
        try:
            tenants = self.model.get_all_tenants()
            tenant_names = [f"{t['tenantID']}: {t['fullName']}" for t in tenants]

            if tenant_names:
                self.tenant_dropdown.configure(values=tenant_names)
                self.tenant_var.set(tenant_names[0])
            else:
                self.tenant_dropdown.configure(values=["No tenants found"])
                self.tenant_var.set("No tenants found")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load tenants: {e}")

        try:
            apartments = self.model.get_all_apartments()
            apartment_list = [str(a) for a in apartments]

            if apartment_list:
                self.apartment_dropdown.configure(values=apartment_list)
                self.apartment_var.set(apartment_list[0])
            else:
                self.apartment_dropdown.configure(values=["No apartments found"])
                self.apartment_var.set("No apartments found")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load apartments: {e}")

    def assign_apartment(self):
        tenant_value = self.tenant_var.get()
        apartment_id = self.apartment_var.get()
        depositAmount_raw = self.depositAmount.get()
        duration_raw = self.duration.get()

        if not tenant_value or tenant_value == "No tenants found":
            self.labelBanner.configure(text="Please select a tenant.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return

        if not apartment_id or apartment_id == "No apartments found":
            self.labelBanner.configure(text="Please select an apartment.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return

        if not depositAmount_raw.isdigit():
            self.labelBanner.configure(text="Deposit must be a number.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return
        
        depositAmount = int(depositAmount_raw)

        if not depositAmount or depositAmount < 500:
            self.labelBanner.configure(text="Deposit must be atleast £500.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return
        
        if not duration_raw.isdigit():
            self.labelBanner.configure(text="Duration must be a number.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return
        
        duration = int(duration_raw)

        if duration < 1 or duration > 5:
            self.labelBanner.configure(text="Duration must be between 1 to 5 years.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return
        
        tenant_id = tenant_value.split(":")[0].strip()

        try:
            self.model.assign_apartment(tenant_id, int(apartment_id), depositAmount, duration)

            self.labelBanner.configure(text=f"Apartment {apartment_id} assigned to tenant {tenant_id}", fg_color=theme.SUCCESS)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            self.refresh()
        except Exception as e:
            self.labelBanner.configure(text=str(e), fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
