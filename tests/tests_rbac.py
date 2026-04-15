# this file tests least-privilege access, one of the requirements
# test if the other staff can access the wrong dashboards
# check role-restricted actions
    # add apartment
    # assign apartment
    # view finance data
    # submit complaint
  
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    
import unittest
import customtkinter
from models import user_session
from gui.nav import navbar
from gui.page_mdash import mngdashboard
from gui.app import App
from db.db_connect import Database
from models.front_desk import FrontDesk
from models.mngdash import mngBE
from models.finance_model import FinanceModel
from models.repairs import Repair


db = Database()

class test_rbac(unittest.TestCase):
    
    def setUp(self):
        self.app = App()
    def tearDown(self):
        self.app.destroy()
    def test_finance_access_mngdash(self): #can finance staff access management dashboards?
        user_session.user_type="finance"
        controller = App()
        page = mngdashboard(controller)
        self.assertIsNotNone(page)
        if hasattr(db, 'close'):
            db.close()
    
        
    # test auth access with assertTrue; unauth access with assertFalse; for invalid role assertfalse;
    
    # invalid role?
    def test_valid_add_apt(self):
        user_session.user_type = "manager"
        model = mngBE()
        result = model.add_apartment("A999", "London", 1200, "Available")
        self.assertTrue(result) # managers can add apartments
        if hasattr(db, 'close'):
            db.close()                      
        
    def test_invalid_add_apt(self): #finance_Staff should not be able to add apartments
        user_session.user_type = "finance"
        model = mngBE()
        result = model.add_apartment("A999", "London", 1200, "Available")
        self.assertFalse(result)
        if hasattr(db, 'close'):
            db.close()
        
    
    def test_valid_assign_apt(self):
        user_session.user_type = "frontdesk"
        model = FrontDesk()
        result = model.assign_apartment("1", "A103")
        self.assertTrue(result) # staff can assign apartments
        if hasattr(db, 'close'):
            db.close()
            
            
    def test_invalid_assign_apt(self):
        user_session.user_type = "finance"
        model = FrontDesk()
        result = model.assign_apartment("1", "A103")
        self.assertFalse(result) # finance staff can't assign apartments
        if hasattr(db, 'close'):
            db.close() 
    
    def test_valid_view_finance_data(self):
        user_session.user_type = "finance" #staff view reports
        user_session.user_base = 1
        model = FinanceModel()
        result = model.get_summary()   
        self.assertIsInstance(result, dict)
        self.assertIn("total", result)
        self.assertIn("paid", result)
        if hasattr(db, 'close'):
            db.close()
            
    def test_invalid_view_finance_data(self):
        user_session.user_type = "frontdesk"  # not allowed
        user_session.user_base = 1
        model = FinanceModel()
        result = model.get_summary()
        self.assertIsInstance(result, dict)
        if hasattr(db, 'close'):
            db.close()
    
    def test_valid_submit_complaint(self):
        user_session.user_type = "maintenance"
        model = Repair()
        result = model.add_complaint("Leaky tap", "3", "A103", "Tap")
        self.assertTrue(result) # staff can assign apartments
        if hasattr(db, 'close'):
            db.close()

            
    def test_invalid_submit_complaint(self):
        user_session.user_type = "finance"
        model = Repair()
        result = model.add_complaint("Leaky tap", "3", "A103", "Tap")
        self.assertFalse(result) # staff can assign apartments
        if hasattr(db, 'close'):
            db.close()
