import os
import unittest

import sys
from flask import Flask
from app import app
import config as config
from app.utils.dbdriver import DBDriver
from app.controllers.controller import AdminController
# from app.utils.login_required import login_required
from db import credentials


__author__ = 'boris'

class TestAdminController(unittest.TestCase):
    def setUp(self):
        """ Fixture that creates a initial data and records for tests """
        app.config['TESTING'] = True
        app.test_client()
        pass
        # from app import app
        #
        # app.run(debug = True)

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

    # @app.route('/')
    # @app.route('/index')
    # @login_required
    def test_get_index(self):
        app = Flask(__name__, template_folder='app/templates')
        app.root_path = config.basedir
        DB_ROOT = os.path.join(config.basedir, '..', 'database_settings')
        sys.path.append(DB_ROOT)
        app.config.from_object('config')
        print(config.basedir)
        print( app.root_path)
        with app.app_context():
            controller = AdminController()
            controller.get_index()
            # print(1)
            # print(controller)
            self.fail()
    """
    def test_get_login(self):
        self.fail()

    def test_get_error404(self):
        self.fail()

    """
    # @app.route('/users_list')
    # @login_required
    def test_list_all_users(self):
        app = Flask(__name__)
        app.root_path = config.basedir
        controller = AdminController()
        with app.app_context():
            controller.list_all_users()
        self.fail()

    def test_add_user(self):

        self.fail()

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

    def test_list_all_subjects(self):
        self.fail()

    def test_add_subject(self):
        self.fail()

    def test_update_subject(self):
        self.fail()

    def test_remove_subject(self):
        self.fail()


if __name__ == "__main__":
    unittest.main(verbosity=2)