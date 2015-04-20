# -*- coding: utf-8 -*-

from flask import Flask

from utils.MySQLORM import MySQLORM


app = Flask(__name__)
app.config.from_object('config')

from app import urls