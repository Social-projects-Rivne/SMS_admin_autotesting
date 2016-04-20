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

        self.subject_model = app.models.subjects_model_with_entity \
            .ExtendedSubjectsModel()

        # self.dbdriver = DBDriver()

        # self.dbdriver_mock = self.__create_patch(
        #     'app.models.subjects_model_with_entity.DBDriver')

        # self.subject_model = \
        #     app.models.subjects_model_with_entity.ExtendedSubjectsModel()
        # self.dbh = self.subject_model.initORM()
        # self.test_subject_name = 'TestSubject'
        # self.test_subject_id = self.dbh.mysql_do(
        #     "SELECT id FROM SMSDB.Subjects WHERE name = '{0}'".format(
        #         self.test_subject_name))
        #
        # if len(self.test_subject_id) > 0:
        #     self.test_subject_id = self.test_subject_id[0]['id']
        # else:
        #     # manually add test subject 'TestSubject' and get it id :)
        #     self.dbh.mysql_do(
        #         "INSERT INTO SMSDB.Subjects (id,name) VALUES (null,'{0}')".format(
        #             self.test_subject_name))
        #     self.test_subject_id = self.dbh.mysql_do(
        #         "SELECT id FROM SMSDB.Subjects WHERE name = '{0}'".format(
        #             self.test_subject_name))[0]['id']
        #
        # self.test_subject = app.models.subjects_model_with_entity.Subject(
        #     self.test_subject_id, self.test_subject_name)

    def tearDown(self):
        """Clear all preparations for test and close connection"""
        # restore changes after insert and delete test
        # self.dbh.mysql_do(
        #     "DELETE FROM SMSDB.Subjects WHERE name = '{0}'".format(
        #         'newTestSubject'))

        # delete our 'TestSubject' from db
        # self.dbh.mysql_do(
        #     "DELETE FROM SMSDB.Subjects WHERE name = '{0}' AND id = '{1}'"
        #         .format(self.test_subject_name, self.test_subject_id))
        #
        # self.dbh.close()

    @mock.patch.object(DBDriver, 'connect')
    def test_initORM(self, mock_connect):
        """ Basic smoke test: ORM is initialized """
        self.subject_model.initORM()
        mock_connect.assert_called_with(self.host, self.username,
                                        self.password, self.database)

    @mock.patch.object(DBDriver, 'connect')
    @mock.patch.object(DBDriver, 'mysql_do')
    @mock.patch.object(DBDriver, 'close') # stub
    def test_get_all_subjects(self, mock_close, mock_mysql_do, mock_connect):
        """Check if method returns a list of subjects"""
        expected_result = [
            {'id': 1, 'name': 'Math'},
            {'id': 2, 'name': 'Literature'}
        ]
        self.subject_model.initORM()

        mock_mysql_do.return_value = expected_result
        actual_result = self.subject_model.get_all_subjects()
        mock_connect.assert_called_with(self.host, self.username,
                                        self.password, self.database)
        mock_mysql_do.assert_called_with(self.subject_model
                                         .select_subjects_query + ' ')
        self.assertEqual(type(expected_result), type(actual_result))

    # def test_get_subject_by_id(self):
    #     """Trying to get subject by given id"""
    #     result_subject = self.subject_model.get_subject_by_id(
    #         self.test_subject_id)
    #     self.assertEqual(self.test_subject_name, result_subject[0].name)
    #
    # def test_get_subject_by_wrong_id(self):
    #     """Check whether the application returns
    #     the list of subjects with zero length"""
    #     result_subject = self.subject_model.get_subject_by_id(99999)
    #     self.assertEqual(0, len(result_subject))
    #
    # def test_update_subject_by_id(self):
    #     """Check if function updates subject by id"""
    #     self.subject_model.update_subject_by_id(
    #         Subject(self.test_subject_id, 'newSubjectName'))
    #     new_subject_name = self.dbh.mysql_do(
    #         "SELECT name FROM SMSDB.Subjects WHERE id = '{0}'".format(
    #                 self.test_subject_id))[0]['name']
    #     self.assertEqual(new_subject_name, 'newSubjectName')
    #     # return changes
    #     self.dbh.mysql_do(
    #         "UPDATE SMSDB.Subjects SET name = '{0}' WHERE id = '{1}'".format(
    #             self.test_subject_name, self.test_subject_id))
    #
    # def test_update_subject_by_wrong_id(self):
    #     """Trying to update subject by wrong id"""
    #     self.subject_model.update_subject_by_id(
    #         Subject(99999, 'newSubjectName'))
    #     new_subject_name = self.dbh.mysql_do(
    #         "SELECT name FROM SMSDB.Subjects WHERE id = '{0}'".format(
    #             99999))
    #     self.assertEqual(0, len(new_subject_name))
    #
    # def test_insert_subject(self):
    #     """Trying to add new subject to table 'Subjects'"""
    #     self.subject_model.insert_subject(Subject(1, 'newTestSubject'))
    #     last_id = self.dbh.mysql_do(
    #         "SELECT id from SMSDB.Subjects WHERE name = '{0}' ORDER BY id DESC".format(
    #             'newTestSubject'))[0]['id']
    #     check_result = self.dbh.mysql_do(
    #         "SELECT * FROM SMSDB.Subjects WHERE id = '{0}'".format(
    #             last_id))
    #     self.assertTrue(len(check_result) == 1)
    #
    # def test_delete_subject_by_id(self):
    #     """"Trying to delete subject from table 'Subjects'"""
    #     self.dbh.mysql_do(
    #         "INSERT INTO SMSDB.Subjects (id, name) VALUES (NULL,'{0}')".format(
    #             'newTestSubject'))
    #     last_id = self.dbh.mysql_do(
    #         "SELECT id from SMSDB.Subjects WHERE name = '{0}' ORDER BY id DESC".format(
    #             'newTestSubject'))[0]['id']
    #     # testing delete function on just inserted subject
    #     self.subject_model.delete_subject_by_id(last_id)
    #     check_result = self.dbh.mysql_do(
    #         "SELECT * FROM SMSDB.Subjects WHERE id = '{0}'".format(last_id))
    #     self.assertTrue(len(check_result) == 0)
    #
    # def test_delete_subject_by_wrong_id(self):
    #     """Trying to delete subject by wrong id"""
    #     subjects_before_delete = self.dbh.mysql_do(
    #         "SELECT * FROM SMSDB.Subjects")
    #     self.subject_model.delete_subject_by_id(99999)
    #     subjects_after_delete = self.dbh.mysql_do(
    #         "SELECT * FROM SMSDB.Subjects")
    #     self.assertEqual(subjects_before_delete, subjects_after_delete)


if __name__ == "__main__":
    unittest.main(verbosity=2)
