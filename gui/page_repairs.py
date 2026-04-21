# handling workers: one worker per repair per day. if none are available, display 'pick another day'
import customtkinter as ctk
from db import db
from datetime import datetime
from models.repairs import Repair
from . import theme
import gui.nav as nav 
from models import user_session

class RepairsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=theme.BACKGROUND)
        controller = getattr(self.winfo_toplevel(), "app_controller", self.winfo_toplevel())
        self.db = db
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.nav = nav.navbar(self, parent, mode=user_session.user_type.lower())
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")
        
        self.create_widgets()

    def open_maintenance_dashboard(self):
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_maintenance_dashboard", None)

        if callable(navigate):
            navigate()
            return

        for widget in host.winfo_children():
            widget.destroy()

        from .page_mdash import dashboard
        dashboard(host, self.db)

    def open_repairs(self):
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_repairs_page", None)

        if callable(navigate):
            navigate()
            return

        for widget in host.winfo_children():
            widget.destroy()

        repairs_page = RepairsPage(host, self.db)
        repairs_page.pack(fill="both", expand=True)

    def open_complaints(self):
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_complaints_page", None)

        if callable(navigate):
            navigate()
            return

        for widget in host.winfo_children():
            widget.destroy()

        from .page_complaints import ComplaintsPage
        complaints_page = ComplaintsPage(host, self.db)
        complaints_page.pack(fill="both", expand=True)

    def open_settings(self):
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_settings", None)

        if callable(navigate):
            navigate()
            return

        self.labelBanner.configure(text="Settings are not available yet.", fg_color=theme.PRIMARY_LIGHT)
        self.labelFrame.grid()
        self.after(3000, lambda: self.labelFrame.grid_remove())


    def create_widgets(self):
        # Main content container (right side) with vertical scrolling.
        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.BACKGROUND,
            scrollbar_button_color=theme.PRIMARY,
            scrollbar_button_hover_color=theme.PRIMARY_DARK,
        )
        self.container.grid(row=0, column=1, sticky="nsew", padx=40, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.container,
            text="Repair Booking",
            font=theme.TITLE_FONT,
            text_color=theme.PRIMARY,
        )
        title.grid(row=0, column=0, pady=30)

        form = ctk.CTkFrame(self.container, fg_color=theme.SURFACE, corner_radius=12)
        form.grid(row=1, column=0, padx=40, pady=40, sticky="nsew")

        form.grid_columnconfigure(1, weight=1)

        # form components
        # issue
        ctk.CTkLabel(form, text="Repair Reason", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY).grid(
            row=0, column=0, padx=20, pady=15, sticky="e"
        )

        self.issue_entry = ctk.CTkEntry(
            form,
            height=40,
            fg_color=theme.BACKGROUND,
            text_color=theme.TEXT_PRIMARY,
            placeholder_text_color=theme.TEXT_SECONDARY,
            border_color=theme.SECONDARY,
        )
        self.issue_entry.grid(row=0, column=1, padx=20, pady=15, sticky="ew")

        # repair details
        ctk.CTkLabel(form, text="Repair Details", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY).grid(
            row=1, column=0, padx=20, pady=15, sticky="ne"
        )

        self.details_entry = ctk.CTkTextbox(
            form,
            height=120,
            fg_color=theme.BACKGROUND,
            text_color=theme.TEXT_PRIMARY,
            border_color=theme.SECONDARY,
            border_width=1,
        )
        self.details_entry.grid(row=1, column=1, padx=20, pady=15, sticky="ew")

        # apartment
        ctk.CTkLabel(form, text="Apartment Number", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY).grid(
            row=2, column=0, padx=20, pady=15, sticky="e"
        )

        self.apartment_entry = ctk.CTkEntry(
            form,
            height=40,
            fg_color=theme.BACKGROUND,
            text_color=theme.TEXT_PRIMARY,
            placeholder_text_color=theme.TEXT_SECONDARY,
            border_color=theme.SECONDARY,
        )
        self.apartment_entry.grid(row=2, column=1, padx=20, pady=15, sticky="ew")

        # date
        ctk.CTkLabel(form, text="Repair Date (DD-MM-YY)", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY).grid(
            row=3, column=0, padx=20, pady=15, sticky="e"
        )

        self.date_entry = ctk.CTkEntry(
            form,
            height=40,
            fg_color=theme.BACKGROUND,
            text_color=theme.TEXT_PRIMARY,
            placeholder_text_color=theme.TEXT_SECONDARY,
            border_color=theme.SECONDARY,
        )
        self.date_entry.grid(row=3, column=1, padx=20, pady=15, sticky="ew")

        # priority
        ctk.CTkLabel(form, text="Priority", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY).grid(
            row=4, column=0, padx=20, pady=15, sticky="e"
        )

        self.priority_box = ctk.CTkSegmentedButton(
            form,
            values=["1", "2", "3"],
            selected_color=theme.PRIMARY,
            selected_hover_color=theme.PRIMARY_DARK,
            unselected_color=theme.BACKGROUND,
            unselected_hover_color=theme.SECONDARY,
            text_color=theme.TEXT_PRIMARY,
        )
        self.priority_box.grid(row=4, column=1, padx=20, pady=15, sticky="ew")
        self.priority_box.set("2")

        self.labelFrame = ctk.CTkFrame(form, fg_color=theme.TITLE)
        self.labelFrame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        self.labelFrame.grid_remove()
        self.labelBanner = ctk.CTkLabel(self.labelFrame, text="", text_color=theme.SURFACE)
        self.labelBanner.pack(fill="x", padx=5, pady=5) 

        # util
        button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=20)

        ctk.CTkButton(
            button_frame,
            text="Get Cost",
            fg_color=theme.INFO,
            hover_color=theme.PRIMARY_DARK,
            text_color=theme.SURFACE,
            height=45,
            command=self.display_cost
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            button_frame,
            text="Book Now",
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            text_color=theme.SURFACE,
            height=45,
            command=self.book_repair
        ).grid(row=0, column=1, padx=20)

