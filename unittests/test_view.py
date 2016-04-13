#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from flask import session
from app import app
from app.controllers.controller import AdminController
from app.views.view import View


class TestView(unittest.TestCase):

    def setUp(self):
        """ Prepare the initial data for tests """
        self.controller = AdminController()
        self.view = View()
        self.view.render_confirm_delete = lambda name: "confirm_delete.html"
        self.appt = app.test_client()
        self.appt.testing = True
        self.appt.debug = True
        self.appt.SECRET_KEY = 'F12Zr47j\3yX R~X@H!jmM]L'
        self.dict_user = {'id': 1,
                          'login': 'user',
                          'password': 'password'}
        with self.appt as a:
            with a.session_transaction() as sess:
                sess['id'] = 1
                sess['username'] = 'user'
                sess['password'] = 'password'
                sess['logged_in'] = True

    def teardown(self):
        """ Delete the preparation data for tests """
        try:
            session.pop('username', None)
        except Exception as error:
            print(error)
        finally:
            session.close()

    def test_render_login(self):
        """ Test if login page is rendered """
        response = self.appt.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password', response.data)

    def test_render_index(self):
        """ Test if home page is rendered """
        response = self.appt.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Головна сторінка | SMS', response.data)

    def test_render_error(self):
        """ Test the 404 page is rendered """
        response = self.appt.get('/page_not_found')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Error 404 | SMS', response.data)

    def test_render_user_form(self, roles='', errors='', user=''):
        """ Test if user add page is rendered """
        response = self.appt.get('/user_add')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Додати користувача', response.data)

    def test_add_user_form_success(self, name=''):
        """ Test the url redirection when user was added successfully """
        response = self.appt.get("/users_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список користувачів  | SMS', response.data)

    def test_render_confirm_delete(self, name=''):
        """ Test if function returns confirm delete page """
        self.assertEqual(self.view.render_confirm_delete('user'),
                         "confirm_delete.html")

    def test_remove_user_form_success(self, name=''):
        """ Test the url redirection when user was deleted successfully """
        response = self.appt.get("/users_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список користувачів  | SMS', response.data)

    def test_render_list_users(self, users=''):
        """ Test users list is rendered """
        response = self.appt.get('/users_list')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список користувачів  | SMS', response.data)

    # ---View for schools----

    def test_render_list_schools(self, schools=''):
        """ Test schools list is rendered """
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список шкіл  | SMS', response.data)

    def test_render_school_form(self, errors='', school=''):
        """ Test if school add page is rendered """
        response = self.appt.get("/school_add")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Додати школу | SMS', response.data)

    def test_add_school_form_success(self, name=''):
        """ Test the url redirection when schools were added successfully """
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список шкіл  | SMS', response.data)

    def test_remove_school_form_success(self, name=''):
        """ Test the url redirection when school was deleted successfully """
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список шкіл  | SMS', response.data)

    # ---View for subjects----

    def test_render_list_subjects(self, subjects=''):
        """ Test if subjects list is rendered """
        response = self.appt.get("/subjects_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список предметів | SMS', response.data)

    def test_render_subject_form(self, errors='', subject=''):
        """ Test if subject add page is rendered """
        response = self.appt.get("/subject_add")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Додати предмет | SMS', response.data)

    def test_add_subject_form_success(self, name=''):
        """ Test the url redirection when subject was added successfully """
        response = self.appt.get("/subjects_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список предметів | SMS', response.data)

    def test_remove_subject_form_success(self, name=''):
        """ Test the url redirection when subject was deleted successfully """
        response = self.appt.get("/subjects_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список предметів | SMS', response.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
