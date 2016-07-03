import unittest
import requester
import MySQLdb
import sys
import os
sys.path.insert(0,
                os.path.dirname(os.path.dirname
                                (os.path.abspath(__file__))))
from config import credentials, USERNAME, PASSWORD
from app import DBDriver


class TestApp(unittest.TestCase):

    """This class provides client testing positive and negative"""

    def setUp(self):
        self.client = requester.RequestGenerator(5000)
        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.db = credentials[3]
        self.dbh = MySQLdb.connect(self.host, self.username, self.password,
                                   self.db, use_unicode=True, charset='utf8')
        self.cursor = self.dbh.cursor(MySQLdb.cursors.DictCursor)

        self.orm = DBDriver()
        self.orm.connect(self.host, self.username, self.password, self.db)

        # Getting existing role from DB
        self.existing_roles = self.orm.mysql_do("SELECT * FROM {0}.roles".
                                                format(self.db))

        # Add test records to our DB to test CRUD on them
        self.test_school = {
            'id': None,
            'name': 'Test School Name',
            'address': 'Rivne city, Uvileina street, 57'
        }
        sql = "INSERT INTO {0}.schools (id, name, address)" \
              "VALUES(null, '{1}', '{2}')"\
            .format(self.db,
                    self.test_school['name'], self.test_school['address'])

        try:
            self.cursor.execute(sql)
            self.dbh.commit()
            self.test_school['id'] = int(self.cursor.lastrowid)
        except MySQLdb.MySQLError as err:
            print(err.message)
            # Rollback in case there is any error
            self.db.rollback()
            exit("Error while trying to add test school to DB")

        self.test_user = {
            'id': None,
            'name': 'Test User Name',
            'login': 'user1000000',
            'password': '111',
            'email': 'psv.work@mail.ru',
            'user_role': int(self.existing_roles[0]['id']),
            'go': ''
        }
        sql = "INSERT INTO {0}.Teachers (school_id, id, name, role_id," \
              "login, email, password)" \
              "VALUES ('{1}', null, '{2}', '{3}', '{4}', '{5}', '{6}')"\
            .format(self.db, self.test_school['id'], self.test_user['name'],
                    self.existing_roles[0]['id'],
                    self.test_user['login'], self.test_user['email'],
                    self.test_user['password'])

        try:
            self.cursor.execute(sql)
            self.dbh.commit()
            self.test_user['id'] = int(self.cursor.lastrowid)
        except MySQLdb.MySQLError as err:
            print(err.message)
            # Rollback in case there is any error
            self.db.rollback()
            exit("Error while trying to add test teacher to DB")

    def tearDown(self):
        """Clear all test data from DB"""
        self.orm.mysql_do("DELETE FROM {0}.Teachers WHERE "
                          "id = {1}".format(self.db,
                                            self.test_user['id']))
        self.orm.mysql_do("DELETE FROM {0}.Schools WHERE "
                          "id = {1}".format(self.db,
                                            self.test_school['id']))
        self.orm.close()
        self.dbh.close()

    def test_login_correct(self):
        """Test white login (with correct login data)"""
        response = self.client.login()
        self.assertFalse('form-signin' in response.content and
                         response.status_code == 200)

    def test_login_fail(self):
        """Test login with wrong login password"""
        response = self.client.login(user='wrongUserName')
        self.assertTrue('form-signin' in response.content and
                        response.status_code == 200)

    def test_login_fail_sql_injection(self):
        """Test login with SQL injection"""
        response = self.client.login(user="'' or 1=1", password="'' or 1=1")
        self.assertTrue('form-signin' in response.content and
                        response.status_code == 200)

    def test_logout(self):
        """Check whether the application deletes cookie 'session'"""
        response = self.client.logout()
        self.assertTrue('session' not in response.cookies)

    # --------------------------------------------------
    # teacher CRUD
    # --------------------------------------------------
    def test_get_all_users_as_logged_in(self):
        """Positive test on getting the list of users as logged in user"""
        response = self.client.get_users_list()
        users_in_db = self.orm.mysql_do("SELECT * FROM {0}.teachers".
                                        format(self.db))
        self.assertEqual(str(response.content).count('<tr>')-1,
                         len(users_in_db))

    def test_get_all_users_as_logged_out(self):
        """Negative test on getting the list of users as logged out user
        Application have to redirect on login page"""
        response = self.client.get_users_list(as_logged_in=False)
        self.assertTrue(response.status_code == 302 and
                        response.headers['location'] == self.client.url_login)

    def test_add_user_as_logged_in_with_correct_data(self):
        """Trying to add new user with correct data"""
        users_in_db_before = self.orm.mysql_do("SELECT * FROM {0}.teachers".
                                               format(self.db))
        response = self.client.add_user(self.test_user)

        if response.status_code == 302\
                and response.headers['location'] == self.client.url_users_list:
                    users_in_db_after = self.orm.mysql_do(
                        "SELECT * FROM {0}.teachers".format(self.db))
                    self.assertNotEqual(len(users_in_db_before),
                                        len(users_in_db_after),
                                        "Application doesn't actually " +
                                        "add new user to the DB")
        else:
            self.assertEqual(
                response.status_code,
                302, "Application doesn't add new user with correct data")

    def test_add_user_as_logged_in_with_wrong_data(self):
        """Check correct validation on user update"""
        users_in_db_before = self.orm.mysql_do(
            "SELECT * FROM {0}.teachers".format(self.db))
        # change our test user so he'd have 2 wrong fields
        self.test_user['name'] = ''
        self.test_user['email'] = 'user1000.mail.com'
        response = self.client.add_user(self.test_user)

        if response.status_code == 200:
            users_in_db_after = self.orm.mysql_do(
                "SELECT * FROM {0}.teachers".format(self.db))
            self.assertTrue(
                len(users_in_db_before) == len(users_in_db_after) and
                str(response.content).count('has-error') == 2)
        else:
            self.assertEqual(
                response.status_code, 302,
                "Application doesn't add new user with correct data")

    def test_add_user_as_logged_out(self):
        """Check whether the application let unauthorisez users to add user"""
        users_in_db_before = self.orm.mysql_do(
            "SELECT * FROM {0}.teachers".format(self.db))
        response = self.client.add_user(self.test_user, as_logged_in=False)

        if response.status_code == 302 and\
                response.headers['location'] == self.client.url_login:
            users_in_db_after = self.orm.mysql_do(
                "SELECT * FROM {0}.teachers".format(self.db))
            self.assertEqual(len(users_in_db_before), len(users_in_db_after))
        else:
            self.assertEqual(
                response.status_code, 302,
                "Application allows to add new Teacher for unauthorized user")

    def test_update_user_by_correct_id_with_correct_data_as_logged_in_user(
            self):
        """Check whether the application updates user data
        with correct data"""
        # change some data in our test user
        self.test_user['name'] = 'New Test Name'
        response = self.client.update_user(self.test_user)
        if response.status_code == 302:
            query = self.orm.mysql_do("SELECT * FROM {0}.Teachers WHERE "
                                      "id = {1} AND name = '{2}'".
                                      format(self.db,
                                             self.test_user['id'],
                                             self.test_user['name']))
            self.assertTrue(len(query) == 1,
                            "Application doesn't actually updates "
                            "correct user data!")
        else:
            self.assertTrue(response.status_code == 302,
                            "Application doesn't update user data with "
                            "correct id")

    def test_update_user_by_correct_id_with_wrong_data_as_logged_in_user(
            self):
        """Check whether the application updates user data
        with wrong data"""
        # change some data in our test user
        self.test_user['email'] = 'user1000.mail.com'
        response = self.client.update_user(self.test_user)
        if response.status_code == 200:
            query = self.orm.mysql_do("SELECT * FROM {0}.Teachers WHERE "
                                      "id = {1} AND email = '{2}'".
                                      format(self.db,
                                             self.test_user['id'],
                                             self.test_user['email']))
            self.assertTrue(len(query) == 0,
                            "Application allow to update user "
                            "with uncorrect user data!")
        else:
            self.assertTrue(response.status_code == 200,
                            "Application allow to update user "
                            "with uncorrect user data!")

    def test_update_user_by_wrong_id_as_logged_in_user(self):
        """Test whether the application handle the exception
        of wrong id while updating user and redirects to page 404"""
        self.test_user['id'] = 99999
        response = self.client.update_user(self.test_user)
        self.assertEqual(response.status_code, 404,
                         "Application doesn't handle "
                         "wrong user id exception while user update")

    def test_update_user_by_id_as_logged_out_user(self):
        """Check whether the application lets for
        unauthorised user to update user data"""
        self.test_user['name'] = 'New Test Name'
        response = self.client.update_user(user=self.test_user,
                                           as_logged_in=False)
        query = self.orm.mysql_do("SELECT * FROM {0}.teachers "
                                  "WHERE id = {1} AND name = "
                                  "'{2}'".
                                  format(self.db,
                                         self.test_user['id'],
                                         self.test_user['name']))
        self.assertTrue(response.status_code == 302 and
                        response.headers['location'] ==
                        self.client.url_login and
                        len(query) == 0)

    def test_delete_user_by_correct_id_as_logged_in_user(self):
        """Check whether the application deletes user by if from DB"""
        users_in_db_before = self.orm.mysql_do("SELECT * FROM {0}.teachers".
                                               format(self.db))
        response = self.client.delete_user(self.test_user)
        users_in_db_after = self.orm.mysql_do("SELECT * FROM {0}.teachers".
                                              format(self.db))
        self.assertTrue(response.status_code == 302 and
                        len(users_in_db_before) > len(users_in_db_after),
                        "Application doesn't actually delete user from DB!")

    def test_delete_user_by_wrong_id_as_logged_in_user(self):
        """Test whether the application handle the exception
        of wrong id while deleting user and redirects to page 404"""
        self.test_user['id'] = 99999
        response = self.client.delete_user(self.test_user)
        self.assertEqual(response.status_code, 404,
                         "Application doesn't handle "
                         "wrong user id exception while user delete")

    def test_delete_user_by_id_as_logged_out_user(self):
        """Check whether the application lets for
        unauthorised user to update user data"""
        response = self.client.delete_user(self.test_user, as_logged_in=False)
        self.assertTrue(response.status_code == 302 and
                        response.headers['location'] == self.client.url_login,
                        "Application let unauthorized user to delete users!")