# date error handling

    def valid_date(self, date_string):
        parsed_date = self.parse_date(date_string)

        if parsed_date is None:
            return False

        today = datetime.today().date()
        return parsed_date >= today

    def parse_date(self, date_string):
        normalized = (date_string or "").strip().replace("/", "-")

        for fmt in ("%d-%m-%y", "%d-%m-%Y"):
            try:
                return datetime.strptime(normalized, fmt).date()
            except ValueError:
                continue

        return None

    def to_db_date(self, date_string):
        parsed_date = self.parse_date(date_string)
        if parsed_date is None:
            raise ValueError("Invalid date format")

        return parsed_date.strftime("%Y-%m-%d")

    def display_cost(self):

        apartment_number = self.apartment_entry.get().strip()

        if not apartment_number:
            self.labelBanner.configure(text="Enter an apartment number first.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return

        apartment_id = Repair.get_apartment_id_by_number(self.db, apartment_number)
        if not apartment_id:
            self.labelBanner.configure(text="Apartment number not found.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return

        cost = Repair.calculate_total_cost(self.db, apartment_id)

        self.labelBanner.configure(text=f"Total maintenance cost for apartment {apartment_number}: £{cost}", fg_color=theme.INFO)
        self.labelFrame.grid()
        self.after(10000, lambda: self.labelFrame.grid_remove())

    def book_repair(self):

        issue = self.issue_entry.get().strip()
        repair_details = self.details_entry.get("1.0", "end").strip()
        apartment_number = self.apartment_entry.get().strip()
        date = self.date_entry.get().strip()
        priority = self.priority_box.get()

        if not issue or not repair_details or not apartment_number or not date:
            self.labelBanner.configure(text="Please fill in all fields.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return

        if priority not in {"1", "2", "3"}:
            self.labelBanner.configure(text="Priority must be 1, 2, or 3.", fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return

        if not self.valid_date(date):
            self.labelBanner.configure(
                text="Repair date cannot be in the past and must follow DD-MM-YY or DD-MM-YYYY.", 
                fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            return

        try:
            apartment_id = Repair.get_apartment_id_by_number(self.db, apartment_number)
            if not apartment_id:
                self.labelBanner.configure(text="Apartment number not found.", fg_color=theme.DANGER)
                self.labelFrame.grid()
                self.after(3000, lambda: self.labelFrame.grid_remove())
                return

            db_date = self.to_db_date(date)

            # Worker availability check and assignment (1 job per worker per day).
            # We select a maintenance user who has no job on the chosen date.
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
            SELECT u.userID
            FROM UserTbl u
            LEFT JOIN MaintenanceLog m
              ON m.userID = u.userID
             AND DATE(m.maintenanceDate) = DATE(%s)
            WHERE u.Role = 'maintenance'
              AND m.logID IS NULL
            ORDER BY u.userID
            LIMIT 1
            """, (db_date,))
            available_worker_row = cursor.fetchone()
            if not available_worker_row:
                self.labelBanner.configure(
                    text="No maintenance worker is available that day. Please pick another date.", 
                    fg_color=theme.WARNING)
                self.labelFrame.grid()
                self.after(10000, lambda: self.labelFrame.grid_remove())
                return

            assigned_worker_id = available_worker_row["userID"]

            Repair.log_maintenance(
                apartment_id,
                assigned_worker_id,
                db_date,
                issue,
                priority,
                repair_details,
            )

            self.labelBanner.configure(text="Repair booked successfully, Tenant notification sent..", fg_color=theme.SUCCESS)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())
            self.clear_form()

        except Exception as e:
            self.labelBanner.configure(text=str(e), fg_color=theme.DANGER)
            self.labelFrame.grid()
            self.after(3000, lambda: self.labelFrame.grid_remove())

    def clear_form(self):

        self.issue_entry.delete(0, "end")
        self.details_entry.delete("1.0", "end")
        self.apartment_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.priority_box.set("2")
