from models.db import Database


class ReportModel:

    @staticmethod
    def get_occupancy_report(city=None):
        db = Database()
        cursor = db.get_cursor()
        if city:
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
                WHERE l.City = %s
                GROUP BY a.apartmentID, a.apartmentNumber,
                         a.Type, a.monthlyRent,
                         a.Status, l.City
            ''', (city,))
        else:
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
                GROUP BY a.apartmentID, a.apartmentNumber,
                         a.Type, a.monthlyRent,
                         a.Status, l.City
            ''')
        return cursor.fetchall()

    @staticmethod
    def get_financial_report():
        db = Database()
        cursor = db.get_cursor()
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
            ORDER BY i.dueDate DESC
        ''')
        return cursor.fetchall()

    @staticmethod
    def get_maintenance_report():
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('''
            SELECT ml.logID, a.apartmentNumber,
                   ml.maintenanceDate, ml.timeTaken,
                   ml.Cost, COALESCE(ml.Notes, "")
            FROM MaintenanceLog ml
            JOIN Apartment a
                ON ml.apartmentID = a.apartmentID
            ORDER BY ml.maintenanceDate DESC
        ''')
        return cursor.fetchall()