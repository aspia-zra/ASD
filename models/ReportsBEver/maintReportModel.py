from models import user_session
from db import db

class ReportModel:
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
