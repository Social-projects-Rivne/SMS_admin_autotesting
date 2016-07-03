#!/usr/bin/env python
#-*-coding:utf-8-*-

import unittest
from app.models.roles_model import RolesModel
from app.utils.dbdriver import DBDriver


class TestRolesModel(unittest.TestCase):
    """ Class with methods for testing RolesModel class """

    def setUp(self):
        self.roles = RolesModel()

    def test_initORM(self):
        """ Check that function is not empty """

        orm = self.roles.initORM()
        self.assertIsNotNone(orm)

    def test_initORM_isinstance(self):
        """ Check that function is object of DBDriver """

        orm = self.roles.initORM()
        self.assertIsInstance(orm, DBDriver)

    def test_get_all_roles(self):
        """ Test, that checks, whether get_all_roles
        return an object """

        all_roles = self.roles.get_all_roles()
        self.assertEqual(all_roles[0]['id'], 1)
        self.assertEqual(all_roles[1]['role_name'], u'Завуч')

    def test_select_roles_query(self):
        """ Test, that checks select_roles_query """

        self.assertEqual(RolesModel.select_roles_query, \
                         "SELECT id, role_name FROM Roles")

if __name__ == '__main__':
    unittest.main(verbosity=2)
