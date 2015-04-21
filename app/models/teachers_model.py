# -*- coding: utf-8 -*-
import MySQLdb
from app.utils.MySQLORM import MySQLORM

class TeachersModel(object):
	"""Class for Teachers Entity"""
	def __init__(self):
		get_orm('ss_sms_admin', 'root', 'password', 'SMSDB')
		
	def get_orm(self, host, username, password, db):
		self.orm = MySQLORM()
		self.orm.connect(host, username, password, db)
		return self.orm

	def get_teacher_by_id(self, id_):
		'''Method for getting dict of one teacher by id'''
		sqlresult = self.orm.get(teachers_table, {'id' : '%s'} % id_)
		return create_dict(sqlresult)

	def get_all_teachers(self):
		'''Method for getting list of all teachers'''
		sql = 'SELECT id, name, login, password, email from teachers_table \
		INNER JOIN roles_table ON roles_table.id = teachers_table.role_id \
		INNER JOIN schools_table ON schools_table.id = teachers_table.teacher_id'
		sqlresult = self.orm.mysql_do(sql)
        return create_list(sqlresult)

	def add_teacher(self, **kwargs):
		'''Method for adding new teacher, **kwarg - dictionary, for example: {'name':'Sasha', 'login' : 'sasha_login', ... e.t.c.}'''
		sqlresult = self.orm.insert(table, 'name', 'login', 'passwd', kwargs['name'], kwargs['login'],kwargs['password'])
        # TO DO
	def update_teacher(self):
		pass

	def delete_teacher(self):
		pass

	def create_dict(self,sqlrow):
		'''Helper method to create dictionary from sqlrow'''
		sqlrow_dict = {
		'id' : sqlrow[0],
		'name' : sqlrow[1],
		'login' : sqlrow[2],
		'password' : sqlrow[3],
		'email' : sqlrow[4],
		'role' : sqlrow[5],
		'schoole' : sqlrow[6],
		}
		return sqlrow_dict
	
	def create_list(self,sqlresult):
		'''Helper method to create list of sqlrows'''
		sqlresult_list = []
		for sqlrow in sqlresult:
			dict_list.append(create_dict(sqlrow))
		return sqlresult_list


