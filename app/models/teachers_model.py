#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from app.utils.MySQLORM import MySQLORM

class TeachersModel(object):
	"""Class for Teachers Entity"""
	def __init__(self):
		self.get_orm('localhost', 'root', 'password', 'SMSDB')

	def get_orm(self, host, username, password, db):
		self.orm = MySQLORM()
		self.orm.connect(host, username, password, db)
		return self.orm

	def get_teacher_by_id(self, id_):
		'''Method for getting dict of one teacher by id'''
		return self.orm.get(teachers_table, {'id' : '%s'} % id_)

	def get_all_teachers(self):
		'''Method for getting list of all teachers'''
		sql = 'SELECT id, name, login, password, email from teachers_table \
		INNER JOIN roles_table ON roles_table.id = teachers_table.role_id \
		INNER JOIN schools_table ON schools_table.id = teachers_table.teacher_id'
		return self.orm.mysql_do(sql)

	def add_teacher(self, **kwargs):
		'''Method for adding new teacher, **kwarg - dictionary, for example: {'name':'Sasha', 'login' : 'sasha_login', ... e.t.c.}'''
		sqlresult = self.orm.insert(table, 'name', 'login', 'passwd', kwargs['name'], kwargs['login'],kwargs['password'])
        # TO DO

	def edit_teacher(self):
		pass

	def delete_teacher(self):
		pass

	def get_role_by_id(self, id_):
		pass

	def get_all_roles(self):
		pass


