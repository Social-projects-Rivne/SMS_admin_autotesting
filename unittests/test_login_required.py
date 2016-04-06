import unittest
import app.controllers.controller
import app.urls
from functools import wraps
from app import app
from flask import session, url_for, request, redirect


class TestLoginRequired(unittest.TestCase):
	
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True
		self.app.debug = True
        
	def tearDown(self):
		pass
		
	def test_login_required_True(rout):
		#if not session.get('logged_in'):
		if session['logged_in'] == True:
			assertIsNotNone(rout)
	
	def test_login_required_False(rout):
		if session['logged_in'] == False:
			response = self.app.get("login")
			self.assertEqual(response.status_code, 302)
		
if __name__ =='__main__':
    unittest.main(verbosity=2)
