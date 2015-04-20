# -*- coding: utf-8 -*-
import ModelToDB

class RolesModel(ModelToDB):
	"""Class for Roles entity"""
	def __init__(self, id, role_name):
		self.id = id
		self.role_name = role_name
