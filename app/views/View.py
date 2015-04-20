#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, flash


class View(object):

    """This class is used to render templates"""

    def render_index(self):
        """Render home page"""
        return render_template('index.html')

    def render_error(self):
        """Render 404 page"""
        return render_template('page_not_found.html')

    def add_user_ok(self, name):
        """Render successfull user adding"""
        # display message on the users list page
        flash('%s was successfully added to database') % name
        return redirect('users_list.html')

    def add_user_err(self, **kwargs):
        """Render adding user error"""
        _data = kwargs
        return render_template('user_add.html', errors=_data)

    def render_list_users(self, **kwargs):
        """Render users list"""
        _data = kwargs
        return render_template('users_list.html', users=_data)
