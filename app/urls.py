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

@app.route('/user_upgrade/', methods=['GET', 'POST'])
@app.route('/user_upgrade/<int:id_>', methods=['GET', 'POST'])
def user_upgrade(id_):
    """Return update user form"""

    return controller.update_user(id_=id_)


@app.errorhandler(404)
def page_not_found(error):
    """Render 404 error page"""

    return controller.get_error404()

#---Routes for schools----
@app.route('/schools_list')
def schools_list():
    """Render page with schools list"""
    return controller.get_view_all_schools()

@app.route('/school_add', methods=['GET', 'POST'])
def school_add():
    """Render page with school add"""
    return controller.get_view_add_school()

@app.route('/school_remove/', methods=['GET', 'POST'])
@app.route('/school_remove/<int:id_>', methods=['GET', 'POST'])
def school_remove(id_):
    """Render page with school_remove"""
    return controller.remove_school(id_=id_)

@app.route('/school_upgrade/', methods=['GET', 'POST'])
@app.route('/school_upgrade/<int:id_>', methods=['GET', 'POST'])
def school_upgrade(id_):
    """Return update school form"""
    return controller.update_school(id_=id_)

#---Routes for subjects----
@app.route('/subjects_list')
def subjects_list():
    """Render page with subjects list"""
    return controller.get_view_all_subjects()

@app.route('/subject_add', methods=['GET', 'POST'])
def subject_add():
    """Render page with subject add"""
    return controller.get_view_add_subject()

@app.route('/subject_remove/', methods=['GET', 'POST'])
@app.route('/subject_remove/<int:id_>', methods=['GET', 'POST'])
def subject_remove(id_):
    """Render page with subject_remove"""
    return controller.remove_subject(id_=id_)

@app.route('/subject_upgrade/', methods=['GET', 'POST'])
@app.route('/subject_upgrade/<int:id_>', methods=['GET', 'POST'])
def subject_upgrade(id_):
    """Return update subject form"""
    return controller.update_subject(id_=id_)