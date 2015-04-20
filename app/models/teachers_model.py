# -*- coding: utf-8 -*-
import MySQLdb
import MySQLORM

class TeachersModel(ModelToDB):
	"""Class for Teachers Entity"""
	def __init__(self):
		get_orm('ss_sms_admin', 'root', 'password', 'ss_sms_db')
		
	def get_orm(self, host, username, password, db):
		self.orm = MySQLORM()
		self.orm.connect(host, username, password, db)
		return self.orm

	def get_teacher_by_id(self, id_):
		sql_result = orm.get(teachers_table, {'id' : '%s'} % id_)
		return sql_result

	def get_all_teachers(self):
		sql = SELECT id, name, login, password, email from teachers_table \
		INNER JOIN roles_table ON roles_table.id = teachers_table.role_id \
		INNER JOIN schools_table ON schools_table.id = teachers_table.teacher_id
		sqlresult = orm.mysql_do(sql)
        return dictresult
            #todo
		




	def add_teacher(self, **kwargs):
		orm.insert(...)

	def update_teacher(self):
		pass

	def delete_teacher(self):
		pass

