import unittest
from flask import Flask, url_for, redirect, render_template, request, session
from app import app
from app.controllers.controller import AdminController
from app.views.view import View


class TestView(unittest.TestCase):

    def setUp(self):
        self.controller = AdminController()
        self.view = View()
        self.appt = app.test_client()
        self.appt.testing = True
        self.appt.debug = True
        self.appt.SECRET_KEY = 'F12Zr47j\3yX R~X@H!jmM]L'
        
        self.dict_user = {'id' : 1,
        				  'login' : 'username',
                          'password' : 'password'}
        self.controller.view.render_login = lambda error: "login.html"
        self.controller.view.render_index = lambda: "index.html"
        self.controller.view.render_error = lambda: "page_not_found.html"
        
    def test_render_login(self):
        """Test if login page is rendered"""
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
            response = a.get(path = '/login', 
                             method = "POST",
                             data = self.dict_user)

            #print str(response)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Password', response.data)
                
    def test_render_index(self):
        """Test if home page is rendered"""
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
        
    def test_render_error(self):
        """Test the 404 page is rendered"""
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
            response = a.get(path = '/page_not_found', 
                             method = "POST",
                             data = self.dict_user)

            #print str(response)
            self.assertEqual(response.status_code, 404)
            self.assertIn('Error 404 | SMS', response.data)
        
    def test_render_user_form(self, roles = '', errors = '', user = ''):
        """Test if user add page is rendered"""
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
            response = a.get(path = '/user_add', 
                             method = "POST",
                             data = self.dict_user)

            #print str(response)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Додати користувача', response.data)
        
    def test_add_user_form_success(self, name=''):
        """Test the url redirection when user was added successfully"""
        response = self.appt.get("/users_list")
        self.assertEqual(response.status_code, 302)
                
    def test_render_confirm_delete(self, name=''):
        """Test if function returns confirm delete page"""
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
            response = a.get(path = '/confirm_delete', 
                             method = "POST",
                             data = self.dict_user)

            #print str(response)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Видалити | SMS', response.data)
        """response = self.appt.get("/confirm_delete")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Видалити | SMS', response.data)"""

    def test_remove_user_form_success(self, name=''):
        """Test the url redirection when user was deleted successfully"""
        response = self.appt.get("/users_list")
        self.assertEqual(response.status_code, 302)

    def test_render_list_users(self, users=''):
        """Test users list is rendered"""
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'username'
                sess['password'] = 'password'
                sess['logged_in'] = True
            response = a.get(path = '/users_list', 
                             method = "POST",
                             data = self.dict_user)

            #print str(response)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Список користувачів  | SMS', response.data)
        
    #---View for schools----

    def test_render_list_schools(self, schools=''):
        """Test schools list is rendered"""
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список шкіл  | SMS', response.data)

    def test_render_school_form(self, errors='', school=''):
        """Test if school add page is rendered"""
        response = self.appt.get("/school_add")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Додати школу | SMS', response.data)

    def test_add_school_form_success(self, name=''):
        """Test the url redirection when schools were added successfully"""
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, 302)

    def test_remove_school_form_success(self, name=''):
        """Test the url redirection when school was deleted successfully"""
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, 302)
        
    #---View for subjects----

    def test_render_list_subjects(self, subjects=''):
        """Test if subjects list is rendered"""
        response = self.appt.get("/subject_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список предметів | SMS', response.data)
        
    def test_render_subject_form(self, errors='', subject=''):
        """test if subject add page is rendered"""
        response = self.appt.get("/subject_add")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Додати предмет | SMS', response.data)
        
    def test_add_subject_form_success(self, name=''):
        """Test the url redirection when subject was added successfully"""
        response = self.appt.get("/subjects_list")
        self.assertEqual(response.status_code, 302)
        
    def test_remove_subject_form_success(self, name=''):
        """Test the url redirection when subject was deleted successfully"""
        response = self.appt.get("/subjects_list")
        self.assertEqual(response.status_code, 302)


if __name__ =='__main__':
    unittest.main(verbosity=2)
