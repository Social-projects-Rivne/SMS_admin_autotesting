""" A couple of tests for testing module controller """
# -*- coding: utf-8 -*-
import unittest

from app import app, DBDriver
from app.models.schools_model_with_entity import ExtendedSchoolsModel
from app.models.subjects_model_with_entity import ExtendedSubjectsModel
from app.models.teachers_model_with_entity import ExtendedTeachersModel
from app.controllers.controller import AdminController
from db import credentials


class TestAdminController(unittest.TestCase):
    """ Class with methods, for testing AdminController class """

    def setUp(self):
        """ Fixture that creates a initial data and records for tests """

        self.admin = AdminController()
        self.admin.view.render_login = lambda error: "login.html"
        self.admin.view.render_index = lambda: "index.html"
        self.admin.view.render_error = lambda: "page_not_found.html"

        self.app_t_client = app.test_client()
        self.arg_dict_subj = {'name': 'ПрЕдМеТдЛяТеСтУвАнНя'}
        self.arg_dict_subj_negative = {'name': 'TestingSubject'}
        self.arg_dict_school = {'name': 'ШкОлАдЛяТеСтУвАнНя',
                                'address': 'АдРеСаШкОлИ'}
        self.arg_dict_school_negative = {'name': 'TestSchoolName',
                                         'address': 'TestSchoolAddr'}
        self.arg_dict_users = {'name': 'Тест Тестович',
                               'login': 'testlogin',
                               'password': 'TestPassword',
                               'email': 'testmail@domain.com',
                               'role_id': 1,
                               'user_role': 1,
                               'delete_button': True}
        self.arg_dict_users_negative = {'name': 'Тест Тестович',
                                        'login': 'Логін',
                                        'password': 'TestPassword',
                                        'email': 'chdomain.com',
                                        'role_id': 1,
                                        'user_role': 1,
                                        'delete_button': True}

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.db = credentials[3]

        self.orm = DBDriver()
        self.orm.connect(self.host, self.username, self.password, self.db)
        self.orm.insert('Schools', ('name', 'address'),
                        (self.arg_dict_school['name'],
                         self.arg_dict_school['address']))
        self.orm.insert('Subjects', ('name',),
                        (self.arg_dict_subj['name'],))
        self.orm.mysql_do("INSERT INTO `Teachers`(`name`, `role_id`, \
                          `login`, `email`, `password`) \
                          VALUES ('{0}', {1},'{2}', '{3}','{4}')".format(
                              self.arg_dict_users['name'],
                              self.arg_dict_users['role_id'],
                              self.arg_dict_users['login'],
                              self.arg_dict_users['email'],
                              self.arg_dict_users['password']
        ))

    def tearDown(self):
        """ Fixture that deletes all preparation for tests """
        try:
            self.orm.delete('Subjects',
                            'name = "{}"'.format(self.arg_dict_subj['name']))
            self.orm.delete('Subjects', 'name = "{}{}"'.format(
                self.arg_dict_subj['name'], "ЗмІнЕнИй"))

            self.orm.delete('Schools',
                            'name = "{}"'.format(self.arg_dict_school['name']))
            self.orm.delete('Schools', 'name = "{}{}"'.format(
                self.arg_dict_school['name'], "ЗмІнЕнИй"))

            self.orm.delete('Teachers',
                            'name = "{}"'.format(self.arg_dict_users['name']))
            # pass
        except Exception as error:
            print(error)
        finally:
            self.orm.close()

    def test_get_index(self):
        """ Test method return page get_index() """
        self.assertEqual(self.admin.get_index(), "index.html")

    def test_get_login(self):
        """ Test method return page get_login() """
        self.assertEqual(self.admin.get_login('404'), "login.html")

    def test_get_error404(self):
        """ Test method return page get_error404() """
        self.assertEqual(self.admin.get_error404(),
                         "page_not_found.html")

    # ---------------------------------------------
    # Testing teacher CRUD
    # ---------------------------------------------

    def test_list_all_users_get_content(self):
        """ Test method list_all_users, method "GET",
        check whether content is HTML """
        with app.test_request_context(path='/users_list',
                                      method="GET",
                                      data=self.arg_dict_users):
            response = repr(self.admin.list_all_users())
            self.assertIn(u'SMS</title>', response)

    def test_add_user_get_content(self):
        """ Test method add_user, method "GET",
        check whether content is HTML """

        with app.test_request_context(path='/user_add',
                                      method="GET",
                                      data=self.arg_dict_users):
            response = repr(self.admin.add_user())
            self.assertIn(u'SMS</title>', response)

    def test_add_user_results(self):
        """ Test method add_user, method "POST",
        check changes in DB - whether object is created """

        results_before = self.orm.mysql_do('SELECT * FROM `Teachers`')
        with app.test_request_context(path='/user_add',
                                      method="POST",
                                      data=self.arg_dict_users):
            response = self.admin.add_user()
            results_after = self.orm.mysql_do("SELECT * FROM `Teachers`")

            self.assertNotEqual(results_after,
                                results_before)  # BUG! Nothing changed!
            self.assertEqual(results_after[0]['login'],
                             self.arg_dict_users['login'])

    def test_add_user_content(self):
        """ Test method add_user, method "POST",
        check whether content is HTML """

        results_before = self.orm.mysql_do('SELECT * FROM `Teachers`')
        with app.test_request_context(path='/user_add',
                                      method="POST",
                                      data=self.arg_dict_users):
            response = self.admin.add_user()
            results_after = self.orm.mysql_do("SELECT * FROM `Teachers`")
            self.assertIn(u'<a href="/users_list">', response.data)

    def test_update_user_response_status(self):
        """ Test method update_user, method "POST",
        chec k whether content is HTML """

        results_before = self.orm.mysql_do('SELECT * FROM `Teachers`')
        test_id = results_before[0]['id']
        dict_user_update = {
            'name': self.arg_dict_users['name'] + "Апдейт",
            'login': self.arg_dict_users['login'] + "change",
            'password': self.arg_dict_users['password'] + "change",
            'email': self.arg_dict_users['email'] + "a@mail.com",
            'user_role': 2}
        with app.test_request_context(path='/user_update',
                                      method="POST",
                                      data=dict_user_update):
            response = self.admin.update_user(test_id)
            results_after = self.orm.mysql_do("SELECT * FROM `Teachers`")
            self.assertIn(u'SMS</title>', response)

    def test_update_user_response(self):
        """ Test method update_user, method "POST",
        whether user is updated """
        results_before = self.orm.mysql_do('SELECT * FROM `Teachers`')
        test_id = results_before[0]['id']
        dict_user_update = {
            'name': self.arg_dict_users['name'] + "Апдейт",
            'login': self.arg_dict_users['login'] + "change",
            'password': self.arg_dict_users['password'] + "change",
            'email': self.arg_dict_users['email'] + "a@mail.com",
            'user_role': 2}
        with app.test_request_context(path='/user_update',
                                      method="POST",
                                      data=dict_user_update):
            response = self.admin.update_user(test_id)
            results_after = self.orm.mysql_do("SELECT * FROM `Teachers`")
            self.assertEqual(results_before, results_after)

    def test_remove_user_status(self):
        """ Test method remove_user, method "POST", check status code"""

        results_before = self.orm.mysql_do('SELECT * FROM `Teachers`')
        test_id = results_before[0]['id']
        with app.test_request_context(path='/user_remove',
                                      method="POST",
                                      data=self.arg_dict_users):
            response = self.admin.remove_user(test_id)
            results_after = self.orm.mysql_do('SELECT * FROM `Teachers`')
            self.assertTrue(response.status_code == 302)

    def test_remove_user_response(self):
        """ Test method remove_user, method "POST",
        check changes in DB - whether object is removed """

        results_before = self.orm.mysql_do('SELECT * FROM `Teachers`')
        test_id = results_before[0]['id']
        with app.test_request_context(path='/user_remove',
                                      method="POST",
                                      data=self.arg_dict_users):
            response = self.admin.remove_user(test_id)
            results_after = self.orm.mysql_do('SELECT * FROM `Teachers`')
            self.assertNotEqual(results_before, results_after)
            self.assertTrue(results_after < results_before)

    def test_update_user_response_negative_login(self):
        """ Test method update_user, method "POST", wrong login """

        results_before = self.orm.mysql_do('SELECT * FROM `Teachers`')
        test_id = results_before[0]['id']
        with app.test_request_context(path='/user_update',
                                      method="POST",
                                      data=self.arg_dict_users_negative):
            response = self.admin.update_user(test_id)
            self.assertIn('Некоректно введно логін'.decode('utf-8'),
                          response)

    def test_update_user_response_negative_email(self):
        """ Test method update_user, method "POST", wrong email """

        results_before = self.orm.mysql_do('SELECT * FROM `Teachers`')
        test_id = results_before[0]['id']
        with app.test_request_context(path='/user_update',
                                      method="POST",
                                      data=self.arg_dict_users_negative):
            response = self.admin.update_user(test_id)
            self.assertIn('Некоректно введно емейл'.decode('utf-8'),
                          response)
    # --------------------------------------------------
    # Testing school CRUD
    # ---------------------------------------------------

    def test_list_all_schools_get_content(self):
        """ Test method list_all_schools, method "GET",
        check whether content has a value, inserted in SetUp """

        with app.test_request_context(path='/schools_list',
                                      method="GET",
                                      data=self.arg_dict_school):
            response = self.admin.list_all_schools()
            self.assertIn(self.arg_dict_school['name'].decode('utf-8'),
                          response)

    def test_list_all_schools_post_content(self):
        """ Test method list_all_schools, method "POST",
        check whether content has a value, inserted in SetUp """

        with app.test_request_context(path='/schools_list',
                                      method="POST",
                                      data=self.arg_dict_school):
            response = self.admin.list_all_schools()
            self.assertIn(self.arg_dict_school['name'].decode('utf-8'),
                          response)

    def test_add_school_content(self):
        """ Test method add_school, method "GET",
        check whether content has a value, inserted in SetUp """

        with app.test_request_context(path='/school_add',
                                      method="GET",
                                      data=self.arg_dict_school):
            response = self.admin.add_school()
            self.assertIn(self.arg_dict_school['name'].decode('utf-8'),
                          response)

    def test_add_school_response(self):
        """ Test method add_school, method "POST", check status-code """

        with app.test_request_context(path='/school_add',
                                      method="POST",
                                      data=self.arg_dict_school):
            response = self.admin.add_school()
            self.assertTrue(response.status_code == 302)

    def test_add_school_content_wrong_name(self):
        """ Test method add_school, method "POST", wrong school name
        check whether response has a warning """

        with app.test_request_context(path='/school_add',
                                      method="POST",
                                      data=self.arg_dict_school_negative):
            response = self.admin.add_school()
            self.assertIn('Некоректно введено назву'.decode('utf-8'),
                          response)

    def test_add_school_content_wrong_address(self):
        """ Test method add_school, method "POST", wrong school address
        check whether response has a warning """

        with app.test_request_context(path='/school_add',
                                      method="POST",
                                      data=self.arg_dict_school_negative):
            response = self.admin.add_school()
            self.assertIn('Некоректно введено адресу'.decode('utf-8'),
                          response)

    def test_add_school_db_results(self):
        """ Test method add_school, method "POST",
        check changes in DB - whether object is created """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        with app.test_request_context(path='/school_add',
                                      method="POST",
                                      data=self.arg_dict_school):
            response = self.admin.add_school()
            results_after = self.orm.mysql_do(
                ExtendedSchoolsModel.select_schools_query +
                ' where name = "{}"'.format(self.arg_dict_school['name']))
            self.assertTrue(len(results_before) == len(results_after) - 1)

    def test_update_school_response(self):
        """ Test method update_school, method "POST", check status-code """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/school_update',
                                      method="POST",
                                      data=self.arg_dict_school):
            response = self.admin.update_school(test_id)
            self.assertTrue(response.status_code == 302)

    def test_update_school_content(self):
        """ Test method update_school, method "GET",
        check whether response is HTML """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/school_update',
                                      method="GET",
                                      data=self.arg_dict_school):
            response = self.admin.update_school(test_id)
            self.assertTrue(response.find("</html>") >= 0)

    def test_update_school_content_wrong_name(self):
        """ Test method update_school, method "GET",
        check whether response has warning """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/school_update',
                                      method="POST",
                                      data=self.arg_dict_school_negative):
            response = self.admin.update_school(test_id)
            self.assertIn('Некоректно введено назву'.decode('utf-8'),
                          response)

    def test_update_school_content_wrong_address(self):
        """ Test method update_school, method "GET",
        check whether response has warning """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/school_update',
                                      method="POST",
                                      data=self.arg_dict_school_negative):
            response = self.admin.update_school(test_id)
            self.assertIn('Некоректно введено адресу'.decode('utf-8'),
                          response)

    def test_update_school_db_result(self):
        """ Test method update_school, method "POST",
        check changes in DB - whether object is updated """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        test_id = results_before[0]['id']
        dict_school_changed = {
            'name': self.arg_dict_school['name'] + "ЗмІнЕнИй",
            'address': self.arg_dict_school['address'] + "ЗмІнЕнИй"}
        with app.test_request_context(path='/school_update',
                                      method="POST",
                                      data=dict_school_changed):
            response = self.admin.update_school(test_id)
            results_after = self.orm.mysql_do(
                ExtendedSchoolsModel.select_schools_query +
                ' where name = "{}"'.format(dict_school_changed['name']))
            self.assertTrue(len(results_before) == len(results_after))

    def test_remove_school_response(self):
        """ Test method remove_school, method "POST", check status code """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/school_remove',
                                      method="POST",
                                      data=self.arg_dict_school):
            response = self.admin.remove_school(test_id)
            self.assertTrue(response.status_code == 302)

    def test_remove_school_response_negative(self):
        """ Test method remove_school, method "POST", negative test,
        trying to delete non-existent school """

        with app.test_request_context(path='/school_remove',
                                      method="GET",
                                      data=self.arg_dict_school):
            try:
                response = self.admin.remove_school(777777777777777)
            except Exception as error:
                print(error)
                self.assertTrue(False)

    def test_remove_school_content(self):
        """ Test method remove_school, method "POST", check status code """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/school_remove',
                                      method="GET",
                                      data=self.arg_dict_school):
            response = self.admin.remove_school(test_id)
            self.assertTrue(response.find("</html>") >= 0)

    def test_remove_school_db_results(self):
        """ Test method remove_school, method "POST",
        check changes in DB - whether object is removed """

        results_before = self.orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query +
            ' where name = "{}"'.format(self.arg_dict_school['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/school_remove',
                                      method="POST",
                                      data=self.arg_dict_school):
            response = self.admin.remove_school(test_id)
            results_after = self.orm.mysql_do(
                ExtendedSchoolsModel.select_schools_query +
                ' where name = "{}"'.format(self.arg_dict_school['name']))
            self.assertTrue(len(results_before) == len(results_after) + 1)

    # ---------------------------------------------
    # Testing subject CRUD
    # ---------------------------------------------

    def _test_list_all_subjects_get_response(self):
        """ Test method list_all_subjects, method "GET", check status-code """

        response = self.app_t_client.get(path='/subject_list',
                                         method="GET",
                                         data=self.arg_dict_subj)
        self.assertTrue(response.status_code == 302)

    def _test_list_all_subjects_post_response(self):
        """ Test method list_all_subjects, method "POST", check status-code """

        response = self.app_t_client.get(path='/subject_list',
                                         method="POST",
                                         data=self.arg_dict_subj)
        self.assertTrue(response.status_code == 302)

    def test_list_all_subjects_response(self):
        """ Test method list_all_subjects, method "POST",
        check whether content has a value, inserted in SetUp """

        with app.test_request_context(path='/subject_list',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.list_all_subjects()
            self.assertIn(self.arg_dict_subj['name'].decode('utf-8'),
                          response)

    def test_list_all_subjects_content(self):
        """ Test method list_all_subjects, method "GET",
        check whether content has a value, inserted in SetUp """

        with app.test_request_context(path='/subject_list',
                                      method="GET",
                                      data=self.arg_dict_subj):
            response = self.admin.list_all_subjects()
            self.assertIn(self.arg_dict_subj['name'].decode('utf-8'),
                          response)

    def _test_add_subject_get_response(self):
        """ Test method add_subject, method "GET", check status-code """

        response = self.app_t_client.get(path='/subject_add',
                                         method="GET",
                                         data=self.arg_dict_subj)
        self.assertTrue(response.status_code == 302)

    def _test_add_subject_post_response(self):
        """ Test method add_subject, method "POST", check status-code """

        response = self.app_t_client.get(path='/subject_add',
                                         method="POST",
                                         data=self.arg_dict_subj)
        self.assertTrue(response.status_code == 302)

    def test_add_subject_response(self):
        """ Test method add_subject, method "POST", check status-code """

        with app.test_request_context(path='/subject_add',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.add_subject()
            self.assertTrue(response.status_code == 302)

    def test_add_subject_content(self):
        """ Test method add_subject, method "GET",
         whether content has a value, inserted in SetUp """

        with app.test_request_context(path='/subject_add',
                                      method="GET",
                                      data=self.arg_dict_subj):
            response = self.admin.add_subject()
            self.assertIn(self.arg_dict_subj['name'].decode('utf-8'),
                          response)

    def test_add_subject_content_wrong_subject(self):
        """ Test method add_subject, method "POST", check whether
        returned content has warning """

        with app.test_request_context(path='/subject_add',
                                      method="POST",
                                      data=self.arg_dict_subj_negative):
            response = self.admin.add_subject()
            self.assertIn('Некоректно введено назву'.decode('utf-8'),
                          response)

    def test_add_subject_db_results(self):
        """ Test method add_subject, method "POST",
        check changes in DB - whether object is created """

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "{}"'.format(self.arg_dict_subj['name']))
        with app.test_request_context(path='/subject_add',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.add_subject()
            results_after = self.orm.mysql_do(
                ExtendedSubjectsModel.select_subjects_query +
                ' where name = "{}"'.format(self.arg_dict_subj['name']))
            self.assertTrue(len(results_before) == len(results_after) - 1)

    def test_update_subject_response(self):
        """ Test method update_subject, method "POST", check status-code """

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "{}"'.format(self.arg_dict_subj['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/subject_update',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.update_subject(test_id)
            self.assertTrue(response.status_code == 302)

    def test_update_subject_content_wrong_data(self):
        """ Test method update_subject, method "POST", wrong school name,
        check whether response has a warning """

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "{}"'.format(self.arg_dict_subj['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/subject_update',
                                      method="POST",
                                      data=self.arg_dict_subj_negative):
            response = self.admin.update_subject(test_id)
            self.assertIn('Некоректно введено назву'.decode('utf-8'),
                          response)

    def test_update_subject_content(self):
        """ Test method update_subject, method "GET",
        check whether response is HTML """

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "{}"'.format(self.arg_dict_subj['name']))
        test_id = results_before[0]['id']
        dict_subj_changed = {
            'name': self.arg_dict_subj['name'] + "ЗмІнЕнИй"}
        with app.test_request_context(path='/subject_update',
                                      method="GET",
                                      data=dict_subj_changed):
            response = self.admin.update_subject(test_id)
            self.assertTrue(response.find("</html>") >= 0)

    def test_update_subject_db_result(self):
        """ Test method update_subject, method "POST",
        check changes in DB - whether object is updated """

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "{}"'.format(self.arg_dict_subj['name']))
        test_id = results_before[0]['id']
        dict_subj_changed = {
            'name': self.arg_dict_subj['name'] + "ЗмІнЕнИй"}
        with app.test_request_context(path='/subject_update',
                                      method="POST",
                                      data=dict_subj_changed):
            response = self.admin.update_subject(test_id)
            results_after = self.orm.mysql_do(
                ExtendedSubjectsModel.select_subjects_query +
                ' where name = "{}"'.format((dict_subj_changed['name'])))
            self.assertTrue(len(results_before) == len(results_after))

    def test_remove_subject_response(self):
        """ Test method remove_subject, method "POST", check status code """

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "{}"'.format(self.arg_dict_subj['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/subject_remove',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.remove_subject(test_id)
            self.assertTrue(response.status_code == 302)

    def test_remove_subject_response_negative(self):
        """ Test method remove_subject, method "GET", negative test,
        trying to delete non-existent subject """

        with app.test_request_context(path='/subject_remove',
                                      method="GET",
                                      data=self.arg_dict_subj_negative):
            try:
                response = self.admin.remove_subject(777777777777777)
            except Exception as error:
                print(error)
                self.assertTrue(False)

    def test_remove_subject_content(self):
        """ Test method remove_subject, method "GET",
        check whether response is HTML """

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "{}"'.format(self.arg_dict_subj['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/subject_remove',
                                      method="GET",
                                      data=self.arg_dict_subj):
            response = self.admin.remove_subject(test_id)
            self.assertTrue(response.find("</html>") >= 0)

    def test_remove_subject_db_results(self):
        """ Test method remove_subject, method "POST",
        check changes in DB - whether object is removed """

        results_before = self.orm.mysql_do(
            ExtendedSubjectsModel.select_subjects_query +
            ' where name = "{}"'.format(self.arg_dict_subj['name']))
        test_id = results_before[0]['id']
        with app.test_request_context(path='/subject_remove',
                                      method="POST",
                                      data=self.arg_dict_subj):
            response = self.admin.remove_subject(test_id)
            results_after = self.orm.mysql_do(
                ExtendedSubjectsModel.select_subjects_query +
                ' where name = "{}"'.format(self.arg_dict_subj['name']))
            self.assertTrue(len(results_before) == len(results_after) + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
