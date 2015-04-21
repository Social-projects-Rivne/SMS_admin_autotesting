#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import request

from app.views.view import View
from app.models.teachers_model import TeachersModel


class AdminController(object):

    """AdminController - user controller"""

    def __init__(self):
        self.model = TeachersModel()
        self.view = View()

    def validate_on_submite(self, **kwargs):
        """correct = true else false"""
        self.message = dict()
        # regex pattern
        email_pattern = "^[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}$"
        name_pattern = "^([A-Z])\w+\s([A-Z])\w+$"
        login_pattern = "^[A-Za-z0-9]+$"
        # check data
        if not re.match(name_pattern, kwargs.get('name')):
            self.message['name'] = 'Invalid name'

        if not kwargs.get('role'):
            self.message['role'] = 'Invalid role'

        if not kwargs.get('password'):
            self.message['password'] = 'Invalid password'

        if not re.match(login_pattern, kwargs.get('login')):
            self.message['login'] = 'Invalid login'

        if not kwargs.get('school'):
            self.message['school'] = 'Invalid school'

        if not re.match(email_pattern, kwargs.get('email')):
            self.message['email'] += 'Invalid email address'
        # If validate return true
        if self.message:
            return False
        else:
            return True

    def get_index(self):
        """return index.html"""
        return self.view.render_index()

    def get_error404(self):
        """error 404"""
        return self.view.render_error()

    def get_view_add_get(self):
        """view => user_add.html get"""
        # define variables for sendind to template
        _errors = {}

        # TO DO:
        # get all roles from DB
        _roles = ({'id': 1, 'role_name': 'Admin'},
                 {'id': 2, 'role_name': 'Zav'},
                 {'id': 3, 'role_name': 'Teacher'})

        if request.method == 'POST':

            _name = request.form['name'].strip()
            if not _name:
                _errors['name'] = u"ПІБ є обов’язковим"

            _login = request.form['login'].strip()
            if not _login:
                _errors['login'] = u"Логін є обов’язковим"

            _password = request.form['password'].strip()
            if not _password:
                _errors['password'] = u"Пароль є обов’язковим"

            _email = request.form['email'].strip()
            if not _email:
                _errors['email'] = u"Email є обов’язковим"

            _role = request.form['user_role']
            if not _role:
                _errors['user_role'] = u"Виберіть права зі списку"

            # save user in case here isn't any mistakes
            if not _errors:
                # TO DO:
                # - save all data in DB

                # redirect to users list and make status message
                return self.view.add_user_form_success(_name)

        # render empty user add form
        return self.view.render_add_user_form(_roles, _errors)

    def get_view_add_post(self, **kwargs):
        """view => user_add.html post"""
        self.data = kwargs
        if validate_on_submite(self.data):
            #save data to db
            self.model.set(self.data)
            #return operation succes
            return self.view.add_user_ok()
        else:
            return self.view.add_user_err(self.message)

    def get_view_all(self):
        """view => user_add.html get"""
        #get data from db
        self.data = self.model.get_all_teachers()
        #render page with all users
        return self.view.render_list_users(self.data)

