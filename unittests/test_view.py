import unittest
from flask import Flask, url_for, redirect, render_template, request
from app import app
from app.views.view import View
from app.controllers.controller import AdminController


class TestView(unittest.TestCase):

    def setUp(self):
        self.controller = AdminController()
        self.view = View()
        self.appt = app.test_client()
        self.appt.testing = True
        self.appt.debug = True
        
        self.dict_user = {'login': 'username',
                          'password': 'password'}
        
        name = ''
        roles = ''
        errors = ''
        user = ''
        school = ''
        subject = ''
        schools = ''
        subjects = ''
        
       
    def test_render_login(self):
        """Test if login page is rendered"""
        response = self.appt.get(path = '/login', 
                                 method = "POST",
                                 data = self.dict_user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Авторизація | SMS', response.data)
        
    def test_render_index(self):
        """Test if home page is rendered"""
        response = self.appt.get(path = '/index', 
                                 method = "POST",
                                 data = self.dict_user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Головна сторінка | SMS', response.data)

    def test_render_error(self):
        """Test the 404 page is rendered"""
        response = self.appt.get("/page_not_found")
        self.assertEqual(response.status_code, 404)   
        self.assertIn('Error 404 | SMS', response.data)

    def test_render_user_form(self, roles = '', errors = '', user = ''):
        """Test if user add page is rendered"""
        response = self.appt.get("/user_add")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Додати користувача', response.data)

    def test_add_user_form_success(self, name=''):
        """Test the url redirection when user was added successfully"""
        response = self.appt.get("/users_list")
        self.assertEqual(response.status_code, 302)
        #self.assertIn('Список користувачів', response.data)
        #self.assertEqual(urlparse(response.location).path, "/users_list")

    def test_render_confirm_delete(self, name=''):
        """Test if function returns confirm delete page"""
        response = self.appt.get("/confirm_delete")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Видалити | SMS', response.data)

    def test_remove_user_form_success(self, name=''):
        """Test the url redirection when user was deleted successfully"""
        response = self.appt.get("/users_list")
        self.assertEqual(response.status_code, 302)

    def test_render_list_users(self, users=''):
        """Test users list is rendered"""
        response = self.appt.get("/users_list")
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
