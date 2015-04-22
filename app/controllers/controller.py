#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import request

from app.views.view import View
from app.models.teachers_model import TeachersModel
from app.models.teachers_model_with_entity import Teacher,\
                                                  ExtendedTeachersModel

import re

class AdminController(object):

    """AdminController - user controller"""

    def __init__(self):
        self.first_model = TeachersModel()
        self.model = ExtendedTeachersModel()
        self.view = View()


    def get_index(self):
        """return index.html"""
        return self.view.render_index()

    def get_error404(self):
        """error 404"""
        return self.view.render_error()

    def get_view_all(self):
        """view => user_add.html get"""
        # get data from db
        self.data = self.model.get_all_teachers()
        # render page with all users
        return self.view.render_list_users(self.data)

    def get_view_add_get(self):
        """view => user_add.html get"""
        # define variables for sending to template
        _errors = {}

        # TO DO:
        # get all roles from DB
        _roles = self.first_model.get_all_roles()

        if request.method == 'POST':
            # save user in case here isn't any mistakes
            if self._validate_on_submite(name = request.form['name']
                                        ,login =request.form['login']
                                        ,password = request.form['password']
                                        ,email = request.form['email']
                                        ,user_role =request.form['user_role']
                                        ):
                _name = str(request.form['name'].strip())
                _login = str(request.form['login'].strip())
                _password = str(request.form['password'].strip())
                _email = str(request.form['email'].strip())
                _role = int(request.form['user_role'])

                # create entity
                _teacher = Teacher(None, _name, _login,
                                   _password, _email, _role,
                                   None, None, None)

                # TO DO:
                # - save all data in DB
                self.model.insert_teacher(_teacher)
                # redirect to users list and make status message
                return self.view.add_user_form_success(_name)

            _errors = self.message
        # render empty user add form
        return self.view.render_add_user_form(_roles, _errors)

    def update(self, id_):
        if request.method == 'POST' and request.form['update_button']:
            _user = self.model.delete_teacher_by_id(id_)
            for fields in _user:
                name = fields.name
            self.model.update_teacher_by_id(_user)
            return self.view.remove_user_form_success(name)

    def update_few(self, *id):
        pass

    def remove_user(self, id_):
        """Delete user method"""
        if request.method == 'POST' and request.form['delete_button']:
            # get user by id
            _user = self.model.get_teacher_by_id(id_)
            # get name variable for status message
            for fields in _user:
                name = fields.name
            # delete user by id
            self.model.delete_teacher_by_id(id_)

            return self.view.remove_user_form_success(name)

        # TODO:
        # fix cancel button action
        #elif request.method == 'POST' and request.form['cancel_button']:
        #    return self.get_view_all()

        return self.view.render_confirm_delete()


    def _validate_on_submite(self, **kwargs):
        """correct = true else false"""
        self.message = dict()
        # regex pattern
        email_pattern = "^[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}$"
        name_pattern = "^([A-ZА-Я])\w+\s([A-ZА-Я])\w+$"
        login_pattern = "^[A-Za-z0-9]+$"
        # check data
        if not re.match(name_pattern, kwargs.get('name')):
            self.message['name'] = u'Некоректно введно імя'

        if not kwargs.get('user_role'):
            self.message['user_role'] = u'Виберіть роль'

        if not kwargs.get('password'):
            self.message['password'] = u'Введіть пароль'

        if not re.match(login_pattern, kwargs.get('login')):
            self.message['login'] = u'Некоректно введно логин'

        if not re.match(email_pattern, kwargs.get('email')):
            self.message['email'] = u'Некоректно введно емейл'
        # If validate return true
        if self.message:
            return False
        else:
            return True