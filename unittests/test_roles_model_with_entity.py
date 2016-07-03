#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" File to test roles_model_with_entity """
import unittest
from app.utils.dbdriver import DBDriver

from app.models.roles_model_with_entity import Role, \
    ExtendedRolesModel


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
        self.erm = ExtendedRolesModel()
        self.role_to_test = Role(self.test_role_id, self.test_role_name)

        from db import credentials
        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.dbname = credentials[3]

        self.orm = DBDriver()
        self.orm.connect(self.host, self.username, self.password, self.dbname)

    def tearDown(self):
        """ Fixture that deletes all preparation for tests """
        self.orm.close()

    def test_init_orm(self):
        """ Basic smoke test: ORM is initialized """
        self.assertIsNotNone(self.erm.initORM())

    def test_get_all_roles(self):
        """ Test to check if get_all_roles returns list of 3 elements """
        roles = self.erm.get_all_roles()
        self.assertTrue(len(roles) == 3)

    def test_get_role_by_id(self):
        """ Test to check whether get_role_by_id \
         returns object with id that set"""
        roles_by_id = self.erm.get_role_by_id(self.test_role_id)
        self.assertTrue(roles_by_id[0].role_name == self.test_role_name)

    def test_create_list_from_dbresult(self):
        """ Test to check whether create_list_from_dbresult \
        returns list with objects """
        role = \
        self.erm._get_roles('WHERE id=%d' % (self.test_role_id))
        self.assertIsInstance(role, list)


if __name__ == "__main__":
    unittest.main(verbosity=2)

