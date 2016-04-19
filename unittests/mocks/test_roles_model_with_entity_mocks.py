# -*- coding: utf-8 -*-
""" Unit tests for roles_model_with_entity on mock """
import unittest
import mock

import app.models.roles_model_with_entity
from app.models.roles_model_with_entity import Role
from db import credentials


class TestRole(unittest.TestCase):
    """ Class to test class Role """
    def test_creation_of_role(self):
        """ Basic smoke test: object role is created """
        my_test_role = Role(2, u'Завуч')
        self.assertIsInstance(my_test_role, Role)


class TestExtendedRolesModel(unittest.TestCase):
    """ Class to test ExtendedRolesModel class """
    def setUp(self):
        """ Preparation """
        self.test_role_name = u"Завуч"
        self.test_role_id = 2
        self.roles_model = \
            app.models.roles_model_with_entity.ExtendedRolesModel()

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.database = credentials[3]

        self.test_list = [
            {'id': 1, 'name': u'Директор'},
            {'id': 2, 'name': u'Завуч'},
            {'id': 3, 'name': u'Викладач'}, ]

        self.roles = app.models.roles_model_with_entity.\
            Role(self.test_role_id,
                  self.test_role_name)
    @mock.patch('app.models.roles_model_with_entity.DBDriver')
    def test_init_orm(self, mock_dbdriver):
        """ Testing method initORM, check correct call of dbdriver """

        dbdriver_execute_mock = mock.Mock()

        mock_dbdriver.return_value = dbdriver_execute_mock
        app.models.roles_model_with_entity.ExtendedRolesModel.initORM(
            self.roles_model)

        call = self.host, self.username, self.password, self.database
        dbdriver_execute_mock.connect.assert_called_with(*call)
    @mock.patch('app.models.roles_model_with_entity.DBDriver')
    def test_get_all_roles(self, mock_dbdriver):
        """ Test to check whether get_all_roles \
        returns list of roles"""

        self.roles_model.get_all_roles = \
        mock.Mock(return_value=({'id':1, 'role_name': u'Викладач'}, \
        {'id':2, 'role_name':u'Завуч'},))
        all_roles = self.roles_model.get_all_roles()
        self.assertEqual(all_roles[0]['id'], 1)
        self.assertEqual(all_roles[1]['role_name'], u'Завуч')
    @mock.patch('app.models.roles_model_with_entity.DBDriver')
    def test_get_role_by_id(self, mock_dbdriver):
        """ Test to check whether get_role_by_id \
        returns object with id that set"""

        self.roles_model.get_role_by_id = \
        mock.Mock(return_value=self.test_list)
        role_by_id = self.roles_model.get_role_by_id()
        self.assertEqual(role_by_id[0]['id'], 1)
    @mock.patch('app.models.roles_model_with_entity.DBDriver')
    def test_create_list_from_dbresult(self, mock_dbdriver):
        """ Test to check whether create_list_from_dbresult \
        returns list with objects """

        self.roles_model._create_list_from_dbresult = \
        mock.Mock(return_value=self.test_list)
        list_of_roles = self.roles_model._create_list_from_dbresult()
        self.assertEqual(list_of_roles[0]['id'], 1)
if __name__ == "__main__":
    unittest.main(verbosity=2)


