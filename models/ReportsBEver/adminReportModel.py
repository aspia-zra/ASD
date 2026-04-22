#Mercy Lang’At -24050109 
from models import user_session
from db import db

class ReportModel:
    @staticmethod
    def get_occupancy_report():
        conn = db.getconnection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT a.apartmentNumber, a.Type,
                   a.monthlyRent, a.Status, l.City,
                   COUNT(ls.leaseID) AS num_tenants
            FROM Apartment a
            JOIN Location l
                ON a.locationID = l.locationID
            LEFT JOIN LeaseAgreement ls
                ON a.apartmentID = ls.apartmentID
                AND ls.Status = "active"
            WHERE l.locationID = %s
            GROUP BY a.apartmentID, a.apartmentNumber,
                    a.Type, a.monthlyRent,
                    a.Status, l.City''', (user_session.user_base,))
        rows = cursor.fetchall()
        result = [{
            "apartment": r[0],
            "type":      r[1],
            "rent":      f"£{float(r[2]):,.2f}",
            "status":    r[3],
            "city":      r[4],
            "tenants":   r[5]
        } for r in rows]

        cursor.close()
        conn.close()

        return result
    
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

    @staticmethod
    def get_maintenance_report():
        conn = db.getconnection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ml.logID, a.apartmentNumber,
                   ml.maintenanceDate, ml.timeTaken,
                   ml.Cost, COALESCE(ml.RepairDetails, "")
            FROM MaintenanceLog ml
            JOIN Apartment a
                ON ml.apartmentID = a.apartmentID
            WHERE a.locationID = %s
            ORDER BY ml.maintenanceDate DESC''', (user_session.user_base,))
        rows = cursor.fetchall()

        total_cost = 0.0
        total_hours = 0
        data = []

        for r in rows:
            cost  = float(r[4]) if r[4] else 0.0
            hours = int(r[3])   if r[3] else 0
            total_cost  += cost
            total_hours += hours
            data.append({
                "id":    r[0],
                "apt":   r[1],
                "date":  str(r[2]),
                "hours": hours,
                "cost":  f"£{cost:,.2f}",
                "notes": r[5]
            })

        summary = {
            "total_cost":  f"£{total_cost:,.2f}",
            "total_hours": str(total_hours)
        }

        cursor.close()
        conn.close()
        
        return data, summary
