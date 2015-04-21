#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, flash, url_for


class View(object):

    """This class is used to render templates"""

    def render_index(self):
        """Render home page"""

        return render_template('index.html')

    def render_error(self):
        """Render 404 page"""

        return render_template('page_not_found.html')

    def render_add_user_form(self, roles, errors):
        """Render user add page"""

        return render_template('user_add.html', roles=roles, errors=errors)

    def add_user_form_success(self, name):
        """Render successfull user adding"""

        # display message on the users list page
        flash(u'%s був успішно доданий до БД' % name)
        return redirect(url_for('users_list'))

    def render_confirm_delete(self):
        """Returns confirm delete page"""

        return render_template('confirm_delete.html')

    def remove_user_form_success(self, name):
        """Render successfull user delete"""

        # display message on the users list page
        flash(u'%s був успішно видалений з БД' % name)
        return redirect(url_for('users_list'))

    def render_list_users(self, data):
        """Render users list"""

        return render_template('users_list.html', users=data)
