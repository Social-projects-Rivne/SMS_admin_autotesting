import unittest
from flask import session, url_for, request, redirect, Flask
from functools import wraps

from app.controllers.controller import AdminController
import app.urls
from app.utils.login_required import login_required
from app import app




class TestLoginRequired(unittest.TestCase):
    
    def setUp(self):
        """Prepare the initial data for tests"""
        self.controller = AdminController()
        
        self.appt = app.test_client()
        self.appt.testing = True
        self.appt.debug = True
        self.appt.SECRET_KEY = 'F12Zr47j\3yX R~X@H!jmM]L'
        
        self.dict_user = {'id' : 1,
                          'login' : 'username',
                          'password' : 'password'}

    def teardown(self):
        """Delete the preparation data for tests"""
        try: 
            session.pop('login', None)
        except Exception as error:
            print(error)
        finally:
            session.close()
        
    def test_login_required_True_response(self):
        """Test the path redirection when user is logged in using 
        test_client()"""
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
            response = a.get(path = '/index', 
                             method = "POST",
                             data = self.dict_user)

            #print str(response)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Головна сторінка | SMS', response.data)

    def test_login_required_True_context(self):
        """Test the path redirection when user is logged in using context"""
        with app.test_request_context(path = '/index', 
                                      method = "POST",
                                      data = self.dict_user):
            with self.appt.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
            response = self.controller.get_index()
            #print response
            self.assertTrue(response.find("</html>") >= 0)
            self.assertIn('SMS', response)

    def test_login_required_False_response(self):
        """Test the path redirection when user is not logged in using 
        test_client()"""
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = False
            response = a.get(path = '/login', 
                             method = "POST",
                             data = self.dict_user)

            #print str(response)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Password', response.data)

    def test_login_required_False_context(self):
        """Test the path redirection when user is not logged in using 
        context"""
        with app.test_request_context(path = '/login', 
                                      method = "POST",
                                      data = self.dict_user):
            with self.appt.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = False
            response = self.controller.get_login('')
            #print response
            self.assertTrue(response.find("</html>") >= 0)
            self.assertIn('Password', response)
    
if __name__ =='__main__':
    unittest.main(verbosity=2)
