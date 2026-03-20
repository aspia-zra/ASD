import tkinter as tk
from tkinter import messagebox
from database import insert_tenant, get_all_tenants
import re

#Themes- work on font
BG_COLOR = "#f5f3ff"
SIDEBAR_COLOR = "#ede9fe"
CARD_COLOR = "#ffffff"
ACCENT_COLOR = "#7c3aed"
SUB_ACCENT = "#a78bfa"
TEXT_COLOR = "#1f1f1f"
ENTRY_BG = "#f3e8ff"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")


def clear_main():
    for widget in main_frame.winfo_children():
        widget.destroy()

def is_valid_phone(phone):
    phone = phone.replace(" ", "")

    return bool(re.fullmatch(r"0\d{10}", phone))

#Register page
def show_register():
    clear_main()

    tk.Label(main_frame, text="Register Tenant",
             font=FONT_HEADER, fg=ACCENT_COLOR,
             bg=BG_COLOR).pack(anchor="w", pady=10)

    card = tk.Frame(main_frame, bg=CARD_COLOR)
    card.pack(padx=10, pady=10, fill="both")

    form = tk.Frame(card, bg=CARD_COLOR)
    form.pack(padx=30, pady=30)

    def make_row(text, row):
        tk.Label(form, text=text, font=FONT_LABEL,
                 bg=CARD_COLOR).grid(row=row, column=0, sticky="w", pady=10)

        entry = tk.Entry(form, width=35, font=FONT_ENTRY,
                         bg=ENTRY_BG, relief="flat")
        entry.grid(row=row, column=1, pady=10, padx=15)
        return entry

    global entry_name, entry_phone, entry_ni, entry_email
    entry_name = make_row("Full Name:", 0)
    entry_phone = make_row("Phone:", 1)
    entry_ni = make_row("NI Number:", 2)
    entry_email = make_row("Email:", 3)

    def submit():
        full_name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        ni = entry_ni.get().strip().upper()
        email = entry_email.get().strip()

        if not full_name or not phone or not ni or not email:
            messagebox.showerror("Error", "All fields are required")
            return

        if not is_valid_phone(phone):
            messagebox.showerror("Error", "Phone number must be 11 digits and start with 0")
            return
    
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format")
            return

        try:
            insert_tenant(full_name, phone, ni, email)
            messagebox.showinfo("Success", "Tenant registered")

            entry_name.delete(0, tk.END)
            entry_phone.delete(0, tk.END)
            entry_ni.delete(0, tk.END)
            entry_email.delete(0, tk.END)

        except Exception:
            messagebox.showerror("Error", "Email already exists")

    tk.Button(card, text="Register Tenant", font=FONT_BTN,
              bg=ACCENT_COLOR, fg="white", width=20,
              relief="flat", command=submit).pack(pady=20)


#Tenant list page
def show_list():
    clear_main()

    tk.Label(main_frame, text="Tenant List",
             font=FONT_HEADER, fg=ACCENT_COLOR,
             bg=BG_COLOR).pack(anchor="w", pady=10)

    card = tk.Frame(main_frame, bg=CARD_COLOR, highlightthickness=1, highlightbackground=SUB_ACCENT)
    card.pack(padx=10, pady=10, fill="both", expand=True)

    headers = ["ID", "Name", "Phone", "NIN", "Email"]
    col_widths = [6, 18, 14, 14, 32]

    header_frame = tk.Frame(card, bg=ACCENT_COLOR)
    header_frame.pack(fill="x")

    for i, h in enumerate(headers):
        tk.Label(header_frame, text=h,
                 font=FONT_BTN,
                 bg=ACCENT_COLOR, fg="white",
                 width=col_widths[i],
                 anchor="w", padx=6,
                 relief="solid", bd=1).grid(row=0, column=i, sticky="nsew")

    body = tk.Frame(card, bg=CARD_COLOR)
    body.pack(fill="both", expand=True)

    tenants = get_all_tenants()

    for r, tenant in enumerate(tenants):
        for c, val in enumerate(tenant):
            bg = ENTRY_BG if r % 2 == 0 else "white"

            tk.Label(body, text=val,
                     bg=bg,
                     fg=TEXT_COLOR,
                     width=col_widths[c],
                     anchor="w",
                     padx=6,
                     relief="solid", bd=1).grid(row=r, column=c, sticky="nsew")
            
#search up tenant page
def show_search():
    clear_main()

    tk.Label(main_frame, text="Search Tenant",
             font=FONT_HEADER, fg=ACCENT_COLOR,
             bg=BG_COLOR).pack(anchor="w", pady=10)

    card = tk.Frame(main_frame, bg=CARD_COLOR)
    card.pack(padx=10, pady=10, fill="both")

    tk.Label(card, text="Search by Name:", bg=CARD_COLOR).pack(pady=10)

    search_entry = tk.Entry(card, width=40, bg=ENTRY_BG, relief="flat")
    search_entry.pack(pady=5)

    result_frame = tk.Frame(card, bg=CARD_COLOR)
    result_frame.pack(pady=15)

    def search():
        for w in result_frame.winfo_children():
            w.destroy()

        term = search_entry.get().strip().lower()

        tenants = get_all_tenants()

        for tenant in tenants:
            if term in tenant[1].lower():
                tk.Label(result_frame, text=f"{tenant[1]} — {tenant[4]}",
                         bg=CARD_COLOR).pack(anchor="w")

    tk.Button(card, text="Search", bg=ACCENT_COLOR, fg="white",
              relief="flat", width=15, command=search).pack(pady=10)


#home window
root = tk.Tk()
root.title("Tenant Management System")
root.geometry("900x500")
root.configure(bg=BG_COLOR)

#sidebar
sidebar = tk.Frame(root, bg=SIDEBAR_COLOR, width=180)
sidebar.pack(side="left", fill="y")

tk.Label(sidebar, text="Paragon",
         font=("Segoe UI", 16, "bold"),
         bg=SIDEBAR_COLOR, fg=ACCENT_COLOR).pack(pady=20)

def nav_btn(text, cmd):
    return tk.Button(sidebar, text=text, font=FONT_BTN,
                     bg=SIDEBAR_COLOR, fg=TEXT_COLOR,
                     relief="flat", anchor="w",
                     command=cmd)

nav_btn("➕ Register Tenant", show_register).pack(fill="x", pady=5, padx=15)
nav_btn("📋 View Tenants", show_list).pack(fill="x", pady=5, padx=15)
nav_btn("🔍 Search Tenant", show_search).pack(fill="x", pady=5, padx=15)


main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

show_register()

root.mainloop()