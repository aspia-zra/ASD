
from models.db import Database


def get_all_invoices():
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("""
    SELECT i.invoiceID, t.fullName, i.Amount, i.dueDate, i.Status
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    JOIN Tenant t ON l.tenantID = t.tenantID
    ORDER BY i.dueDate DESC
    """)

    data = cursor.fetchall()
    return data


def get_overdue_invoices():
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("""
    SELECT i.invoiceID, t.fullName, i.Amount, i.dueDate, i.Status
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    JOIN Tenant t ON l.tenantID = t.tenantID
    WHERE i.Status = 'overdue'
    ORDER BY i.dueDate ASC
    """)

    data = cursor.fetchall()
    return data


def mark_invoice_paid(invoice_id):
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("UPDATE Invoice SET Status = 'paid' WHERE invoiceID = %s", (invoice_id,))
    db.commit()


def reset_invoice_status(invoice_id):
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("UPDATE Invoice SET Status = 'pending' WHERE invoiceID = %s", (invoice_id,))
    db.commit()


def check_any_overdue():
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("SELECT COUNT(*) FROM Invoice WHERE Status = 'overdue'")
    result = cursor.fetchone()[0]
    return result > 0