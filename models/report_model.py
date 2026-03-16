from models.db import Database

class ReportModel:
    @staticmethod
    def get_occupancy_report(location=None):
        db = Database()
        cursor = db.get_cursor()
        if location:
            cursor.execute('''
                SELECT a.apartmentID, a.Type, a.Status, l.City, t.fullName
                FROM Apartment a
                JOIN Location l ON a.locationID = l.locationID
                LEFT JOIN LeaseAgreement ls ON a.apartmentID = ls.apartmentID AND ls.Status = 'active'
                LEFT JOIN Tenant t ON ls.tenantID = t.tenantID
                WHERE l.City = ?
            ''', (location,))
        else:
            cursor.execute('''
                SELECT a.apartmentID, a.Type, a.Status, l.City, t.fullName
                FROM Apartment a
                JOIN Location l ON a.locationID = l.locationID
                LEFT JOIN LeaseAgreement ls ON a.apartmentID = ls.apartmentID AND ls.Status = 'active'
                LEFT JOIN Tenant t ON ls.tenantID = t.tenantID
            ''')
        return cursor.fetchall()

    @staticmethod
    def get_financial_report():
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate, i.Status, t.fullName
            FROM Invoice i
            JOIN LeaseAgreement ls ON i.leaseID = ls.leaseID
            JOIN Tenant t ON ls.tenantID = t.tenantID
        ''')
        return cursor.fetchall()

    @staticmethod
    def get_maintenance_report():
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('''
            SELECT ml.logID, a.apartmentNumber, ml.maintenanceDate, ml.timeTaken, ml.Cost, ml.Notes
            FROM MaintenanceLog ml
            JOIN Apartment a ON ml.apartmentID = a.apartmentID
            ORDER BY ml.maintenanceDate DESC
        ''')
        return cursor.fetchall()

    @staticmethod
    def get_complaint_report():
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('''
            SELECT c.complaintID, c.Description, c.Severity, c.Status,
                   c.reportDate, t.fullName as tenant
            FROM Complaint c
            JOIN Tenant t ON c.tenantID = t.tenantID
            ORDER BY c.reportDate DESC
        ''')
        return cursor.fetchall()