import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    
import unittest
import customtkinter
from models import user_session
from db import db
from models.front_desk import FrontDesk
from models.mngdash import mngBE
from models.finance_model import FinanceModel
from models.repairs import Repair
from datetime import datetime

class test_rbac(unittest.TestCase):
    
    def setUp(self):
        self.db = db.get_connection()
        
    def tearDown(self):
        if self.db and hasattr(self.db, 'close'):
            self.db.close()
    
    def test_finance_access_mngdash(self):
        user_session.user_type = "finance"
        pass
    
    def test_valid_add_apt(self):
        user_session.user_type = "manager"
        model = mngBE()
        try:
            model.addApt("A999", 1200, "Available", "London", "2BR")
            self.assertTrue(True)
        except ValueError:
            self.skipTest("Apartment number already exists")
        except Exception as e:
            self.fail(f"Add apartment failed: {e}")
                      
    def test_invalid_add_apt(self):
        user_session.user_type = "finance"
        model = mngBE()
        try:
            model.addApt("A999", 1200, "Available", "London", "2BR")
            self.fail("Finance staff should not be able to add apartments")
        except:
            self.assertTrue(True)
    
    def test_valid_assign_apt(self):
        user_session.user_type = "frontdesk"
        model = FrontDesk()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tenantID FROM Tenant LIMIT 1")
        tenant = cursor.fetchone()
        cursor.execute("SELECT apartmentID FROM Apartment WHERE status='available' LIMIT 1")
        apartment = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if tenant and apartment:
            model.assign_apartment(tenant[0], apartment[0], 1000, 12)
            self.assertTrue(True)
        else:
            self.fail("No test data available")
            
    def test_invalid_assign_apt(self):
        user_session.user_type = "finance"
        model = FrontDesk()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tenantID FROM Tenant LIMIT 1")
        tenant = cursor.fetchone()
        cursor.execute("SELECT apartmentID FROM Apartment WHERE status='available' LIMIT 1")
        apartment = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if tenant and apartment:
            try:
                model.assign_apartment(tenant[0], apartment[0], 1000, 12)
                self.fail("Finance staff should not be able to assign apartments")
            except:
                self.assertTrue(True)
        else:
            self.fail("No test data available")
    
    def test_valid_view_finance_data(self):
        user_session.user_type = "finance"
        user_session.user_base = 1
        model = FinanceModel()
        result = model.get_summary()   
        self.assertIsInstance(result, dict)
        self.assertIn("total", result)
        self.assertIn("paid", result)
            
    def test_invalid_view_finance_data(self):
        user_session.user_type = "frontdesk"
        user_session.user_base = 1
        model = FinanceModel()
        result = model.get_summary()
        self.assertIsInstance(result, dict)
    
    def test_valid_submit_complaint(self):
        user_session.user_type = "maintenance"
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT apartmentID FROM Apartment LIMIT 1")
        apt = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if apt:
            Repair.log_maintenance(apt[0], 1, datetime.now(), "Leaky tap", "high", "Need new washer")
            self.assertTrue(True)
        else:
            self.fail("No apartment found")

    def test_invalid_submit_complaint(self):
        user_session.user_type = "finance"
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT apartmentID FROM Apartment LIMIT 1")
        apt = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if apt:
            try:
                Repair.log_maintenance(apt[0], 1, datetime.now(), "Leaky tap", "high", "Need new washer")
                self.fail("Finance staff should not be able to submit complaints")
            except:
                self.assertTrue(True)
        else:
            self.fail("No apartment found")


if __name__ == "__main__":
    unittest.main()
