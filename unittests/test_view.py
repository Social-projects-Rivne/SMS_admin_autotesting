import unittest
from flask import Flask, url_for, redirect, render_template
from app import app
from app.views.view import View


class TestView(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app.debug = True
        self.view = View()
        name = ''
        roles = ''
        errors = ''
        user = ''
        school = ''
        subject = ''
        schools = ''
        subjects = ''
        #SERVER_NAME = 'http://localhost:5000/'

    def tearDown(self):
        pass
    
    def test_render_login(self):
        """Test if login page is rendered"""
        response = self.app.get("login")
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.location, url_for('login', _external=True))
            
    def test_render_index(self):
        """Test if home page is rendered"""
        response = self.app.get("index")
        self.assertEqual(response.status_code, 200)
	
    def test_render_error(self):
        """Test the 404 page is rendered"""
        response = self.app.get("page_not_found")
        self.assertEqual(response.status_code, 404)
	
	def test_render_user_form(self, roles, errors, user):
		"""Test if user add page is rendered"""
        response = self.app.get("user_add")
        self.assertEqual(response.status_code, 200)
	
	def test_add_user_form_success(self, name=''):
		"""Test the url redirection when user was added successfully"""
        response = self.app.get("users_list")
        self.assertEqual(response.status_code, 302)
        
    def test_render_confirm_delete(self, name=''):
        """Test if function returns confirm delete page"""
        response = self.app.get("confirm_delete")
        self.assertEqual(response.status_code, 200)
        
    def test_remove_user_form_success(self, name=''):
        """Test the url redirection when user was deleted successfully"""
        response = self.app.get("users_list")
        self.assertEqual(response.status_code, 302)
        
    def test_render_list_users(self, users=''):
        """Test users list is rendered"""
        response = self.app.get("users_list")
        self.assertEqual(response.status_code, 302)
        
    #---View for schools----

    def test_render_list_schools(self, schools=''):
        """Test schools list is rendered"""
        response = self.app.get("schools_list")
        self.assertEqual(response.status_code, 200)
        
    def test_render_school_form(self, errors='', school=''):
        """Test if school add page is rendered"""
        response = self.app.get("school_add")
        self.assertEqual(response.status_code, 200)
        
    def test_add_school_form_success(self, name=''):
        """Test the url redirection when schools were added successfully"""
        response = self.app.get("schools_list")
        self.assertEqual(response.status_code, 302)
        
    def test_remove_school_form_success(self, name=''):
        """Test the url redirection when school was deleted successfully"""
        response = self.app.get("schools_list")
        self.assertEqual(response.status_code, 302)
        
    #---View for subjects----

    def test_render_list_subjects(self, subjects=''):
        """Test if subjects list is rendered"""
        response = self.app.get("subject_list")
        self.assertEqual(response.status_code, 200)
        
    def test_render_subject_form(self, errors='', subject=''):
        """test if subject add page is rendered"""
        response = self.app.get("subject_add")
        self.assertEqual(response.status_code, 200)
        
    def test_add_subject_form_success(self, name=''):
        """Test the url redirection when subject was added successfully"""
        response = self.app.get("subjects_list")
        self.assertEqual(response.status_code, 302)
        
    def test_remove_subject_form_success(self, name=''):
        """Test the url redirection when subject was deleted successfully"""
        response = self.app.get("subjects_list")
        self.assertEqual(response.status_code, 302)
        
        			
if __name__ =='__main__':
    unittest.main(verbosity=2)
