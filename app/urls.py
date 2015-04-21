# -*- coding: utf-8 -*-

from flask import render_template, request

from app import app
from app.controllers.controller import AdminController


controller = AdminController()


@app.route('/')
@app.route('/index')
def index():
    return controller.get_index()


@app.route('/users_list')
def users_list():
    return controller.get_view_all()


@app.route('/user_add', methods=['GET', 'POST'])
def user_add():
    roles = {}
    errors = {}
    return render_template('user_add.html', roles=roles, errors=errors)
    #if request.method == 'POST':
    #    return controller.get_view_add_get()


@app.errorhandler(404)
def page_not_found(error):
    return controller.get_error404()
