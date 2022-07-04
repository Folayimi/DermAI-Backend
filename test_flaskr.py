import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, User


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "dermai_test"
        self.database_password = "Florinfix$321"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres',self.database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    creates at least a test for each successful operation and for expected errors.
    """
    
    def test_cofirm_user(self):
        res = self.client().post('/getpassList', json={'email':"ridwanfolayimi@gmail.com", 'password':"Rinfinix"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['password'],'Rinfinix') 
               
    # def test_404_user_not_found(self):
    #     res = self.client().post('/getpassList', json={'email':"ridwanfolayimi@gmail.com", 'password':"Rinfinix"})
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'],False)
    #     self.assertEqual(data['message'],'resource not found')        
    
    # def test_create_user(self):
    #     res = self.client().post('/postUserDetails', json={'fullname':'Ridwan Ogunlade','email':"ridwanfolayimi@gmail.com", 'password':"Rinfinix"})
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['delivered'],True)        
               
    # def test_422_bad_request(self):
    #     res = self.client().post('/postUserDetails', json={})
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'],False)
    #     self.assertEqual(data['message'],'unprocessable')
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()