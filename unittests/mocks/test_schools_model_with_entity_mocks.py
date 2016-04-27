# -*- coding: utf-8 -*-
""" A couple of unit-tests for testing module schools_model_with_entity """

import mock
import unittest

import app.models.schools_model_with_entity
from db import credentials


class TestSchool(unittest.TestCase):

    """ Class with methods, for testing School class """

    def test_creation_of_school(self):
        """ Basic smoke test: object school is created """
        school = app.models.schools_model_with_entity.School(1,
                                                             "name",
                                                             "address")
        self.assertIsNotNone(school)


class TestExtendedSchoolsModel(unittest.TestCase):

    """ Class with methods, for testing ExtendedSchoolModel class """

    def setUp(self):
        """ Fixture that creates a initial data and records for tests """
        self.test_school_name = u"testSchoolName"
        self.test_school_address = u"testSchoolAddress"
        self.school_model = \
            app.models.schools_model_with_entity.ExtendedSchoolsModel()

        self.test_list = [
            {'id': 1, 'name': u'Школа 1', 'address': u'Адреса перша'},
            {'id': 2, 'name': u'Школа 2', 'address': u'Адреса друга'}, ]

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.database = credentials[3]

        self.school = app.models.schools_model_with_entity.\
            School(1,
                   self.test_school_name,
                   self.test_school_address)

    def test_creation_of_ExtendedSchoolsModel(self):
        """ Basic smoke test: object ExtendedSchoolsModel is created """
        school_model = app.models.schools_model_with_entity.\
            ExtendedSchoolsModel()

        self.assertIsNotNone(school_model)

    @mock.patch('app.models.schools_model_with_entity.DBDriver')
    def test_initORM(self, mock_dbdriver):
        """ Testing method initORM, check correct call of dbdriver """
        dbdriver_execute_mock = mock.Mock()

        mock_dbdriver.return_value = dbdriver_execute_mock
        app.models.schools_model_with_entity.ExtendedSchoolsModel.initORM(
            self.school_model)

        call = self.host, self.username, self.password, self.database
        dbdriver_execute_mock.connect.assert_called_with(*call)

    @mock.patch('app.models.schools_model_with_entity.DBDriver')
    def test_get_all_schools(self, mock_dbdriver):
        """ Testing method get_all_schools, check correct method call
        and whether the results is equal with given in test """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'results'
        dbdriver_execute_mock.mysql_do.return_value = self.test_list
        mock_dbdriver.return_value = dbdriver_execute_mock

        result = app.models.schools_model_with_entity.\
            ExtendedSchoolsModel.get_all_schools(
                self.school_model)

        call_sql = app.models.schools_model_with_entity.\
                       ExtendedSchoolsModel.select_schools_query + ' '

        dbdriver_execute_mock.mysql_do.assert_called_with(call_sql)

        for school_object in result:
            for school_dict in self.test_list:
                if school_dict['id'] == school_object.id_ \
                        and school_dict['name'] == school_object.name \
                        and school_dict['address'] == school_object.address:
                    self.test_list.remove(school_dict)
        self.assertEqual(len(self.test_list), 0)

    @mock.patch('app.models.schools_model_with_entity.DBDriver')
    def test_get_school_by_id(self, mock_dbdriver):
        """ Testing method get_school_by_id, check correct method call
        and whether the results is equal with given in test """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'results'
        test_list_single = [self.test_list[0], ]

        dbdriver_execute_mock.mysql_do.return_value = test_list_single
        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.schools_model_with_entity.\
            ExtendedSchoolsModel.get_school_by_id(
                self.school_model, test_list_single[0]['id'])

        call_sql = app.models.schools_model_with_entity.\
                       ExtendedSchoolsModel.select_schools_query + \
                        ' WHERE id=' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.mysql_do.assert_called_with(call_sql)

        for school_object in result:
            for school_dict in test_list_single:
                if school_dict['id'] == school_object.id_ \
                        and school_dict['name'] == school_object.name \
                        and school_dict['address'] == school_object.address:
                    test_list_single.remove(school_dict)
        self.assertEqual(len(test_list_single), 0)

    @mock.patch('app.models.schools_model_with_entity.DBDriver')
    def test_insert_school(self, mock_dbdriver):
        """ Testing method insert_school, check correct method call
        and whether the results is None """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'results'
        test_list_single = [self.test_list[0], ]

        test_school = app.models.schools_model_with_entity.School(
            test_list_single[0]['id'],
            test_list_single[0]['name'],
            test_list_single[0]['address'])

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.schools_model_with_entity.\
            ExtendedSchoolsModel.insert_school(
                self.school_model, test_school)

        call = 'Schools', \
               ('name', 'address', 'state'), \
               (test_list_single[0]['name'], test_list_single[0]['address'], 1)

        dbdriver_execute_mock.insert.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.schools_model_with_entity.DBDriver')
    def test_delete_school_by_id(self, mock_dbdriver):
        """ Testing method delete_school_by_id, check correct method call
        and whether the results is None """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'results'
        test_list_single = [self.test_list[0], ]

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.schools_model_with_entity.\
            ExtendedSchoolsModel.delete_school_by_id(
                self.school_model, test_list_single[0]['id'])

        call = 'Schools', 'id = ' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.delete.assert_called_with(*call)
        self.assertIsNone(result)

    @mock.patch('app.models.schools_model_with_entity.DBDriver')
    def test_update_school_by_id(self, mock_dbdriver):
        """ Testing method update_school_by_id, check correct method call
        and whether the results is None """
        dbdriver_execute_mock = mock.Mock()
        dbdriver_execute_mock.name = 'results'

        test_list_single = [self.test_list[0], ]

        test_school = app.models.schools_model_with_entity.School(
            test_list_single[0]['id'],
            test_list_single[0]['name'],
            test_list_single[0]['address'])

        mock_dbdriver.return_value = dbdriver_execute_mock
        result = app.models.schools_model_with_entity.\
            ExtendedSchoolsModel.update_school_by_id(
                self.school_model, test_school)

        call = 'Schools', \
               'name="' + test_list_single[0]['name'] + \
               '", address="' + test_list_single[0]['address'] + \
               '"', 'id=' + str(test_list_single[0]['id'])

        dbdriver_execute_mock.update.assert_called_with(*call)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main(verbosity=2)
