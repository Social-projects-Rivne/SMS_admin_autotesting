#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for view.py file from SMS_admin_autotesting application
"""

import unittest

from mock import Mock, patch

from flask import session

from app import app
from app.controllers.controller import AdminController
from app.views.view import View


class TestView(unittest.TestCase):

    """
    Class for testing functions from View Class
    """

    def setUp(self):
        """
        Prepare the initial data for tests
        """
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
        self.roles = " "
        self.user = " "
        self.errors = " "
        with self.appt.session_transaction() as sess:
            sess['id'] = 1
            sess['username'] = 'user'
            sess['password'] = 'password'
            sess['logged_in'] = True

    def teardown(self):
        """
        Delete the preparation data for tests
        """
        try:
            session.pop('username', None)
        except Exception as error:
            print(error)
        finally:
            session.close()

    @patch('app.views.view.View')
    def test_render_login(self, mock_view):
        """
        Test if login page is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Password'
        mock_view.render_login.return_value = mock_response
        response = self.appt.get('/login')
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_render_index(self, mock_view):
        """
        Test if home page is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Головна сторінка | SMS'
        mock_view.render_index.return_value = mock_response
        response = self.appt.get('/index')
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_render_error(self, mock_view):
        """
        Test the 404 page is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = 'Error 404 | SMS'
        mock_view.render_error.return_value = mock_response
        response = self.appt.get('/page_not_found')
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_render_user_form(self, mock_view):
        """
        Test if user add page is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Додати користувача'
        mock_view.render_user_form.return_value = mock_response
        response = self.appt.get('/user_add')
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_add_user_form_success(self, mock_view):
        """
        Test the url redirection when user was added successfully
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список користувачів  | SMS'
        mock_view.add_user_form_success.return_value = mock_response
        response = self.appt.get("/users_list")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_render_confirm_delete(self, mock_view):
        """
        Test if function returns confirm delete page
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_view.render_confirm_delete.return_value = mock_response
        response = self.appt.get("/confirm_delete")
        self.assertEqual(self.view.render_confirm_delete('user'),
                         "confirm_delete.html")

    @patch('app.views.view.View')
    def test_remove_user_form_success(self, mock_view):
        """
        Test the url redirection when user was deleted successfully
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список користувачів  | SMS'
        mock_view.remove_user_form_success.return_value = mock_response
        response = self.appt.get("/users_list")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_render_list_users(self, mock_view):
        """
        Test users list is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список користувачів  | SMS'
        mock_view.render_list_users.return_value = mock_response
        response = self.appt.get('/users_list')
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    # ---View for schools----

    @patch('app.views.view.View')
    def test_render_list_schools(self, mock_view):
        """
        Test schools list is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список шкіл  | SMS'
        mock_view.render_list_schools.return_value = mock_response
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_render_school_form(self, mock_view):
        """
        Test if school add page is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Додати школу | SMS'
        mock_view.render_school_form.return_value = mock_response
        response = self.appt.get("/school_add")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_add_school_form_success(self, mock_view):
        """
        Test the url redirection when schools were added successfully
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список шкіл  | SMS'
        mock_view.add_school_form_success.return_value = mock_response
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_remove_school_form_success(self, mock_view):
        """
        Test the url redirection when school was deleted successfully
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список шкіл  | SMS'
        mock_view.remove_school_form_success.return_value = mock_response
        response = self.appt.get("/schools_list")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    # ---View for subjects----

    @patch('app.views.view.View')
    def test_render_list_subjects(self, mock_view):
        """
        Test if subjects list is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список предметів | SMS'
        mock_view.render_list_subjects.return_value = mock_response
        response = self.appt.get("/subjects_list")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_render_subject_form(self, mock_view):
        """
        Test if subject add page is rendered
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Додати предмет | SMS'
        mock_view.render_subject_form.return_value = mock_response
        response = self.appt.get("/subject_add")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_add_subject_form_success(self, mock_view):
        """
        Test the url redirection when subject was added successfully
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список предметів | SMS'
        mock_view.add_subject_form_success.return_value = mock_response
        response = self.appt.get("/subjects_list")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)

    @patch('app.views.view.View')
    def test_remove_subject_form_success(self, mock_view):
        """
        Test the url redirection when subject was deleted successfully
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Список предметів | SMS'
        mock_view.remove_subject_form_success.return_value = mock_response
        response = self.appt.get("/subjects_list")
        self.assertEqual(response.status_code, mock_response.status_code)
        self.assertIn(mock_response.text, response.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
