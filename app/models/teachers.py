# -*- coding: utf-8 -*-
import ModelToDB
import roles, schools

class TeachersModel(ModelToDB):
	"""Class for Teachers Entity"""
	def __init__(self, id, name, login, email, password, schools_model, roles_model):
		'''schools_model in arguments - instance of SchoolsModel'''
		'''roles_model in arguments - instance of RolesModel'''
		self.id = id
		self.name = name
		self.login = login
		self.email = email
		self.password = password
		self.school_id = schools_model.id
		self.role_id = roles_model.role_id
