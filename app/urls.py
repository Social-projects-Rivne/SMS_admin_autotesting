# -*- coding: utf-8 -*-

from flask import request, session, redirect, url_for

from app import app
from app.controllers.controller import AdminController
from app.utils.login_required import login_required


controller = AdminController()


@app.route('/')
@app.route('/index')
@login_required
def index():
    """Return main page"""

    return controller.get_index()


@app.route('/users_list')
@login_required
def users_list():
    """Return page with users list"""
    return controller.list_all_users()


@app.route('/user_add', methods=['GET', 'POST'])
@login_required
def user_add():
    """Return user add form"""
    return controller.add_user()


@app.route('/user_remove/')
@app.route('/user_remove/<int:id_>', methods=['GET', 'POST'])
@login_required
def user_remove(id_):
    """Return page with users list"""
    return controller.remove_user(id_=id_)


@app.route('/user_update/')
@app.route('/user_update/<int:id_>', methods=['GET', 'POST'])
@login_required
def user_upgrade(id_):
    """Return update user form"""
    return controller.update_user(id_=id_)

#---Routes for schools----


@app.route('/schools_list')
@login_required
def schools_list():
    """Return page with schools list"""
    return controller.list_all_schools()


@app.route('/school_add', methods=['GET', 'POST'])
@login_required
def school_add():
    """Return page with school add"""
    return controller.add_school()


@app.route('/school_remove/')
@app.route('/school_remove/<int:id_>', methods=['GET', 'POST'])
@login_required
def school_remove(id_):
    """Return page with school_remove"""
    return controller.remove_school(id_=id_)


@app.route('/school_update/')
@app.route('/school_update/<int:id_>', methods=['GET', 'POST'])
@login_required
def school_upgrade(id_):
    """Return update school form"""
    return controller.update_school(id_=id_)

#---Routes for subjects----


@app.route('/subjects_list')
@login_required
def subjects_list():
    """Return page with subjects list"""
    return controller.list_all_subjects()


@app.route('/subject_add', methods=['GET', 'POST'])
@login_required
def subject_add():
    """Return page with subject add"""
    return controller.add_subject()


@app.route('/subject_remove/')
@app.route('/subject_remove/<int:id_>', methods=['GET', 'POST'])
@login_required
def subject_remove(id_):
    """Return page with subject_remove"""
    return controller.remove_subject(id_=id_)


@app.route('/subject_update/')
@app.route('/subject_update/<int:id_>', methods=['GET', 'POST'])
@login_required
def subject_upgrade(id_):
    """Return update subject form"""
    return controller.update_subject(id_=id_)

#---Routes for error----


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or\
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            #flash(u'Ви успішно увійшли в систему')
            return controller.get_index()
    return controller.get_login(error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    #flash(u'Ви вийшли з системи')
    return redirect(url_for('login'))


@app.errorhandler(404)
@login_required
def page_not_found(error):
    """Return 404 error page"""
    return controller.get_error404()
