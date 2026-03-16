from models.db import Database
from datetime import datetime, timedelta

class FinanceModel:
    @staticmethod
    def get_invoice_summary():
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('''
            SELECT
                COUNT(*) as total_invoices,
                SUM(CASE WHEN Status = 'pending' THEN Amount ELSE 0 END) as pending_total,
                SUM(CASE WHEN Status = 'overdue' THEN Amount ELSE 0 END) as overdue_total,
                SUM(CASE WHEN Status = 'paid' THEN Amount ELSE 0 END) as paid_total,
                COUNT(CASE WHEN Status = 'pending' THEN 1 END) as pending_count,
                COUNT(CASE WHEN Status = 'overdue' THEN 1 END) as overdue_count,
                COUNT(CASE WHEN Status = 'paid' THEN 1 END) as paid_count
            FROM Invoice
        ''')
        return cursor.fetchone()

    @staticmethod
    def get_recent_transactions(limit=10):
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate, i.Status,
                   i.Created_at, t.fullName, a.apartmentNumber
            FROM Invoice i
            JOIN LeaseAgreement ls ON i.leaseID = ls.leaseID
            JOIN Tenant t ON ls.tenantID = t.tenantID
            JOIN Apartment a ON ls.apartmentID = a.apartmentID
            ORDER BY i.Created_at DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    @staticmethod
    def get_upcoming_due_dates(days=7):
        db = Database()
        cursor = db.get_cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        future = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate, t.fullName, a.apartmentNumber
            FROM Invoice i
            JOIN LeaseAgreement ls ON i.leaseID = ls.leaseID
            JOIN Tenant t ON ls.tenantID = t.tenantID
            JOIN Apartment a ON ls.apartmentID = a.apartmentID
            WHERE i.Status IN ('pending', 'overdue')
            AND i.dueDate BETWEEN ? AND ?
            ORDER BY i.dueDate ASC
        ''', (today, future))
        return cursor.fetchall()