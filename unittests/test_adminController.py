    # -*- coding: utf-8 -*-
import os
import unittest
import sys
import urllib2

from flask import Flask

from app import app
import config as config
from app.controllers.controller import AdminController
from db import credentials


__author__ = 'boris'

class TestAdminController(unittest.TestCase):
    def setUp(self):
        """ Fixture that creates a initial data and records for tests """
        # app = aPP(__name__, template_folder='app/templates')
        # self.app = Flask(__name__, template_folder='app/templates')
        # self.app.config.from_object('config')
        # self.app.root_path = config.basedir
        # DB_ROOT = os.path.join(config.basedir, '..', 'database_settings')
        # self.app.config['TESTING'] = True
        #
        # self.app.test_client()

    def tearDown(self):
        """ Fixture that deletes all preparation for tests """
        try:
            pass
        except:
            pass
        finally:
            pass

    def test_creation_of_object(self):
        self.assertIsNotNone(AdminController())

    def test_type_if_object(self):
        self.assertTrue(isinstance(AdminController(), AdminController))

    """
    def test_get_index(self):
        print("test_get_index")
        with app.test_request_context():
            controller = AdminController()
            print("index")
            print(controller.get_index())
            # print(1)
            # print(controller)
            self.fail()
    """
    """
    def test_get_login(self):
        self.fail()

    def test_get_error404(self):
        self.fail()

    """
    # @app.route('/users_list')
    # @login_required
    """
    def test_list_all_users(self):

        print("test_list_all_users")

        app = Flask(__name__)
        app.root_path = config.basedir
        controller = AdminController()
        with app.app_context():
            controller.list_all_users()
        self.fail()

    """

    def test_add_user(self):
        arg_dict = {'name':'name','login':'login',
            'password':'password','email':'email',
            'user_role':'user_role'}

        with app.test_request_context(path = '/user_add', method="POST", data = arg_dict ):
            controller = AdminController()
            print(controller.add_user())

        # self.fail()

    """
    def test_update_user(self):
        self.fail()

    def test_remove_user(self):
        self.fail()

    def test_list_all_schools(self):
        self.fail()

    def test_add_school(self):
        self.fail()

    def test_update_school(self):
        self.fail()

    def test_remove_school(self):
        self.fail()
    """

    def test_list_all_subjects(self):
        print("test_list_all_subjects")

        with app.test_request_context(path = '/subjects_list', method="GET"):
            # rv = app.preprocess_request()

            controller = AdminController()
            print(controller.list_all_subjects())

            # if rv != None:
            #     response = self.app.make_response(rv)
            # else:
                # do the main dispatch
                # rv = app.dispatch_request()
                # response = app.make_response(rv)

                # now do the after funcs
                # response = app.process_response(response)

        # self.fail()

    def test_add_subject_get_responce(self):
        print("test_add_subject_get_responce")
        arg_dict = {'name': 'Предмет'}
        appt = app.test_client()
        responce = appt.post(path='/subject_add', method="GET", data=arg_dict)
        print(responce)

    def test_add_subject_post_responce(self):
        print("test_add_subject_post_responce")
        arg_dict = {'name': 'Предмет'}
        appt = app.test_client()
        responce = appt.post(path='/subject_add', method="POST", data=arg_dict)
        print(responce)

    def test_add_subject_get_content(self):
        print("test_add_subject_get_content")
        arg_dict = {'name': 'Предмет'}
        with app.test_request_context(path='/subject_add', method="GET",
                                      data=arg_dict):

            rv = app.preprocess_request()

            controller = AdminController()
            req = controller.add_subject()
            print(req)
            print(type(req))
            # print(controller.add_subject())

    def test_add_subject_post_content(self):
        print("test_add_subject_post_content")
        arg_dict = {'name': 'Предмет'}
        with app.test_request_context(path='/subject_add', method="POST",
                                      data=arg_dict):
            rv = app.preprocess_request()

            controller = AdminController()
            print(controller.add_subject())


    """
    def test_update_subject(self):
        self.fail()

    def test_remove_subject(self):
        # controller = AdminController()
        # controller.remove_subject()
        self.fail()
    """


if __name__ == "__main__":
    unittest.main(verbosity=2)