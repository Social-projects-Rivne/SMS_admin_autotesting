"""Test Teachers model with entity"""

import unittest
import mockcd
import app.models.teachers_model_with_entity
from db import credentials

class TestTeachers(unittest.TestCase):
    """This class creates teacher objects to use them in Teacher Model"""

    def test_creation_of_teacher(self):
        """Object teacher is created"""
        teacher = app.models.teachers_model_with_entity.Teacher(1, "name", "login", "password", "email", "role_id",
                          "role_name", "school_id", "school_name")
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
        self.teacher_model = app.models.teachers_model_with_entity.ExtendedTeachersModel()

        self.test_list = [
            {'id': 1, 'name': u'testTeacherName', 'login': u'testTeacherLogin', 'email': u'testTeacherEmail',
             'password': u'testTeacherPassword', 'role_id': 1, 'school_id': 1, 'role_name': u'testTeacherRoleName',
             'school_name': u'testTeacherSchoolName'}]

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.database = credentials[3]

        self.teacher = app.models.teachers_model_with_entity.Teacher(1, self.test_teacher_name,
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
        """ Testing method initORM, check correct call of dbdriver """
        dbdriver_execute_mock = mock.Mock()

        mock_dbdriver.return_value = dbdriver_execute_mock
        app.models.teachers_model_with_entity.ExtendedTeachersModel.initORM(
            self.teacher_model)

        call = self.host, self.username, self.password, self.database
        dbdriver_execute_mock.connect.assert_called_with(*call)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_get_all_teacher(self, mock_dbdriver):
        """Testing method get_all_teacher, check correct method call
        and whether the results is equal with given in test"""

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
        for teacher_object in result:
            for teacher_dict in self.test_list:
                if teacher_dict['id'] == teacher_object.id_ \
                        and teacher_dict['name'] == teacher_object.name \
                        and teacher_dict['login'] == teacher_object.address \
                        and teacher_dict['email'] == teacher_object.address \
                        and teacher_dict['password'] == teacher_object.address \
                        and teacher_dict['role_id'] == teacher_object.address \
                        and teacher_dict['school_id'] == teacher_object.address \
                        and teacher_dict['role_name'] == teacher_object.address \
                        and teacher_dict['school_name'] == teacher_object.address:
                    self.test_list.remove(teacher_dict)
        self.assertEqual(len(self.test_list), 0)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_get_teacher_by_id(self, mock_dbdriver):
        """Testing method get_teacher_by_id, check correct method call
        and whether the results is equal with given in test"""

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
                   ' WHERE id=' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.mysql_do.assert_called_with(call_sql)

        self.assertEqual(len(test_list_single), len(result))
        for teacher_object in result:
            for teacher_dict in test_list_single:
                if teacher_dict['id'] == teacher_object.id_ \
                        and teacher_dict['name'] == teacher_object.name \
                        and teacher_dict['login'] == teacher_object.address \
                        and teacher_dict['email'] == teacher_object.address \
                        and teacher_dict['password'] == teacher_object.address \
                        and teacher_dict['role_id'] == teacher_object.address \
                        and teacher_dict['school_id'] == teacher_object.address \
                        and teacher_dict['role_name'] == teacher_object.address \
                        and teacher_dict['school_name'] == teacher_object.address:
                    test_list_single.remove(teacher_dict)
        self.assertEqual(len(test_list_single), 0)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_insert_teacher(self, mock_dbdriver):
        """Testing method insert_teacher, check correct method call
        and whether the results is None """

        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        test_list_single = [self.test_list[0], ]

        test_teacher = app.models.teachers_model_with_entity.Teacher(
            test_list_single[0]['id'], test_list_single[0]['name'], test_list_single[0]['login'],
            test_list_single[0]['email'], test_list_single[0]['password'], test_list_single[0]['role_id'],
            test_list_single[0]['school_id'], test_list_single[0]['role_name'], test_list_single[0]['school_name'])

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.insert_teacher(
            self.teacher_model, test_teacher)

        call = 'Teacher', \
               ("name", "login", "password", "email", "role_id",
                "role_name", "school_id", "school_name"), \
               (test_list_single[0]['id'], test_list_single[0]['name'], test_list_single[0]['login'],
                test_list_single[0]['email'], test_list_single[0]['password'], test_list_single[0]['role_id'],
                test_list_single[0]['school_id'], test_list_single[0]['role_name'], test_list_single[0]['school_name'],
                1)

        dbdriver_execute_mock.insert.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_delete_teacher_by_id(self, mock_dbdriver):
        """ Testing method delete_teacher_by_id, check correct method call
        and whether the results is None """

        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'
        test_list_single = [self.test_list[0], ]

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.delete_teacher_by_id(
            self.teacher_model, test_list_single[0]['id'])

        call = 'Teacher', 'id = ' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.delete.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.teachers_model_with_entity.DBDriver')
    def test_update_teacher_by_id(self, mock_dbdriver):
        """ Testing method update_teacher_by_id, check correct method call
        and whether the results is None """

        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'sql_results'

        test_list_single = [self.test_list[0], ]

        test_teacher = app.models.teachers_model_with_entity.Teacher(
            test_list_single[0]['id'], test_list_single[0]['name'], test_list_single[0]['login'],
            test_list_single[0]['email'], test_list_single[0]['password'], test_list_single[0]['role_id'],
            test_list_single[0]['school_id'], test_list_single[0]['role_name'], test_list_single[0]['school_name'])

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.teachers_model_with_entity. \
            ExtendedTeachersModel.update_teacher_by_id(
            self.teacher_model, test_teacher)

        call = 'Teacher', \
               'name="' + test_list_single[0]['name'] + \
               '", address="' + test_list_single[0]['address'] + \
               '", login="' + test_list_single[0]['login'] + \
               '", email="' + test_list_single[0]['email'] + \
               '", password="' + test_list_single[0]['password'] + \
               '", role_id="' + str(test_list_single[0]['role_id']) + \
               '", school_id="' + str(test_list_single[0]['school_id']) + \
               '", role_name="' + test_list_single[0]['role_name'] + \
               '", school_name="' + test_list_single[0]['school_name'] + \
               '"', 'id=' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.update.assert_called_with(*call)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

