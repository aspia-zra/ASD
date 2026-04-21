from db.db import *
import re
from datetime import date
from dateutil.relativedelta import relativedelta

class FrontDesk:

    def insert_tenant(self, name, phone, ni_number, email):
        conn = get_connection()
        cursor = conn.cursor()
        role = 'tenant'
        password = 'password'

        query = "INSERT INTO usertbl (fullName, Phone, Email, Role, Password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, phone, email, role, password))
        conn.commit()

        cursor.execute("SELECT userID FROM UserTbl WHERE Email = %s", (email,))
        userID = cursor.fetchone()[0]
        query = """INSERT INTO tenant (userID, national_Insurance, Email) 
            VALUES (%s, %s, %s)"""
        cursor.execute(query, (userID, ni_number, email))
        conn.commit()
        cursor.close()
        conn.close()

    def register_tenant(self, name, phone, ni, email):
        if not name or not phone or not ni or not email:
            raise ValueError("All fields are required")

        if not self.is_valid_phone(phone):
            raise ValueError("Phone must be 11 digits starting with 0")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        self.insert_tenant(name, phone, ni, email)

    def get_all_tenants(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) 
        query = ("""SELECT t.tenantID, u.fullName, u.Phone, t.national_Insurance, t.Email, u.Created_at, t.status 
            FROM Tenant t JOIN UserTbl u ON t.userID = u.userID""")
        cursor.execute(query)
        tenants = cursor.fetchall()
        cursor.close()
        conn.close()
        return tenants

    def get_tenant_by_id(self, tenant_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM tenant WHERE tenantID=%s""", (tenant_id,))
        tenant = cursor.fetchone()
        cursor.close()
        conn.close()
        return tenant

    def update_user(self, tenantID, name, phone, ni_number, email):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT userID FROM Tenant WHERE tenantID = %s", (tenantID,))
        userID = cursor.fetchone()[0]

        cursor.execute (""" UPDATE Tenant SET national_Insurance = %s, Email = %s 
            WHERE tenantID = %s""", (ni_number, email, tenantID,))
        cursor.execute("""UPDATE UserTbl SET fullName = %s, Phone = %s,
            Email = %s WHERE userID = %s""", (name, phone, email, userID))

        conn.commit()
        cursor.close()
        conn.close()
    
    def assign_apartment(self, tenant_id, apartment_id, depositAmount, duration):
        conn = get_connection()
        cursor = conn.cursor()

        startDate = date.today()
        endDate = startDate + relativedelta(years=duration)
        
        cursor.execute(""" INSERT INTO LeaseAgreement (tenantID, apartmentID, 
                startDate, endDate, depositAmount, Status) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
            (tenant_id, apartment_id, startDate, endDate, depositAmount, 'active'))
        
        cursor.execute(""" UPDATE Apartment SET Status = 'occupied' 
        WHERE apartmentID = %s """, (apartment_id,))
        conn.commit()

        cursor.close()
        conn.close()

    def delete_user(self, tenantID):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT userID FROM Tenant WHERE tenantID = %s", (tenantID,))
        userID = cursor.fetchone()[0]

        cursor.execute("DELETE FROM Tenant WHERE tenantID = %s", (tenantID,))
        cursor.execute("DELETE FROM UserTbl WHERE userID = %s", (userID))
        conn.commit()

        cursor.close()
        conn.close()

    def is_valid_phone(self, phone):
        return re.match(r"^0\d{10}$", phone) is not None
    
    def get_all_apartments(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT apartmentID FROM apartment WHERE status='available'")
        apartments = [row['apartmentID'] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return apartments
