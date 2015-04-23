#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.utils.dbdriver import DBDriver
from config import credentials


class Teacher(object):

    """This class creates teacher objects to use them in Teacher Model"""

    def __init__(self, id_, name, login, password, email,
                 role_id, role_name,
                 school_id, school_name):
        self.id_ = id_
        self.name = name
        self.login = login
        self.password = password
        self.email = email
        self.role_id = role_id
        self.role_name = role_name
        self.school_id = school_id
        self.school_name = school_name


class ExtendedTeachersModel(object):

    """This class is used to retrieve data about teachers from DB"""

    select_teachers_query = 'SELECT t.id as id, t.name as name, \
                            t.login as login, t.email as email, \
                            t.password as password, t.role_id as role_id, \
                            t.school_id as school_id, \
                                r.role_name as role_name, \
                                s.name as school_name \
                            FROM Teachers t \
                            INNER JOIN Roles r \
                                ON t.role_id=r.id\
                            LEFT JOIN Schools s\
                                ON t.school_id=s.id'

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

    def get_all_teachers(self):
        """Get all teachers from DB"""
        return self._get_teachers()

    def get_teacher_by_id(self, id_):
        """Get teacher by given id"""
        return self._get_teachers('WHERE t.id=%d' % (id_))

    def get_all_teachers_by_role(self, role_id):
        """Get all teachers by given role id"""
        return self._get_teachers('WHERE role_id=%d' % (role_id))

    def get_all_teachers_by_school(self, school_id):
        """Get all teachers by given school id"""
        return self._get_teachers('WHERE school_id=%d' % (school_id))

    def update_teacher_by_id(self, teacher):
        """Update teacher by id"""
        orm = self.initORM()
        orm.update('Teachers', 'name="%s", login="%s", email="%s", password="%s", role_id=%d' %
                   (teacher.name, teacher.login, teacher.email,
                    teacher.password, teacher.role_id),
                   'id=%d' % (teacher.id_))
        orm.close()

    def delete_teacher_by_id(self, id_):
        """Delete teacher by given id"""
        orm = self.initORM()
        orm.delete('Teachers', 'id = %d' % (id_))
        orm.close()

    def insert_teacher(self, teacher):
        """Insert teacher into DB"""
        orm = self.initORM()
        orm.insert('Teachers', ('name', 'login', 'email', 'password', 'role_id'),
                   (teacher.name, teacher.login, teacher.email, teacher.password, teacher.role_id))
        orm.close()

    def set_role_id_to_teacher_by_id(self, id_, role_id):
        """Set teacher's role id"""
        orm = self.initORM()
        orm.update('Teachers', 'role_id=%d' % (role_id), 'id=%d' % (id_))
        orm.close()

    def set_school_id_to_teacher_by_id(self, id_, school_id):
        """Set teacher's school id"""
        orm = self.initORM()
        orm.update('Teachers', 'school_id=%d' % (school_id), 'id=%d' % (id_))
        orm.close()

    def set_password_to_teacher_by_id(self, id_, password):
        """Set teacher's password"""
        orm = self.initORM()
        orm.update('Teachers', 'password="%s"' % (password), 'id=%d' % (id_))
        orm.close()

    def _create_list_from_dbresult(self, results):
        """Make list of teacher objects from select"""
        teachers = []
        for row in results:

            id_ = row["id"]
            name = row["name"]
            login = row["login"]
            password = row["password"]
            email = row["email"]
            role_id = row["role_id"]
            role_name = row["role_name"]
            school_id = row["school_id"]
            school_name = row["school_name"]
            teacher = Teacher(id_, name, login, password, email,
                              role_id, role_name,
                              school_id, school_name)
            print teacher
            teachers.append(teacher)
        return teachers

    def _get_teachers(self, condition=''):
        """Select teachers from db"""
        orm = self.initORM()
        # print self.select_teachers_query + ' ' + condition
        results = orm.mysql_do(self.select_teachers_query + ' ' + condition)
        #results=orm.mysql_do('select * from Teachers')
        teachers = self._create_list_from_dbresult(results)
        orm.close()
        return teachers
