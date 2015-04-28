#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from flask import request

from app.views.view import View
from app.models.roles_model import RolesModel
from app.models.teachers_model_with_entity import Teacher,\
    ExtendedTeachersModel
from app.models.subjects_model_with_entity import Subject, \
    ExtendedSubjectsModel
from app.models.schools_model_with_entity import School, \
    ExtendedSchoolsModel
from app.utils.validation import Validate


class AdminController(object):

    """This class receives user requests, takes data from models and sends it
       to the view"""

    def __init__(self):
        self.role_model = RolesModel()
        self.teacher_model = ExtendedTeachersModel()
        self.subject_model = ExtendedSubjectsModel()
        self.school_model = ExtendedSchoolsModel()
        self.view = View()
        self.validate = Validate()

    def get_index(self):
        """Return home page"""

        return self.view.render_index()

    def get_login(self, error):
        """Return login page"""

        return self.view.render_login(error=error)

    def get_error404(self):
        """Return error page"""

        return self.view.render_error()

    #--------------------------------------------------
    # teacher CRUD
    #--------------------------------------------------
    def list_all_users(self):
        """Get all teachers from db and return teachers list page"""

        # get data from db
        _data = self.teacher_model.get_all_teachers()
        # render page with all users
        return self.view.render_list_users(_data)

    def add_user(self):
        """Validate data and add teacher to db"""

        # define variables for sending to template
        _errors = {}

        # get all roles from DB
        _roles = self.role_model.get_all_roles()

        if request.method == 'POST':
            # save user in case there aren't any mistakes
            if self._validate_teachers(name=request.form['name'],
                                       login=request.form['login'],
                                       password=request.form['password'],
                                       email=request.form['email'],
                                       user_role=request.form['user_role']):
                # create entity
                _teacher = self._create_entity_teacher()
                #_teacher.name = str(_teacher.name).encode("UTF-8")
                # save all data in DB
                self.teacher_model.insert_teacher(_teacher)
                # redirect to users list and make status message
                return self.view.add_user_form_success(_teacher.name)

            _errors = self.message
        # render empty user add form
        return self.view.render_user_form(_roles, _errors)

    def update_user(self, id_):
        """Update user in db"""

        # define variables for sending to template
        _errors = {}

        # get all roles from DB
        _roles = self.role_model.get_all_roles()

        _user = self.teacher_model.get_teacher_by_id(id_)
        for field in _user:
            _data = field

        if request.method == 'POST':
            # save user in case there aren't any mistakes
            if self._validate_teachers(name=request.form['name'],
                                       login=request.form['login'],
                                       password=request.form['password'],
                                       email=request.form['email'],
                                       user_role=request.form['user_role']):

                # create entity
                _teacher = self._create_entity_teacher()
                _teacher.id_ = int(id_)
                # update all data in DB
                self.teacher_model.update_teacher_by_id(_teacher)
                # redirect to users list and make status message
                return self.view.add_user_form_success(_teacher.name)

            _errors = self.message
        return self.view.render_user_form(_roles, _errors, _data)

    def remove_user(self, id_):
        """Delete user from db"""

        # get user by id
        _user = self.teacher_model.get_teacher_by_id(id_)
        # get name variable for status message
        for fields in _user:
            _name = fields.name
        if request.method == 'POST' and request.form['delete_button']:

            # delete user by id
            self.teacher_model.delete_teacher_by_id(id_)

            return self.view.remove_user_form_success(_name)

        # TODO:
        # fix cancel button action
        # elif request.method == 'POST' and request.form['cancel_button']:
        #    return self.list_all_users()

        return self.view.render_confirm_delete(_name)
    #--------------------------------------------------

    #--------------------------------------------------
    # school CRUD
    #---------------------------------------------------
    def list_all_schools(self):
        """Get all schools from db and return schools list page"""

        # get data from db
        _data = self.school_model.get_all_schools()
        # render page with all schools
        return self.view.render_list_schools(_data)

    def add_school(self):
        """Add new school to db"""

        _errors = {}

        if request.method == 'POST':
            # save school in case there aren't any mistakes
            if self._validate_schools(name=request.form['name'].strip(),
                                      address=request.form['address'].strip()):
                # create entity
                _school = self._create_entity_school()
                # save all data in DB
                self.school_model.insert_school(_school)
                # redirect to schools list and make status message
                return self.view.add_school_form_success(_school.name)

            _errors = self.message
        # render empty school add form
        return self.view.render_school_form(_errors)

    def update_school(self, id_):
        """Update school in db"""

        _errors = {}

        _school = self.school_model.get_school_by_id(id_)

        for field in _school:
            _data = field

        if request.method == 'POST':
            # save school in case there aren't any mistakes
            if self._validate_schools(name=request.form['name'].strip(),
                                      address=request.form['address'].strip()):
                # create entity
                _school = self._create_entity_school()
                _school.id_ = int(id_)
                # update all data in DB
                self.school_model.update_school_by_id(_school)
                # redirect to schools list and make status message
                return self.view.add_school_form_success(_school.name)

            _errors = self.message
        return self.view.render_school_form(_errors, _data)

    def remove_school(self, id_):
        """Delete school from db"""

        _school = self.school_model.get_school_by_id(id_)

        for field in _school:
            _name = field.name

        if request.method == 'POST':

            # delete school by id
            self.school_model.delete_school_by_id(id_)
            return self.view.remove_school_form_success(_name)

        return self.view.render_confirm_delete(_name)
    #---------------------------------------------

    #---------------------------------------------
    # subject CRUD
    #---------------------------------------------
    def list_all_subjects(self):
        """Get all subjects from db and return subjects list page"""

        # get data from db
        _data = self.subject_model.get_all_subjects()

        # render page with all subjects
        return self.view.render_list_subjects(_data)

    def add_subject(self):
        """Add new subject to db"""

        _errors = {}

        if request.method == 'POST':
            # save subject in case there aren't any mistakes
            if self._validate_subjects(name=request.form['name'].strip()):
                # create entity
                _subject = self._create_entity_subject()
                # save all data in DB
                self.subject_model.insert_subject(_subject)
                # redirect to subjects list and make status message
                return self.view.add_subject_form_success(_subject.name)

            _errors = self.message
        # render empty subject add form
        return self.view.render_subject_form(_errors)

    def update_subject(self, id_):
        """Update subject in db"""

        _errors = {}

        _subject = self.subject_model.get_subject_by_id(id_)

        for field in _subject:
            _data = field

        if request.method == 'POST':
            # save subject in case there aren't any mistakes
            if self._validate_subjects(name=request.form['name'].strip()):
                # create entity
                _subject = self._create_entity_subject()
                _subject.id_ = int(id_)
                # save all data in DB
                self.subject_model.update_subject_by_id(_subject)
                # redirect to subjects list and make status message
                return self.view.add_subject_form_success(_subject.name)

            _errors = self.message
        return self.view.render_subject_form(_errors, _data)

    def remove_subject(self, id_):
        """Delete subject from db"""

        _subject = self.subject_model.get_subject_by_id(id_)

        for field in _subject:
            _name = field.name

        if request.method == 'POST':

            # delete subject by id
            self.subject_model.delete_subject_by_id(id_)
            return self.view.remove_subject_form_success(_name)

        return self.view.render_confirm_delete(_name)
    #---------------------------------------------

    def _create_entity_teacher(self):
        """Create Teacher entity"""

        _name = request.form['name'].strip().encode('utf-8')
        _login = str(request.form['login'].strip())
        _password = str(request.form['password'].strip())
        _email = str(request.form['email'])
        _role = int(request.form['user_role'])
        # create entity
        return Teacher(None, _name, _login,
                       _password, _email, _role,
                       None, None, None)

    def _create_entity_school(self):
        """Create School entity"""

        _name = request.form['name'].strip().encode('utf-8')
        _address = request.form['address'].strip().encode('utf-8')
        # create entity
        return School(None, _name, _address)

    def _create_entity_subject(self):
        """Create Subject entity"""

        _name = request.form['name'].strip().encode('utf-8')
        # create entity
        return Subject(None, _name)

    def _validate_teachers(self, **kwargs):
        """Validate request teacher's data from form"""

        self.message = dict()
        # check data
        if not kwargs.get('name'):
            self.message['name'] = u'Некоректно введно ім\'я'

        if not kwargs.get('user_role'):
            self.message['user_role'] = u'Виберіть роль'

        if not kwargs.get('password'):
            self.message['password'] = u'Введіть пароль'

        if not self.validate.check_login(kwargs.get('login')):
            self.message['login'] = u'Некоректно введно логін'

        if not self.validate.check_email(kwargs.get('email')):
            self.message['email'] = u'Некоректно введно емейл'
        # If validate return true
        if self.message:
            return False
        else:
            return True

    def _validate_schools(self, **kwargs):
        """Validate request school's data from form"""

        self.message = dict()
        # check data
        if not self.validate.check_cyrillic(kwargs.get('name')):
            self.message['name'] = u'Некоректно введено назву'

        if not self.validate.check_cyrillic(kwargs.get('address')):
            self.message['address'] = u'Некоректно введено адресу'

        # If validate return true
        if self.message:
            return False
        else:
            return True

    def _validate_subjects(self, **kwargs):
        """Validate request subject's data from form"""

        self.message = dict()
        # check data
        if not self.validate.check_cyrillic(kwargs.get('name')):
            self.message['name'] = u'Некоректно введено назву'

        # If validate return true
        if self.message:
            return False
        else:
            return True
