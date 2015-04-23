#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.utils.dbdriver import MySQLORM
from config import credentials


class School(object):

    """This class creates school objects to use them in School Model"""

    def __init__(self, id_, name, address):
        self.id_ = id_
        self.name = name
        self.address = address


class ExtendedSchoolsModel(object):

    """This class is used to retrieve data about schools from DB"""

    select_schools_query = ' SELECT id, name, address  \
                            FROM Schools '

    def __init__(self):
        pass

    def initORM(self):
        """Make connect to database"""

        host = credentials[0]
        username = credentials[1]
        password = credentials[2]
        db = credentials[3]
        orm = MySQLORM()
        orm.connect(host, username, password, db)
        return orm

    def get_all_schools(self):
        """Get all schools from DB"""
        return self._get_schools()

    def get_school_by_id(self, id_):
        """Get school by given id"""
        return self._get_schools('WHERE t.id=%d' % (id_))

    def update_school_by_id(self, school):
        """Update school by id"""
        orm = self.initORM()
        orm.update('schools', 'name="%s", address="%s"' %
                   (school.name, school.address),
                   'id=%d' % (school.id_))
        orm.close()

    def delete_school_by_id(self, id_):
        """Delete school by given id"""
        orm = self.initORM()
        orm.delete('schools', 'id = %d' % (id_))
        orm.close()

    def insert_school(self, school):
        """Insert school into DB"""
        orm = self.initORM()
        orm.insert('schools', ('name', 'address'),
                   (school.name, school.address))
        orm.close()

    def _create_list_from_dbresult(self, results):
        """Make list of schools objects from select"""
        schools = []
        for row in results:
            id_ = row["id"]
            name = row["name"]
            address = row["address"]
            school = School(id_, name, address)
            schools.append(school)
        return schools

    def _get_schools(self, condition=''):
        """Select schools from db"""
        orm = self.initORM()
        results = orm.mysql_do(self.select_schools_query + ' ' + condition)
        schools = self._create_list_from_dbresult(results)
        orm.close()
        return schools
