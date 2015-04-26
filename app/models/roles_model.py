#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.utils.dbdriver import DBDriver
from config import credentials

class RolesModel(object):

    """This class is used to retrieve data about roles from DB"""

    select_roles_query = 'SELECT id, role_name FROM Roles'

    def __init__(self):
        pass

    def initORM(self):
        """Make connect to database"""
        host = credentials[0]
        username = credentials[1]
        password = credentials[2]
        db = credentials[3]
        orm = DBDriver()
        orm.connect(host, username, password, db)
        return orm

    def get_all_roles(self):
        """Get all roles from DB"""
        orm = self.initORM()
        roles = orm.mysql_do(self.select_roles_query)
        orm.close()
        return roles