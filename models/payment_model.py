

from db.db import get_connection


def get_all_invoices():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT i.invoiceID, t.fullName, i.Amount, i.dueDate, i.Status
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    JOIN Tenant t ON l.tenantID = t.tenantID
    ORDER BY i.dueDate DESC
    """

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def get_overdue_invoices():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT i.invoiceID, t.fullName, i.Amount, i.dueDate, i.Status
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    JOIN Tenant t ON l.tenantID = t.tenantID
    WHERE i.Status = 'overdue'
    ORDER BY i.dueDate ASC
    """

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def mark_invoice_paid(invoice_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Invoice SET Status = 'paid' WHERE invoiceID = %s"
    cursor.execute(query, (invoice_id,))
    conn.commit()
    conn.close()


def reset_invoice_status(invoice_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Invoice SET Status = 'pending' WHERE invoiceID = %s"
    cursor.execute(query, (invoice_id,))
    conn.commit()
    conn.close()


def check_any_overdue():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM Invoice WHERE Status = 'overdue'"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0