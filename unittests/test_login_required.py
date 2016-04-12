import unittest
from flask import session, url_for, request, redirect, Flask
from functools import wraps

from app.controllers.controller import AdminController
import app.urls
from app.utils.login_required import login_required
from app import app




class TestLoginRequired(unittest.TestCase):
    
    def setUp(self):
        self.controller = AdminController()
        #self.app.config['SECRET_KEY'] = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
        self.appt = app.test_client()
        self.appt.testing = True
        self.appt.debug = True
        
        self.dict_user = {'username': 'username',
                          'login': 'username',
                          'password': 'password'}
        #app_f = flask.Flask(__name__)
        #app_f.config.update(dict(SECRET_KEY = 'test key',
                             #  DEBUG = True))

    """ def test_login_required_True(self, rout):
        
        if session.get(app.urls.login().logged_in):
            assertIsNotNone(rout)"""

    def test_login_required_True_response(self):
        #rout = controller.get_login()
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
                #logg = sess.get('logged_in')
            response = a.get(path = '/login', 
                                 method = "POST",
                                 data = self.dict_user)

            print str(response)
            #self.assertEqual('Invalid username or password', response.data)
        #self.assertIsNotNone(rout)

    def test_login_required_True_context(self):
        #rout = self.controller.get_login()
        error_log = 'empty'
        with app.test_request_context(path = '/login', 
                                      method = "POST",
                                      data = self.dict_user):
            with self.appt.session_transaction() as sess:
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
                #logg = sess.get('logged_in')
            response = self.controller.get_login(error_log)
            #print response
            print error_log
            #logged = session.get('logged_in')
            #print str(logged)
            #self.assertTrue(logged)
            #self.assertIsNotNone(rout)
    
    """def test_login_required_False(self, rout, dict_user):
        if not session.get('logged_in'):
            response = self.app.get("login")
            self.assertEqual(response.status_code, 302)"""
        
if __name__ =='__main__':
    unittest.main(verbosity=2)
