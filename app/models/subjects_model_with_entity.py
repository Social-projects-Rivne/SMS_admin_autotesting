#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.utils.dbdriver import MySQLORM
from config import credentials


class Subject(object):

    """This class creates subject objects to use them in Subject Model"""

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name


class ExtendedSubjectsModel(object):

    """This class is used to retrieve data about subjects from DB"""

    select_subjects_query = ' SELECT id, name  \
                            FROM Subjects '

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

    def get_all_subjects(self):
        """Get all subjects from DB"""
        return self._get_subjects()

    def get_subject_by_id(self, id_):
        """Get subject by given id"""
        return self._get_subjects('WHERE t.id=%d' % (id_))

    def update_subject_by_id(self, subject):
        """Update subject by id"""
        orm = self.initORM()
        orm.update('subjects', 'name="%s"' %
                   (subject.name),
                   'id=%d' % (subject.id_))
        orm.close()

    def delete_subject_by_id(self, id_):
        """Delete subject by given id"""
        orm = self.initORM()
        orm.delete('subjects', 'id = %d' % (id_))
        orm.close()

    def insert_subject(self, subject):
        """Insert subject into DB"""
        orm = self.initORM()
        orm.insert('subjects', ('name'),
                   (subject.name))
        orm.close()

    def _create_list_from_dbresult(self, results):
        """Make list of subjects objects from select"""
        subjects = []
        for row in results:
            id_ = row["id"]
            name = row["name"]
            subject = subject(id_, name)
            subjects.append(subject)
        return subjects

    def _get_subjects(self, condition=''):
        """Select subjects from db"""
        orm = self.initORM()
        results = orm.mysql_do(self.select_subjects_query + ' ' + condition)
        subjects = self._create_list_from_dbresult(results)
        orm.close()
        return subjects
