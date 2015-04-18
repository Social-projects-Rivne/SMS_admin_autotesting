# -*- coding: utf-8 -*-

from flask import render_template

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main Page')


@app.route('/users_list')
def users_list():
    context = {}

    return render_template('users_list.html', context=context)


@app.route('/user_add', methods=['GET', 'POST'])
def user_add():
    roles = {}
    errors = {}

    return render_template('user_add.html', roles=roles, errors=errors)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404