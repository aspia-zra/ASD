#Azra Rahman - 23022737 
from db import db
from datetime import datetime

class Complaints:
    def get_tenantID(self, apartmentnumber):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT apartmentID FROM Apartment WHERE apartmentNumber = %s", (apartmentnumber,))
        apartment_row = cursor.fetchone()
        if not apartment_row:
            return None

        lease_query = """
        SELECT tenantID
        FROM LeaseAgreement
        WHERE apartmentID = %s AND Status = 'active'
        """
        cursor.execute(lease_query, (apartment_row["apartmentID"],))
        lease_row = cursor.fetchone()
        if not lease_row:
            return None

        cursor.close()
        conn.close()
        return lease_row["tenantID"]

    def add_complaint(self, reason, severity, apartmentnumber, complaintdetail):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT apartmentID FROM Apartment WHERE apartmentNumber = %s",(apartmentnumber,))
        apartment_row = cursor.fetchone()
        if not apartment_row:
            return False

        lease_query = """
        SELECT tenantID
        FROM LeaseAgreement
        WHERE apartmentID = %s AND Status = 'active'
        """
        cursor.execute(lease_query, (apartment_row["apartmentID"],))
        lease_row = cursor.fetchone()
        if not lease_row:
            return False

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = """
        INSERT INTO Complaint (tenantID, apartmentID, Initial_Issue, Description, reportDate, Severity, Status)
        VALUES (%s, %s, %s, %s, %s, %s, 'open')
        """

        cursor.execute(
            query,
            (
                lease_row["tenantID"],
                apartment_row["apartmentID"],
                (complaintdetail or "").strip(),
                (reason or "").strip(),
                timestamp,
                severity,
            ),
        )
        conn.commit()

        cursor.close()
        conn.close()
        return True
