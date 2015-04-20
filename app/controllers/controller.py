#!/usr/bin/env python

from app.models import AdminModel


class AdminController(object):

    """docstring for AdminController"""

    def __init__(self):
        self.model = AdminModel()
        self.view = View()

    def validate_on_submite(self, **kwargs):
        """correct = true else false"""
        self.message = dict()
        # regex pattern
        email_pattern = """^[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}$"""
        # check data
        if not kwargs.get('name'):
            self.message['name'] = 'Invalid name'
        if not kwargs.get('role'):
            self.message['role'] = 'Invalid role'
        if not kwargs.get('password'):
            self.message['password'] = 'Invalid password'
        if not kwargs.get('login'):
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
    
    def get_index():
        """return index.html"""
        return self.view.render_index()

    def get_error404():
        """error 404"""
        return self.view.render_error()

    def get_view_add_get(self):
        """view => user_add.html get"""
        return self.view.add()
    
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

    def get_view_all():
        """view => user_add.html get"""
        #get data from db
        self.data = self.model.get_all()
        #render page with all users
        return self.view.render_list_users(self.data)

