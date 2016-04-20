"""Test Teachers model with entity"""

import unittest
import mock

import app.models.teachers_model_with_entity
from db import credentials


class TestTeachers(unittest.TestCase):
    """This class creates teacher objects to use them in Teacher Model"""

    def test_creation_of_teacher(self):
        """Object teacher is created"""
        teacher = app.models.teachers_model_with_entity.Teacher(1, "name",
                                                                "login",
                                                                "password",
                                                                "email",
                                                                "role_id",
                                                                "role_name",
                                                                "school_id",
                                                                "school_name")
        self.assertIsNotNone(teacher)


class TestTeachersModelWithEntity(unittest.TestCase):
    """This class is used to retrieve data about teachers from DB"""

    def setUp(self):
        """Creates a initial data and records for tests"""
        self.test_teacher_name = u"testTeacherName"
        self.test_teacher_login = u"testTeacherLogin"
        self.test_teacher_email = u"testTeacherEmail"
        self.test_teacher_password = u"testTeacherPassword"
        self.test_teacher_role_id = 1
        self.test_teacher_school_id = 1
        self.test_teacher_role_name = u"testTeacherRoleName"
        self.test_teacher_school_name = u"testTeacherSchoolName"
        self.teacher_model = \
            app.models.teachers_model_with_entity.ExtendedTeachersModel()

        self.test_list = [
            {'id': 1, 'name': u'Name1', 'login': u'Login1',
             'email': u'Email1', 'password': u'Password1',
             'role_id': 1, 'school_id': 1,
             'role_name': u'RoleName1', 'school_name': u'SchoolName1'},
            {'id': 2, 'name': u'Name2', 'login': u'Login2',
             'email': u'Email2', 'password': u'Password2',
             'role_id': 2, 'school_id': 2, 'role_name': u'RoleName2',
             'school_name': u'SchoolName2'}
        ]

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.database = credentials[3]

        self.teacher = app.models.teachers_model_with_entity. \
            Teacher(1,
                    self.test_teacher_name,
                    self.test_teacher_login,
                    self.test_teacher_email,
                    self.test_teacher_password,
                    self.test_teacher_role_id,
                    self.test_teacher_school_id,
                    self.test_teacher_role_name,
                    self.test_teacher_school_name)

    def test_creation_of_ExtendedTeachersModel(self):
        """Basic smoke test: object ExtendedTeacherModel is created"""
        teacher_model = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel()
        self.assertIsNotNone(teacher_model)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_initORM(self, mock_dbdriver):
        """Testing method initORM, check correct call of dbdriver"""
        dbdriver_execute_mock = mock.Mock()
        mock_dbdriver.return_value = dbdriver_execute_mock
        app.models.teachers_model_with_entity.ExtendedTeachersModel.initORM(
            self.teacher_model)
        call = self.host, self.username, self.password, self.database
        dbdriver_execute_mock.connect.assert_called_with(*call)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_get_all_teacher(self, mock_dbdriver):
        """Testing method get_all_teacher, check correct method call
        and whether the results is equal with given in test

        """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        dbdriver_execute_mock.mysql_do.return_value = self.test_list
        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.get_all_teachers(self.teacher_model)
        call_sql = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.select_teachers_query + ' '
        dbdriver_execute_mock.mysql_do.assert_called_with(call_sql)
        self.assertEqual(len(self.test_list), len(result))

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_get_teacher_by_id(self, mock_dbdriver):
        """Testing method get_teacher_by_id, check correct method call
        and whether the results is equal with given in test

        """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        test_list_single = [self.test_list[0], ]
        dbdriver_execute_mock.mysql_do.return_value = test_list_single
        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.get_teacher_by_id(
             self.teacher_model, test_list_single[0]['id'])
        call_sql = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.select_teachers_query + \
            ' WHERE t.id=' + str(test_list_single[0]['id'])
        dbdriver_execute_mock.mysql_do.assert_called_with(call_sql)
        self.assertEqual(len(test_list_single), len(result))

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_get_all_teacher_by_role(self, mock_dbdriver):
        """Testing method get all teachers by given role id"""
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        test_list_single = [self.test_list[0], ]
        dbdriver_execute_mock.mysql_do.return_value = test_list_single
        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.get_all_teachers_by_role(
             self.teacher_model, test_list_single[0]['role_id'])
        call_sql = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.select_teachers_query + \
            ' WHERE role_id=' + str(test_list_single[0]['role_id'])
        dbdriver_execute_mock.mysql_do.assert_called_with(call_sql)
        self.assertEqual(len(test_list_single), len(result))

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_get_all_teachers_by_school(self, mock_dbdriver):
        """Testing method get all teachers by given school_id"""
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        test_list_single = [self.test_list[0], ]
        dbdriver_execute_mock.mysql_do.return_value = test_list_single
        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.get_all_teachers_by_school(
             self.teacher_model, test_list_single[0]['school_id'])
        call_sql = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.select_teachers_query + \
            ' WHERE school_id=' + str(test_list_single[0]['school_id'])
        dbdriver_execute_mock.mysql_do.assert_called_with(call_sql)
        self.assertEqual(len(test_list_single), len(result))

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_insert_teacher(self, mock_dbdriver):
        """Testing method insert_teacher, check correct method call
        and whether the results is None

        """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        test_list_single = [self.test_list[0], ]
        test_teacher = app.models.teachers_model_with_entity.Teacher(
            test_list_single[0]['id'], test_list_single[0]['name'],
            test_list_single[0]['login'], test_list_single[0]['email'],
            test_list_single[0]['password'], test_list_single[0]['role_id'],
            1, 1, 1)

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.insert_teacher(
             self.teacher_model, test_teacher)

        call = 'Teachers', \
               ("name", "login", "email", "password", "role_id", "state"), \
               (test_list_single[0]['name'],
                test_list_single[0]['login'],
                test_list_single[0]['password'],
                test_list_single[0]['email'],
                test_list_single[0]['id'], 1)

        dbdriver_execute_mock.insert.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_delete_teacher_by_id(self, mock_dbdriver):
        """ Testing method delete_teacher_by_id, check correct method call
        and whether the results is None

        """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        test_list_single = [self.test_list[0], ]

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.delete_teacher_by_id(
             self.teacher_model, test_list_single[0]['id'])

        call = 'Teachers', 'id = ' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.delete.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_update_teacher_by_id(self, mock_dbdriver):
        """ Testing method update_teacher_by_id, check correct method call
        and whether the results is None

        """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'

        test_list_single = [self.test_list[0], ]

        test_teacher = app.models.teachers_model_with_entity.Teacher(
            test_list_single[0]['id'], test_list_single[0]['name'],
            test_list_single[0]['login'], test_list_single[0]['password'],
            test_list_single[0]['email'], test_list_single[0]['role_id'],
            test_list_single[0]['school_id'], test_list_single[0]['role_name'],
            test_list_single[0]['school_name'])

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.update_teacher_by_id(
             self.teacher_model, test_teacher)

        call = 'Teachers', \
               'name="' + test_list_single[0]['name'] + \
               '", login="' + test_list_single[0]['login'] + \
               '", email="' + test_list_single[0]['email'] + \
               '",                     password="' + \
               test_list_single[0]['password'] + \
               '", role_id=' + str(test_list_single[0]['role_id']) + \
               '', 'id=' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.update.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_set_role_id_to_teacher_by_id(self, mock_dbdriver):
        """ Testing method set_role_id_to_teacher_by_id"""
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'

        test_list_single = [self.test_list[0], ]

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.set_role_id_to_teacher_by_id(
             self.teacher_model, self.test_teacher_role_id, 1)

        call = 'Teachers', \
               'role_id=' + str(test_list_single[0]['role_id']) + \
               '', 'id=' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.update.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_set_school_id_to_teacher_by_id(self, mock_dbdriver):
        """ Testing method set_role_id_to_teacher_by_id"""
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'

        test_list_single = [self.test_list[0], ]

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.set_school_id_to_teacher_by_id(
             self.teacher_model, self.test_teacher_school_id, 1)

        call = 'Teachers', \
               'school_id=' + str(test_list_single[0]['school_id']) + \
               '', 'id=' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.update.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_set_password_to_teacher_by_id(self, mock_dbdriver):
        """ Testing method set_role_id_to_teacher_by_id"""
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'

        test_list_single = [self.test_list[0], ]
        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.set_password_to_teacher_by_id(
             self.teacher_model, 1, self.test_teacher_password)

        call = 'Teachers', \
               'password=' + str('"testTeacherPassword"') + \
               '', 'id=' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.update.assert_called_with(*call)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
