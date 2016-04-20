import unittest
import mock

import sys
import os
sys.path.insert(0,
                os.path.dirname(os.path.dirname
                                (os.path.abspath
                                 (__file__))))
import app.models.subjects_model_with_entity
from app.utils.dbdriver import DBDriver
from db import credentials


class TestSubject(unittest.TestCase):

    """Smoke test for creation of class instance"""

    def test_creation_of_subject(self):
        """Basic method to create subject"""
        subject = app.models.subjects_model_with_entity.Subject(2,
                                                                'TestSubject')
        self.assertIsNotNone(subject)


class TestExtendedSubjectsModel(unittest.TestCase):

    """This class makes unit tests for specific
    classes Subject -> ExtendedSubjectsModel"""

    def __create_patch(self, name):
        """Simple method to create patch methods for mock"""
        patcher = mock.patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def setUp(self):
        """Fixture that creates an initial data and records for tests"""
        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.database = credentials[3]

        self.test_subject = app.models.subjects_model_with_entity \
            .Subject(1, 'Math')
        self.subject_model = app.models.subjects_model_with_entity \
            .ExtendedSubjectsModel()
        self.wrong_id = 9999999999999999

        patcher = mock._patch_object(DBDriver, 'connect')
        self.addCleanup(patcher.stop)
        self.mock_dbdriver_connect = patcher.start()

        patcher = mock._patch_object(DBDriver, 'mysql_do')
        self.addCleanup(patcher.stop)
        self.mock_dbdriver_mysql_do = patcher.start()

        patcher = mock._patch_object(DBDriver, 'update')
        self.addCleanup(patcher.stop)
        self.mock_dbdriver_update = patcher.start()

        patcher = mock._patch_object(DBDriver, 'insert')
        self.addCleanup(patcher.stop)
        self.mock_dbdriver_insert = patcher.start()

        patcher = mock._patch_object(DBDriver, 'delete')
        self.addCleanup(patcher.stop)
        self.mock_dbdriver_delete = patcher.start()

        patcher = mock._patch_object(DBDriver, 'close')
        self.addCleanup(patcher.stop)
        self.mock_dbdriver_close = patcher.start()

    def tearDown(self):
        """Clear all preparations for test and close connection"""
        pass

    def test_initORM(self):
        """ Basic smoke test: ORM is initialized """
        self.subject_model.initORM()
        self.mock_dbdriver_connect.assert_called_with(self.host,
                                                      self.username,
                                                      self.password,
                                                      self.database)

    def test_get_all_subjects(self):
        """Check if method returns a list of subjects"""
        expected_result = [
            {'id': 1, 'name': 'Math'},
            {'id': 2, 'name': 'Literature'}
        ]
        self.mock_dbdriver_mysql_do.return_value = expected_result

        actual_result = self.subject_model.get_all_subjects()

        self.mock_dbdriver_connect.assert_called_with(self.host,
                                                      self.username,
                                                      self.password,
                                                      self.database)
        self.mock_dbdriver_mysql_do.assert_called_with(
            self.subject_model.select_subjects_query + ' ')
        self.mock_dbdriver_close.assert_called_once_with()

        self.assertEqual(type(expected_result), type(actual_result))

    def test_get_subject_by_id(self):
        """Trying to get subject by given id"""
        expected_result = [
            {'id': self.test_subject.id_, 'name': self.test_subject.name}
        ]
        self.mock_dbdriver_mysql_do.return_value = expected_result

        result_subject = self.subject_model.get_subject_by_id(
            self.test_subject.id_)[0]

        self.mock_dbdriver_connect.assert_called_with(self.host,
                                                      self.username,
                                                      self.password,
                                                      self.database)
        self.mock_dbdriver_mysql_do.assert_called_with(
            self.subject_model.select_subjects_query +
            " WHERE id={0}".format(self.test_subject.id_))
        self.mock_dbdriver_close.assert_called_once_with()

        self.assertEqual(self.test_subject.id_, result_subject.id_)

    def test_get_subject_by_wrong_id(self):
        """Check whether the application returns
        the list of subjects with zero length"""
        expected_result = []
        self.mock_dbdriver_mysql_do.return_value = expected_result

        result_subject = self.subject_model.get_subject_by_id(self.wrong_id)

        self.mock_dbdriver_connect.assert_called_with(self.host,
                                                      self.username,
                                                      self.password,
                                                      self.database)
        self.mock_dbdriver_mysql_do.assert_called_with(
            self.subject_model.select_subjects_query +
            " WHERE id={0}".format(self.wrong_id))
        self.mock_dbdriver_close.assert_called_once_with()

        self.assertEqual(expected_result, result_subject)

    def test_update_subject_by_id(self):
        """Check if function updates subject by id"""
        self.test_subject.name = 'newSubjectName'

        self.subject_model.update_subject_by_id(self.test_subject)

        self.mock_dbdriver_connect.assert_called_with(self.host,
                                                      self.username,
                                                      self.password,
                                                      self.database)
        self.mock_dbdriver_update.assert_called_with(
            'Subjects', 'name="{0}"'.format(self.test_subject.name),
            'id={}'.format(self.test_subject.id_))
        self.mock_dbdriver_close.assert_called_once_with()

    def test_insert_subject(self):
        """Trying to add new subject to table 'Subjects'"""
        self.subject_model.insert_subject(self.test_subject)

        self.mock_dbdriver_connect.assert_called_with(self.host,
                                                      self.username,
                                                      self.password,
                                                      self.database)
        self.mock_dbdriver_insert.assert_called_with(
            'Subjects', ('name',),
            (self.test_subject.name,))
        self.mock_dbdriver_close.assert_called_once_with()

    def test_delete_subject_by_id(self):
        """"Trying to delete subject from table 'Subjects'"""
        self.subject_model.delete_subject_by_id(self.test_subject.id_)

        self.mock_dbdriver_connect.assert_called_with(self.host,
                                                      self.username,
                                                      self.password,
                                                      self.database)
        self.mock_dbdriver_delete.assert_called_with(
            'Subjects', 'id = {0}'.format(self.test_subject.id_))
        self.mock_dbdriver_close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main(verbosity=2)
