#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.utils.dbdriver import DBDriver
from config import credentials

class TeachersModel(object):
	"""Class for Teachers Entity"""
	def __init__(self):
		self.get_orm(*credentials)


	def get_orm(self, host, username, password, db):
		self.orm = DBDriver()
		self.orm.connect(host, username, password, db)
		return self.orm

	def get_teacher_by_id(self, id_):
		'''Method for getting dict of one teacher by id'''
		sql = 'SELECT t.id id, t.name name, t.login login, t.password password, t.email email, r.role_name role_name, s.name school_name FROM Teachers t \
		INNER JOIN Roles r ON r.id = t.role_id \
		INNER JOIN Schools s ON s.id = t.school_id WHERE t.id = %s' % id_
		return self.orm.mysql_do(sql)

	def get_all_teachers(self):
		'''Method for getting list of all teachers'''
		sql = 'SELECT t.id id, t.name name, t.login login, t.password password, t.email email, r.role_name role_name, s.name school_name FROM Teachers t \
		INNER JOIN Roles r ON r.id = t.role_id \
		INNER JOIN Schools s ON s.id = t.school_id'
		return self.orm.mysql_do(sql)

	def add_teacher(self, **kwargs):
		'''Method for adding new teacher, **kwarg - dictionary, for example: {'name':'Sasha', 'login' : 'sasha_login', ... e.t.c.}'''
		sqlresult = self.orm.insert('Teachers', 'name', 'login', 'passwd', kwargs['name'], kwargs['login'],kwargs['password'])
        # TO DO

	def edit_teacher(self):
		pass

	def delete_teacher(self):
		pass

	def get_role_by_id(self, id_):
		'''Method for getting dict of one role by id'''
		sql = 'SELECT id, role_name FROM Roles WHERE id = %s' % id_
		return self.orm.mysql_do(sql)

	def get_all_roles(self):
		'''Method for getting list of dict all roles'''
		sql = 'SELECT id, role_name FROM Roles'
		return self.orm.mysql_do(sql)


