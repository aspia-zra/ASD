import unittest
import time
from models.front_desk import FrontDesk
from db import db

class TestFrontDeskIntegration(unittest.TestCase):
    def setUp(self):
        self.fd = FrontDesk()
        self.email = "frontdesk@test.com"

    def testInsertTenant(self):
        conn = db.get_connection()
        cursor = conn.cursor()

        self.fd.insert_tenant(
            "Test Tenant",
            "07123456789",
            "ABC123456",
            self.email
        )

        cursor.execute("SELECT * FROM UserTbl WHERE Email = %s", (self.email,))
        result = cursor.fetchone()

        self.assertIsNotNone(result)

        cursor.execute("DELETE FROM UserTbl WHERE Email = %s", (self.email,))
        cursor.execute("DELETE FROM Tenant WHERE userID = %s", (result[0],))
        conn.commit()

        cursor.close()
        conn.close()

    def testGetAllTenants(self): 
        result = self.fd.get_all_tenants()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def testGetTenantByID(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        self.email = f"frontdesk_{int(time.time())}@test.com"

        self.fd.insert_tenant(
            "Test Tenant",
            "07123456789",
            "ABC123456",
            self.email
        )

        cursor.execute(""" SELECT t.tenantID from Tenant t
            JOIN UserTbl u ON t.userID = u.userID WHERE u.Email = %s
        """, (self.email,))
        tenantID = cursor.fetchone()[0]

        testResult = self.fd.get_tenant_by_id(tenantID)

        cursor.execute("SELECT * FROM Tenant WHERE tenantID = %s", (tenantID,))
        result = cursor.fetchone()

        self.assertEqual(result, testResult)

        cursor.execute("DELETE FROM UserTbl WHERE Email = %s", (self.email,))
        cursor.execute("DELETE FROM Tenant WHERE tenantID = %s", (tenantID,))
        conn.commit()

        cursor.close()
        conn.close()

    def testUpdateUser(self): #update_user(self, tenant_id, name, phone, ni_number, email):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        self.fd.insert_tenant( 
            "Test Tenant",
            "07123456789",
            "ABC123456",
            self.email
        )

        cursor.execute("""SELECT t.tenantID FROM Tenant t 
            JOIN UserTbl u ON t.userID = u.userID
            WHERE Email = %s""", (self.email,))
        tenantRow = cursor.fetchone()
        tenantID = tenantRow['tenantID']

        name = "Update User Test"
        phone = "07987654321"
        niNumber = "XYZ123456"
        newemail = "update-frontdesk@test.com"
        self.fd.update_user(tenantID, name, phone, niNumber, newemail)

        cursor.execute("""SELECT u.fullName, u.Phone, t.national_Insurance, t.Email
            FROM Tenant t JOIN UserTbl u ON t.userID = u.userID
            WHERE tenantID = %s""", (tenantID,))
        result = cursor.fetchone()

        self.assertEqual(result['fullName'], name)
        self.assertEqual(result['Phone'], phone)
        self.assertEqual(result['national_Insurance'], niNumber)
        
        cursor.execute("DELETE FROM UserTbl WHERE Email = %s", (self.email,))
        cursor.execute("DELETE FROM Tenant WHERE tenantID = %s", (tenantID,))
        conn.commit()

        cursor.close()
        conn.close()

    def testAssignApt(self):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        self.fd.insert_tenant(
            "Test Tenant",
            "07123456789",
            "ABC123456",
            self.email
        )

        cursor.execute("""SELECT t.tenantID FROM Tenant t 
            JOIN UserTbl u ON t.userID = u.userID
            WHERE Email = %s""", (self.email,))
        tenantRow = cursor.fetchone()
        tenantID = tenantRow['tenantID']

        cursor.execute("""SELECT apartmentID FROM Apartment 
            WHERE status='available' LIMIT 1""")
        aptRow = cursor.fetchone()

        if aptRow:
            apartmentID = aptRow['apartmentID']
            self.fd.assign_apartment(tenantID, apartmentID, 1000, 2)

            cursor.execute("""SELECT * FROM LeaseAgreement 
                WHERE tenantID = %s AND apartmentID = %s
                """, (tenantID, apartmentID))
            lease = cursor.fetchone()

            self.assertIsNotNone(lease)

            cursor.execute("""SELECT Status FROM Apartment 
                WHERE apartmentID = %s""", (apartmentID,))
            apt = cursor.fetchone()
            self.assertEqual(apt['Status'],'occupied')

        cursor.execute("""DELETE FROM LeaseAgreement 
            WHERE leaseID = %s""", (lease['leaseID']))
        cursor.execute("""UPDATE Apartment SET Status='available' 
            WHERE apartmentID = %s""", (apt['apartmentID']))
        cursor.execute("DELETE FROM UserTbl WHERE Email = %s", (self.email,))
        cursor.execute("DELETE FROM Tenant WHERE tenantID = %s", (tenantID,))
        conn.commit()

        cursor.close()
        conn.close()

    def testDeleteUser(self):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        self.fd.insert_tenant(
            "Test Tenant",
            "07123456789",
            "ABC123456",
            self.email
        )

        cursor.execute("""SELECT t.tenantID FROM Tenant t 
            JOIN UserTbl u ON t.userID = u.userID
            WHERE Email = %s""", (self.email,))
        tenantRow = cursor.fetchone()
        tenantID = tenantRow['tenantID']

        self.fd.delete_user(tenantID)
        cursor.execute("SELECT * FROM Tenant WHERE tenantID = %s" ,(tenantID,))
        result = cursor.fetchone()
        self.assertIsNone(result)

        cursor.close()
        conn.close()
    
    def testGetAllApt(self):
        result = self.fd.get_all_apartments()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()