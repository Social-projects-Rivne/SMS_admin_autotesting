# -*- coding: utf-8 -*-
import ModelToDB

class SchoolsModel(ModelToDB):
	"""Class for Schools entity"""
	def __init__(self, id, name):
		self.id = id
		self.name = name
