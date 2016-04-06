#!/usr/bin/env python
#-*-coding:utf-8-*-

import unittest
from app.models.roles_model import RolesModel


class TestRolesModel(unittest.TestCase):

    def setUp(self):
        self.roles = RolesModel()

    def test_initORM(self):
        """Check that function is not empty"""
        self.assertIsNotNone(self.roles.initORM())

    def test_get_all_roles(self):
        """Test, that checks, whether get_all_roles
        return an object"""
        all_roles = self.roles.get_all_roles()
        self.assertEqual(all_roles[0]['id'], 1)
        self.assertEqual(all_roles[1]['role_name'], u'Завуч')

    def test_select_roles_query(self):
        """Test, that checks select_roles_query"""
        self.assertEqual(RolesModel.select_roles_query, \
                         "SELECT id, role_name FROM Roles")

if __name__ =='__main__':
    unittest.main(verbosity=2)
