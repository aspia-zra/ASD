import unittest
from models.admindashBE import adminBE
from db import db

class TestAdminBEIntegration(unittest.TestCase):
    def testGetStaffData(self):
        result = adminBE.getStaffData()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def testAddStaff(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        adminBE.addStaff(
            "AdminBE Test",
            "07111111111",
            "adminBE@test.com",
            "password123",
            "admin"
        )

        cursor.execute("SELECT * FROM UserTbl WHERE Email = 'adminBE@test.com'")
        result = cursor.fetchone()

        self.assertIsNotNone(result)

        cursor.execute("DELETE FROM UserTbl WHERE Email = 'adminBE@test.com'")
        conn.commit()

        cursor.close()
        conn.close()

    def testEditStaff(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        editEmail = "edit-test@pams.com"
        cursor.execute("""
            INSERT INTO UserTbl (fullName, Phone, Email, Password, Role, locationID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ("Edit Test", "07000000001", editEmail, "pass", "manager", 1))
        conn.commit()

        cursor.execute("SELECT userID FROM UserTbl WHERE Email = %s", (editEmail,))
        user_id = cursor.fetchone()[0]

        adminBE.editStaff(user_id, "Edited Name", "07999999999", editEmail, "admin")
        conn.commit()

        cursor.execute("SELECT fullName FROM UserTbl WHERE userID = %s", (user_id,))
        updatedName = cursor.fetchone()[0]

        self.assertEqual(updatedName, "Edited Name")

        cursor.execute("DELETE FROM UserTbl WHERE userID = %s", (user_id,))
        conn.commit()

        cursor.close()
        conn.close()

    def testGetAptData(self):
        result = adminBE.getAptData()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()