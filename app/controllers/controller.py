#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from flask import request

from app.views.view import View
from app.models.teachers_model import TeachersModel
from app.models.teachers_model_with_entity import Teacher,\
                                                  ExtendedTeachersModel
from app.models.subjects_model_with_entity import Subject, \
                                                   ExtendedSubjectsModel
from app.models.schools_model_with_entity import School, \
                                                   ExtendedSchoolsModel


class AdminController(object):

    """AdminController - user controller"""

    def __init__(self):
        self.first_model = TeachersModel()
        self.teacher_model = ExtendedTeachersModel()
        self.subject_model = ExtendedSubjectsModel()
        self.school_model = ExtendedSchoolsModel()
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
        self.data = self.teacher_model.get_all_teachers()
        # render page with all users
        return self.view.render_list_users(self.data)

    def user_add(self):
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
                _teacher = self.create_entity_teacher()
                _teacher.name = str(_teacher.name).encode("UTF-8")
                # - save all data in DB
                self.teacher_model.insert_teacher(_teacher)
                # redirect to users list and make status message
                return self.view.add_user_form_success(_teacher.name)

            _errors = self.message
        # render empty user add form
        return self.view.render_user_form(_roles, _errors)

    def remove_user(self, id_):
        """Delete user method"""

        # get user by id
        _user = self.teacher_model.get_teacher_by_id(id_)
        # get name variable for status message
        for fields in _user:
            name = fields.name
        if request.method == 'POST' and request.form['delete_button']:

            # delete user by id
            self.teacher_model.delete_teacher_by_id(id_)

            return self.view.remove_user_form_success(name)

        # TODO:
        # fix cancel button action
        #elif request.method == 'POST' and request.form['cancel_button']:
        #    return self.get_view_all()

        return self.view.render_confirm_delete(name)

    def update_user(self, id_):
        """Update user method"""
        # define variables for sending to template
        _errors = {}

        # get all roles from DB
        _roles = self.first_model.get_all_roles()

        user = self.teacher_model.get_teacher_by_id(id_)
        for field in user:
            data = field

        if request.method == 'POST':
            if self._validate_on_submite(name = request.form['name']
                                        ,login =request.form['login']
                                        ,password = request.form['password']
                                        ,email = request.form['email']
                                        ,user_role =request.form['user_role']
                                        ):

                # create entity
                _teacher = self.create_entity_teacher()
                _teacher.id_ = int(id_)

                self.teacher_model.update_teacher_by_id(_teacher)
                return self.view.add_user_form_success(data.name)

            _errors = self.message
        return self.view.render_user_form(_roles, _errors, data)


    #school CRUD
    #---------------------------------------------------
    def get_view_all_schools(self):
        """return list all school"""
        # get data from db
        self.data = self.school_model.get_all_schools()
        # render page with all schools
        return self.view.render_list_schools(self.data)

    def get_view_add_school(self):
        """add new school"""
        _errors = {}

        if request.method == 'POST':
            _school = self._create_entity_school()
            self.school_model.insert_school(_school)
            return self.view.add_school_form_success(_school.name)

        return self.view.render_school_form(_errors)

    def update_school(self, id_):
        """update school by id"""
        _errors = {}

        _school = self.school_model.get_school_by_id(id_)

        for field in _school:
            data = field
        if request.method == 'POST':
            _school = self._create_entity_school()
            _school.id_ = id_
            school_model.update_school_by_id(_school)

            return self.view.add_school_form_success(_name)

        return self.view.render_school_form(_school, _errors)

    def remove_school(self, id_):
        """delete school by id"""
        _errors = {}
        _school = self._school_model.get_school_by_id(id_)

        for field in _school:
            name = field.name

        if request.method == 'POST':
            _school = self._create_entity_school()
            return self.view.remove_school_form_success(_school.name)

        return self.view.render_confirm_delete(name)


    #---------------------------------------------
    def _create_entity_school(self):
        """entity School"""
        _name = str(request.form['name'])
        _address = str(request.form['address'])

        return School(None, _name, _address)

    def create_entity_teacher(self):
        """entity Teacher"""
        _name = unicode(request.form['name'])
        _login = str(request.form['login'].strip())
        _password = str(request.form['password'].strip())
        _email = str(request.form['email'])
        _role = int(request.form['user_role'])

        # create entity
        return Teacher(None, _name, _login,
                           _password, _email, _role,
                           None, None, None)

    def _validate_on_submite(self, **kwargs):
        """validate request data from form"""
        self.message = dict()
        # regex pattern
        email_pattern = "^[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}$"
        name_pattern = "^([A-Z\p{Cyrillic}])\w\p{Cyrillic}+\s([A-Z{Cyrillic}])\w\p{Cyrillic}+$"
        login_pattern = "^[A-Za-z0-9]+$"
        # check data
        if not kwargs.get('name'):
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