#!/usr/bin/env python
#-*-coding:utf-8-*-

import unittest
import mock

import app.models.roles_model
from app.models.roles_model import RolesModel
from app.utils.dbdriver import DBDriver
from db import credentials


class TestRolesModel(unittest.TestCase):
    """ Class with methods for testing RolesModel class """

    def setUp(self):
        self.roles = RolesModel()
        self.test_roles = [
            {'id':1, 'role_name':u'Роль1'},
            {'id':2, 'role_name':u'Роль2'}, ]

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.database = credentials[3]

    @mock.patch('app.models.roles_model.DBDriver')
    def test_initORM(self, mock_dbdriver):
        """ Testing method initORM, check correct call of dbdriver """

        dbdriver_execute_mock = mock.Mock()
        #mock_dbdriver = mock.Mock(return_value=dbdriver_execute_mock)

        mock_dbdriver.return_value = dbdriver_execute_mock
        app.models.roles_model.RolesModel.initORM(
            self.roles)

        call = self.host, self.username, self.password, self.database
        dbdriver_execute_mock.connect.assert_called_with(*call)

    def test_initORM_content(self):
        """ Check that function is not empty """

        self.roles.initORM = mock.Mock(return_value='I am mock')
        self.assertEqual(self.roles.initORM(), 'I am mock')

    def test_initORM_isinstance(self):
        """ Check that function is object of DBDriver """
        orm = self.roles.initORM()
        self.assertIsInstance(orm, DBDriver)

    def test_get_all_roles(self):
        """ Test, that checks, whether get_all_roles
        return an object """
        self.roles.get_all_roles = mock.Mock(return_value=({'id':1}, {'id':2, 'role_name':u'Завуч'},))
        all_roles = self.roles.get_all_roles()
        self.assertEqual(all_roles[0]['id'], 1)
        self.assertEqual(all_roles[1]['role_name'], u'Завуч')

    def test_select_roles_query(self):
        """ Test, that checks select_roles_query """

        self.assertEqual(RolesModel.select_roles_query, \
                         "SELECT id, role_name FROM Roles")

    @mock.patch('app.models.roles_model.DBDriver')
    def test_get_all_roles(self, mock_dbdriver):
        """ Testing method get_all_roles, check correct method call
        and whether the results is equal with given in test """

        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        dbdriver_execute_mock.mysql_do.return_value = self.test_roles
        mock_dbdriver.return_value = dbdriver_execute_mock

        result = app.models.roles_model.RolesModel.get_all_roles(
            self.roles)

        call_sql = app.models.roles_model.RolesModel.select_roles_query + ' '

        dbdriver_execute_mock.mysql_do.assert_called_with(call_sql)

        self.assertEqual(len(self.test_roles), len(result))
        for roles_object in result:
            for roles_dict in self.test_roles:
                if roles_dict['id'] == roles_object.id_ \
                        and roles_dict['role_name'] == roles_object.role_name:
                    self.test_roles.remove(roles_dict)
        self.assertEqual(len(self.test_roles), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
