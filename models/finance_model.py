from db import db as dbfunc
from . import user_session

class FinanceModel:

    def get_summary(self):
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                COUNT(*),
                SUM(CASE WHEN i.Status="pending"
                    THEN Amount ELSE 0 END),
                SUM(CASE WHEN i.Status="overdue"
                    THEN Amount ELSE 0 END),
                SUM(CASE WHEN i.Status="paid"
                    THEN Amount ELSE 0 END),
                COUNT(CASE WHEN i.Status="pending" THEN 1 END),
                COUNT(CASE WHEN i.Status="overdue" THEN 1 END),
                COUNT(CASE WHEN i.Status="paid"    THEN 1 END)
            FROM Invoice i JOIN LeaseAgreement la ON la.leaseID = i.leaseID
            JOIN Apartment a ON la.apartmentID = a.apartmentID
            WHERE a.locationID = %s''', (user_session.user_base,))
        try:
            row = cursor.fetchone()
            if not row or row[0] == 0:
                return self._empty_summary()

            total, pend, over, paid, pend_n, over_n, paid_n = row
            pend = float(pend or 0)
            over  = float(over  or 0)
            paid  = float(paid  or 0)
            outstanding = pend + over
            revenue     = paid + outstanding
            rate = (paid / revenue * 100) if revenue > 0 else 0

            return {
                "total":       total,
                "pending":     f"£{pend:,.2f}",
                "overdue":     f"£{over:,.2f}",
                "paid":        f"£{paid:,.2f}",
                "outstanding": f"£{outstanding:,.2f}",
                "rate":        f"{rate:.1f}%",
                "pending_n":   pend_n or 0,
                "overdue_n":   over_n or 0,
                "paid_n":      paid_n or 0
            }
        except Exception as e:
            print(f"Finance summary error: {e}")
            return self._empty_summary()
        
    def _empty_summary(self):
        return {
            "total":       0,
            "pending":     "£0.00",
            "overdue":     "£0.00",
            "paid":        "£0.00",
            "outstanding": "£0.00",
            "rate":        "0%",
            "pending_n":   0,
            "overdue_n":   0,
            "paid_n":      0
        }

    @staticmethod
    def get_recent_transactions(limit=10):
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
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
            WHERE a.locationID = %s
            ORDER BY i.Created_at DESC
            LIMIT %s
        ''', (user_session.user_base, limit))

        try:
            rows = cursor.fetchall()
            result = []
            for r in rows:
                amt = float(r[1])
                result.append({
                    "invoice": r[0],
                    "amount":  f"£{amt:,.2f}",
                    "due":     str(r[2]),
                    "status":  r[3].capitalize(),
                    "tenant":  r[4],
                    "apt":     r[5]
                })
            return result
        except Exception as e:
            print(f"Finance transactions error: {e}")
            return []
    
    @staticmethod
    def get_upcoming_dues():
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
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
            WHERE i.Status IN ("pending", "overdue") AND a.locationID=%s
            ORDER BY i.dueDate ASC
            LIMIT 10''', (user_session.user_base,))
        
        try:
            rows = cursor.fetchall()
            return [{
                "invoice": r[0],
                "amount":  f"£{float(r[1]):,.2f}",
                "due":     str(r[2]),
                "tenant":  r[3],
                "apt":     r[4]
            } for r in rows]
        except Exception as e:
            print(f"Finance dues error: {e}")
            return []

