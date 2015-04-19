# -*- coding: utf-8 -*-
import MySQLdb
import MySQLORM

class ModelToDB(MySQLORM):
	"""Class for relations Models to MySQLORM"""
	def __init__(self, arg):
		MySQLORM.connect('host', 'username', 'db')
		#To Do
	def add():
		pass
