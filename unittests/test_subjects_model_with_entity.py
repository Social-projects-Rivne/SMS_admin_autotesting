"""
This code implements unittest for
subject model of the application
"""

import unittest

from app.models.subjects_model_with_entity import Subject,\
    ExtendedSubjectsModel


class TestSubject(unittest.TestCase):

    """
    Smoke test for creation of class instance
    """

    def test_creation_of_subject(self):
        """
        Basic method to create subject
        """

        subject = Subject(2, 'TestSubject')
        self.assertIsNotNone(subject)


class TestExtendedSubjectsModel(unittest.TestCase):

    """
    This class makes unit tests for specific
    classes Subject -> ExtendedSubjectsModel
    """

    def setUp(self):
        """
        Fixture that creates an initial data and records for tests
        """

        self.subject_model = ExtendedSubjectsModel()
        self.dbh = self.subject_model.initORM()
        self.test_subject_name = 'TestSubject'
        self.test_subject_id = self.dbh.mysql_do(
            "SELECT id FROM SMSDB.Subjects WHERE name = '{0}'".format(
                self.test_subject_name))

        if len(self.test_subject_id) > 0:
            self.test_subject_id = self.test_subject_id[0]['id']
        else:
            # manually add test subject 'TestSubject' and get it id :)
            self.dbh.mysql_do(
                "INSERT INTO SMSDB.Subjects (id,name) VALUES (null,'{0}')"
                    .format(self.test_subject_name))
            self.test_subject_id = self.dbh.mysql_do(
                "SELECT id FROM SMSDB.Subjects WHERE name = '{0}'".format(
                    self.test_subject_name))[0]['id']

        self.test_subject = Subject(self.test_subject_id,
                                    self.test_subject_name)

    def tearDown(self):
        """
        Clear all preparations for test and close connection
        """

        # restore changes after insert and delete test
        self.dbh.mysql_do(
            "DELETE FROM SMSDB.Subjects WHERE name = '{0}'".format(
                'newTestSubject'))

        # delete our 'TestSubject' from db
        self.dbh.mysql_do(
            "DELETE FROM SMSDB.Subjects WHERE name = '{0}' AND id = '{1}'"
                .format(self.test_subject_name, self.test_subject_id))

        self.dbh.close()

    def test_initORM(self):
        """
        Basic smoke test: ORM is initialized
        """

        self.assertIsNotNone(self.subject_model.initORM())

    def test_get_all_subjects(self):
        """
        Check if method returns a list of subjects
        """

        result_list = self.subject_model.get_all_subjects()
        self.assertIsInstance(result_list, type(list()))

    def test_get_subject_by_id(self):
        """
        Trying to get subject by given id
        """

        result_subject = self.subject_model.get_subject_by_id(
            self.test_subject_id)
        self.assertEqual(self.test_subject_name, result_subject[0].name)

    def test_get_subject_by_wrong_id(self):
        """
        Check whether the application returns
        the list of subjects with zero length
        """

        result_subject = self.subject_model.get_subject_by_id(99999)
        self.assertEqual(0, len(result_subject))

    def test_update_subject_by_id(self):
        """
        Check if function updates subject by id
        """

        self.subject_model.update_subject_by_id(
            Subject(self.test_subject_id, 'newSubjectName'))
        new_subject_name = self.dbh.mysql_do(
            "SELECT name FROM SMSDB.Subjects WHERE id = '{0}'".format(
                    self.test_subject_id))[0]['name']
        self.assertEqual(new_subject_name, 'newSubjectName')
        # return changes
        self.dbh.mysql_do(
            "UPDATE SMSDB.Subjects SET name = '{0}' WHERE id = '{1}'".format(
                self.test_subject_name, self.test_subject_id))

    def test_update_subject_by_wrong_id(self):
        """
        Trying to update subject by wrong id
        """

        self.subject_model.update_subject_by_id(
            Subject(99999, 'newSubjectName'))
        new_subject_name = self.dbh.mysql_do(
            "SELECT name FROM SMSDB.Subjects WHERE id = '{0}'".format(
                99999))
        self.assertEqual(0, len(new_subject_name))

    def test_insert_subject(self):
        """
        Trying to add new subject to table 'Subjects'
        """

        self.subject_model.insert_subject(Subject(1, 'newTestSubject'))
        last_id = self.dbh.mysql_do(
            "SELECT id from SMSDB.Subjects WHERE name = '{0}' "
            "ORDER BY id DESC".format('newTestSubject'))[0]['id']
        check_result = self.dbh.mysql_do(
            "SELECT * FROM SMSDB.Subjects WHERE id = '{0}'".format(
                last_id))
        self.assertTrue(len(check_result) == 1)

    def test_delete_subject_by_id(self):
        """"
        Trying to delete subject from table 'Subjects'
        """

        self.dbh.mysql_do(
            "INSERT INTO SMSDB.Subjects (id, name) VALUES (NULL,'{0}')"
                .format('newTestSubject'))
        last_id = self.dbh.mysql_do(
            "SELECT id from SMSDB.Subjects WHERE name = '{0}' "
            "ORDER BY id DESC".format('newTestSubject'))[0]['id']
        # testing delete function on just inserted subject
        self.subject_model.delete_subject_by_id(last_id)
        check_result = self.dbh.mysql_do(
            "SELECT * FROM SMSDB.Subjects WHERE id = '{0}'".format(last_id))
        self.assertTrue(len(check_result) == 0)

    def test_delete_subject_by_wrong_id(self):
        """
        Trying to delete subject by wrong id
        """

        subjects_before_delete = self.dbh.mysql_do(
            "SELECT * FROM SMSDB.Subjects")
        self.subject_model.delete_subject_by_id(99999)
        subjects_after_delete = self.dbh.mysql_do(
            "SELECT * FROM SMSDB.Subjects")
        self.assertEqual(subjects_before_delete, subjects_after_delete)


if __name__ == "__main__":
    unittest.main(verbosity=2)


