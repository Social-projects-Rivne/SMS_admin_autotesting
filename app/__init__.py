# -*- coding: utf-8 -*-

from flask import Flask

from utils.dbdriver import MySQLORM


app = Flask(__name__)
app.config.from_object('config')

from app import urls