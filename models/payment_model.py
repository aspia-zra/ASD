from models.db import Database
from datetime import datetime, timedelta


class FinanceModel:

    @staticmethod
    def get_summary():
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('''
            SELECT
                COUNT(*),
                SUM(CASE WHEN Status="pending"
                    THEN Amount ELSE 0 END),
                SUM(CASE WHEN Status="overdue"
                    THEN Amount ELSE 0 END),
                SUM(CASE WHEN Status="paid"
                    THEN Amount ELSE 0 END),
                COUNT(CASE WHEN Status="pending" THEN 1 END),
                COUNT(CASE WHEN Status="overdue" THEN 1 END),
                COUNT(CASE WHEN Status="paid"    THEN 1 END)
            FROM Invoice
        ''')
        return cursor.fetchone()

    @staticmethod
    def get_recent_transactions(limit=10):
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate,
                   i.Status, u.fullName, a.apartmentNumber
            FROM Invoice i
            JOIN LeaseAgreement ls
                ON i.leaseID = ls.leaseID
            JOIN Tenant t
                ON ls.tenantID = t.tenantID
            JOIN UserTbl u
                ON t.userID = u.userID
            JOIN Apartment a
                ON ls.apartmentID = a.apartmentID
            ORDER BY i.Created_at DESC
            LIMIT %s
        ''', (limit,))
        return cursor.fetchall()

    @staticmethod
    def get_upcoming_dues(days=7):
        db = Database()
        cursor = db.get_cursor()
        today  = datetime.now().strftime('%Y-%m-%d')
        future = (datetime.now() +
                  timedelta(days=days)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate,
                   u.fullName, a.apartmentNumber
            FROM Invoice i
            JOIN LeaseAgreement ls
                ON i.leaseID = ls.leaseID
            JOIN Tenant t
                ON ls.tenantID = t.tenantID
            JOIN UserTbl u
                ON t.userID = u.userID
            JOIN Apartment a
                ON ls.apartmentID = a.apartmentID
            WHERE i.Status IN ("pending","overdue")
              AND i.dueDate BETWEEN %s AND %s
            ORDER BY i.dueDate ASC
        ''', (today, future))
        return cursor.fetchall()