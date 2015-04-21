# -*- coding: utf-8 -*-

from flask import render_template, request

from app import app
from app.controllers.controller import AdminController


controller = AdminController()


@app.route('/')
@app.route('/index')
def index():
    """Render main page"""

    return controller.get_index()


@app.route('/users_list')
def users_list():
    """Render page with users list"""

    return controller.get_view_all()


@app.route('/user_add', methods=['GET', 'POST'])
def user_add():
    """Render page with users list"""

    return controller.get_view_add_get()


@app.route('/user_remove/', methods=['GET', 'POST'])
@app.route('/user_remove/<int:id_>', methods=['GET', 'POST'])
def user_remove(id_):
    """Render page with users list"""

    return controller.remove_user(id_=id_)


@app.errorhandler(404)
def page_not_found(error):
    """Render 404 error page"""

    return controller.get_error404()
