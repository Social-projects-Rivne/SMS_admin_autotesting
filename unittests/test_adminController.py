# -*- coding: utf-8 -*-
import os
import unittest
import sys
import urllib2

from flask import Flask

from app import app, DBDriver
from app.models.subjects_model_with_entity import ExtendedSubjectsModel
import config as config
from app.controllers.controller import AdminController
from db import credentials

__author__ = 'boris'


class TestAdminController(unittest.TestCase):
    def setUp(self):
        """ Fixture that creates a initial data and records for tests """

        self.admin = AdminController()
        self.admin.view.render_login = lambda error: "login.html"
        self.admin.view.render_index = lambda: "index.html"
        self.admin.view.render_error = lambda: "page_not_found.html"
        self.admin.view.render_list_users = lambda users: "users_list.html"

        self.app_t_client = app.test_client()
        self.arg_dict_subj = {'name': 'ПрЕдМеТдЛяТеСтУвАнНя'}

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.db = credentials[3]

        self.orm = DBDriver()
        self.orm.connect(self.host, self.username, self.password, self.db)

    def tearDown(self):
        """ Fixture that deletes all preparation for tests """
        try:
            self.orm.delete('Subjects',
                            'name = "%s"' % (self.arg_dict_subj['name']))
            self.orm.delete('Subjects', 'name = "%s%s"' % (
                self.arg_dict_subj['name'], "ЗмІнЕнИй"))
            # pass
        except:
            pass
        finally:
            self.orm.close()

    def test_get_index(self):
        """Test method return page get_index()"""
        self.assertEqual(self.admin.get_index(), "index.html")

    def test_get_login(self):
        """Test method return page get_login()"""
        self.assertEqual(self.admin.get_login('404'), "login.html")

    def test_get_error404(self):
        """Test method return page get_error404()"""
        self.assertEqual(self.admin.get_error404(),
                         "page_not_found.html")

    def test_object_type(self):
        """Check type of object"""
        self.assertTrue(isinstance(AdminController(), AdminController))

    def test_object_not_none(self):
        """Check, whether AdminController() is not empty"""
        self.assertIsNotNone(AdminController())

    def test_list_all_users_has_content(self):
        """Check, whether list of all users is not empty"""
        self.assertTrue(len(self.admin.list_all_users()) > 0)

    # ---------------------------------------------
    # Testing subject CRUD
    # ---------------------------------------------
    def test_list_all_subjects_get_response(self):
        """ Test method list_all_subjects, method "GET", check status-code """
        response = self.app_t_client.get(path='/subject_list',
                                         method="GET",
                                         data=self.arg_dict_subj)
        self.assertTrue(response.status_code == 302)

    def test_list_all_subjects_post_response(self):
        """ Test method list_all_subjects, method "POST", check status-code """
        response = self.app_t_client.get(path='/subject_list',
                                         method="POST",
                                         data=self.arg_dict_subj)
        self.assertTrue(response.status_code == 302)

    def test_list_all_subjects_get_content(self):
        """ Test method list_all_subjects, method "GET",
                check whether content is HTML """
        with app.test_request_context(path='/subject_list',
                                      method="GET",
                                      data=self.arg_dict_subj):
            response = self.admin.add_subject()
            self.assertTrue(response.__repr__().find("</html>") >= 0)

    def test_list_all_subjects_post_content(self):
        """ Test method list_all_subjects, method "POST", check status-code """
        with app.test_request_context(path='/subject_list',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.add_subject()
            self.assertTrue(response.status_code == 302)

    def test_add_subject_get_response(self):
        """ Test method add_subject, method "GET", check status-code """
        response = self.app_t_client.get(path='/subject_add',
                                         method="GET",
                                         data=self.arg_dict_subj)
        self.assertTrue(response.status_code == 302)

    def test_add_subject_post_response(self):
        """ Test method add_subject, method "POST", check status-code """
        response = self.app_t_client.get(path='/subject_add',
                                         method="POST",
                                         data=self.arg_dict_subj)
        self.assertTrue(response.status_code == 302)

    def test_add_subject_get_content(self):
        """ Test method add_subject, method "GET",
                check whether content is HTML """
        with app.test_request_context(path='/subject_add',
                                      method="GET",
                                      data=self.arg_dict_subj):
            response = self.admin.add_subject()
            self.assertTrue(response.__repr__().find("</html>") >= 0)

    def test_add_subject_post_content(self):
        """ Test method add_subject, method "POST", check status-code """
        with app.test_request_context(path='/subject_add',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.add_subject()
            self.assertTrue(response.status_code == 302)

    def test_add_subject_db_results(self):
        """ Test method add_subject, method "POST",
                check changes in DB - whether object is created """
        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "%s"' % self.arg_dict_subj['name'])
        with app.test_request_context(path='/subject_add',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.add_subject()
            results_after = self.orm.mysql_do(
                ExtendedSubjectsModel.select_subjects_query +
                ' where name = "%s"' % self.arg_dict_subj['name'])
            self.assertTrue(len(results_before) == len(results_after) - 1)

    def test_update_subject_response(self):
        """ Test method update_subject, method "POST", check status-code """
        self.orm.insert('Subjects', ('name',),
                        (self.arg_dict_subj['name'],))

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "%s"' % self.arg_dict_subj['name'])
        test_subject_id = results_before[0]['id']
        with app.test_request_context(path='/subject_update',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.update_subject(test_subject_id)
            self.assertTrue(response.status_code == 302)

    def test_update_subject_db_result(self):
        """ Test method update_subject, method "POST",
                check changes in DB - whether object is updated"""
        self.orm.insert('Subjects', ('name',),
                        (self.arg_dict_subj['name'],))

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "%s"' % self.arg_dict_subj['name'])
        test_subject_id = results_before[0]['id']

        with app.test_request_context(path='/subject_update',
                                      method="POST",
                                      data={'name': self.arg_dict_subj[
                                          'name'] + "ЗмІнЕнИй"}):
            response = self.admin.update_subject(test_subject_id)
            results_after = self.orm.mysql_do(
                ExtendedSubjectsModel.select_subjects_query +
                ' where name = "%s%s"' % (
                    self.arg_dict_subj['name'], "ЗмІнЕнИй"))
            self.assertTrue(len(results_before) == len(results_after))

    def test_remove_subject_response(self):
        """ Test method remove_subject, method "POST", check status code"""
        self.orm.insert('Subjects', ('name',),
                        (self.arg_dict_subj['name'],))

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "%s"' % self.arg_dict_subj['name'])
        test_subject_id = results_before[0]['id']
        with app.test_request_context(path='/subject_remove',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.remove_subject(test_subject_id)
            self.assertTrue(response.status_code == 302)

    def test_remove_subject_db_results(self):
        """ Test method remove_subject, method "POST",
                check changes in DB - whether object is removed """
        self.orm.insert('Subjects', ('name',),
                        (self.arg_dict_subj['name'],))

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "%s"' % self.arg_dict_subj['name'])
        test_subject_id = results_before[0]['id']
        with app.test_request_context(path='/subject_remove',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.remove_subject(test_subject_id)
            results_after = self.orm.mysql_do(
                ExtendedSubjectsModel.select_subjects_query +
                ' where name = "%s"' % self.arg_dict_subj['name'])
            self.assertTrue(len(results_before) == len(results_after) + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
