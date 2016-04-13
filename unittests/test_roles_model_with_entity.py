#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from app.utils.dbdriver import DBDriver

from app.models.roles_model_with_entity import Role, \
    ExtendedRolesModel


class TestRole(unittest.TestCase):
    def test_creation_of_role(self):
        
        """Basic smoke test: object role is created"""
        
        role = Role(2, u'Завуч')
        self.assertIsInstance(role, Role)


class TestExtendedRolesModel(unittest.TestCase):
   
    def setUp(self):
        
        """Preparation"""
        
        self.test_role_name = u"Завуч"
        self.test_role_id = 2
        self.extendedRolesModel = ExtendedRolesModel()
        self.role_to_test = Role(self.test_role_id, self.test_role_name)

        from db import credentials
        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.db = credentials[3]

        self.orm = DBDriver()
        self.orm.connect(self.host, self.username, self.password, self.db)
        

    def tearDown(self):
        """Fixture that deletes all preparation for tests"""
        self.orm.close()

    def test_initORM(self):
        """Basic smoke test: ORM is initialized"""
        
        self.assertIsNotNone(self.extendedRolesModel.initORM())

    def test_get_all_roles(self):
        """Get all roles"""
        
        roles = self.extendedRolesModel.get_all_roles()
        self.assertTrue(len(roles) == 3)

    def test_get_role_by_id(self):
        """Get role by given id"""
        
        roles_by_id = self.extendedRolesModel.get_role_by_id(self.test_role_id)
        self.assertTrue(roles_by_id[0].role_name == self.test_role_name)

    def test_create_list_from_dbresult(self):
        """Check if func creates list"""
        
        role = self.extendedRolesModel._get_roles('WHERE id=%d' % (self.test_role_id))
        self.assertIsInstance(role[0], Role)


if __name__ == "__main__":
    unittest.main(verbosity=2)