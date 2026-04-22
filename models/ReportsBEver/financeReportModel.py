#Mercy Lang’At -24050109 
from models import user_session
from db import db

class ReportModel:
    @staticmethod
    def get_financial_report():
        conn = db.getconnection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate,
                   i.Status, u.fullName
            FROM Invoice i
            JOIN LeaseAgreement ls
                ON i.leaseID = ls.leaseID
            JOIN Tenant t
                ON ls.tenantID = t.tenantID
            JOIN UserTbl u
                ON t.userID = u.userID
            WHERE u.locationID = %s
            ORDER BY i.dueDate DESC''', (user_session.user_base,))
        rows = cursor.fetchall()

        total_paid = 0.0
        total_pending = 0.0
        total_overdue = 0.0
        data = []

        for r in rows:
            amt = float(r[1])
            st  = r[3].lower()
            if st == "paid":
                total_paid += amt
            elif st == "pending":
                total_pending += amt
            elif st == "overdue":
                total_overdue += amt
            data.append({
                "invoice": r[0],
                "amount":  f"£{amt:,.2f}",
                "due":     str(r[2]),
                "status":  r[3].capitalize(),
                "tenant":  r[4]
            })

        summary = {
            "paid":        f"£{total_paid:,.2f}",
            "pending":     f"£{total_pending:,.2f}",
            "overdue":     f"£{total_overdue:,.2f}",
            "outstanding": f"£{total_pending + total_overdue:,.2f}"
        }

        cursor.close()
        conn.close()
        
        return data, summary
