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

        return render_template('page_not_found.html'), 404

    def render_user_form(self, roles, errors, user=''):
        """Render user add page"""

        return render_template('user_add.html', roles=roles,\
                               errors=errors, user=user)

    def add_user_form_success(self, name):
        """Render successfull user adding"""

        # display message on the users list page
        flash(u'%s був успішно внесений в БД' % name)
        return redirect(url_for('users_list'))

    def render_confirm_delete(self, name=''):
        """Returns confirm delete page"""

        return render_template('confirm_delete.html', name=name)

    def remove_user_form_success(self, name):
        """Render successfull user delete"""

        # display message on the users list page
        flash(u'%s був успішно видалений з БД' % name)
        return redirect(url_for('users_list'))

    def render_list_users(self, data):
        """Render users list"""

        return render_template('users_list.html', users=data)

    #---View for schools----

    def render_list_schools(self, data):
        """Render schools list"""

        return render_template('schools_list.html', schools=data)

    def render_school_form(self, errors, school=''):
        """Render school add page"""

        return render_template('school_add.html', errors=errors, school=school)

    def add_school_form_success(self, name):
        """Render successfull school adding"""

        # display message on the schools list page
        flash(u'%s була успішно внесена в БД' % name)
        return redirect(url_for('schools_list'))

    def remove_school_form_success(self, name):
        """Render successfull school delete"""

        # display message on the schools list page
        flash(u'%s було успішно видалено з БД' % name)
        return redirect(url_for('schools_list'))

    #---View for subjects----

    def render_list_subjects(self, data):
        """Render subjects list"""

        return render_template('subject_list.html', subjects=data)

    def render_subject_form(self, errors, subject=''):
        """Render subject add page"""

        return render_template('subject_add.html', errors=errors,\
                               subject=subject)

    def add_subject_form_success(self, name):
        """Render successfull subject adding"""

        flash(u'%s був успішно внесена в БД'% name)
        return redirect(url_for('subjects_list'))

    def remove_subject_form_success(self, name):
        """Render successfull subject delete"""

        # display message on the schools list page
        flash(u'%s був успішно видалена з БД' % name)
        return redirect(url_for('subjects_list'))
