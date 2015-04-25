#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.utils.dbdriver import DBDriver
from config import credentials


class Role(object):

    """This class creates role objects to use them in Role Model"""

    def __init__(self, id_, role_name):
        self.id_ = id_
        self.role_name = role_name

class ExtendedRolesModel(object):

    """This class is used to retrieve data about roles from DB"""

    select_roles_query = ' SELECT id, role_name  \
                            FROM Roles '

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
        return self._get_roles()

    def get_role_by_id(self, id_):
        """Get role by given id"""
        return self._get_roles('WHERE id=%d' % (id_))

    def _create_list_from_dbresult(self, results):
        """Make list of roles objects from select"""
        roles = []
        for row in results:
            id_ = row["id"]
            role_name = row["role_name"]
            role = role(id_, role_name)
            roles.append(role)
        return roles

    def _get_roles(self, condition=''):
        """Select roles from db"""
        orm = self.initORM()
        results = orm.mysql_do(self.select_roles_query + ' ' + condition)
        roles = self._create_list_from_dbresult(results)
        orm.close()
        return roles
