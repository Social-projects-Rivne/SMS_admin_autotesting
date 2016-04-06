import unittest
import sys
import os
sys.path.insert(0,
                os.path.dirname(os.path.dirname
                                (os.path.abspath
                                 (__file__))))
from app.models.subjects_model_with_entity import Subject, ExtendedSubjectsModel
from app.utils.dbdriver import DBDriver
from config import credentials

class TestSubject(unittest.TestCase):

    """Smoke test for creation of class instance"""

    def test_creation_of_subject(self):

        """Basic method to create subject"""

        subject = Subject(2, 'TestSubject')
        self.assertIsNotNone(subject)


class TestExtendedSubjectsModel(unittest.TestCase):

    """This class makes unit tests for specific
    classes Subject -> ExtendedSubjectsModel"""

    def setUp(self):

        """Fixture that creates an initial data and records for tests"""

        self.subject_model = ExtendedSubjectsModel()
        self.dbh = self.subject_model.initORM()
        self.test_subject_name = 'Math'
        self.test_subject_id = self.dbh.mysql_do(
            "SELECT id FROM SMSDB.Subjects WHERE name = '{0}'".format(
            self.test_subject_name))

        # print('len of id select is: ' + str(len(self.test_subject_id)))

        if len(self.test_subject_id) > 0:
            self.test_subject_id = self.test_subject_id[0]['id']
        else:
            # manualy set current id of subject 'Math' :)
            self.test_subject_id = 18

        self.test_subject = Subject(self.test_subject_id, self.test_subject_name)

    def tearDown(self):
        """Clear all preparations for test"""
        self.dbh.close()

    def test_get_all_subjects(self):

        """Check if method returns a list of subjects"""

        result_list = self.subject_model.get_all_subjects()
        self.assertIsInstance(result_list, type(list()))

    def test_get_subject_by_id(self):

        """Trying to get subject by given id"""

        result_subject = self.subject_model.get_subject_by_id(
            self.test_subject_id)
        self.assertEqual(self.test_subject_name, result_subject[0].name)

    def test_update_subject_by_id(self):

        """Check if function updates subject by id"""

        self.subject_model.update_subject_by_id(
            Subject(self.test_subject_id,'newSubjectName'))
        new_subject_name = self.dbh.mysql_do(
            "SELECT name FROM SMSDB.Subjects WHERE id = '{0}'".format(
            self.test_subject_id))[0]['name']
        self.assertEqual(new_subject_name,'newSubjectName')
        # return changes
        self.dbh.mysql_do(
            "UPDATE SMSDB.Subjects SET name = '{0}' WHERE id = '{1}'".format(
                self.test_subject_name, self.test_subject_id))

    def test_insert_subject(self):

        """Trying to add new subject to table 'Subjects' """

        self.subject_model.insert_subject(Subject(1,'newTestSubject'))
        last_id = self.dbh.mysql_do(
            "SELECT id from SMSDB.Subjects ORDER BY id DESC")[0]['id']
        # last_id = dbh.cursor.lastrowid
        # print(last_id)
        check_result = self.dbh.mysql_do(
            "SELECT * FROM SMSDB.Subjects WHERE id = '{0}'".format(
            last_id))

        if len(check_result) != 0:
            self.assertEqual(1,1)
            # restore changes
            self.dbh.mysql_do(
                "DELETE FROM SMSDB.Subjects WHERE id = '{0}'".format(
                last_id))
        else:
            self.assertEquals(0,1)

    def test_delete_subject_by_id(self):

        """"Trying to delete subject from table 'Subjects' """

        self.dbh.mysql_do(
            "INSERT INTO SMSDB.Subjects (id, name) VALUES (NULL,'{0}')".format(
            'newTestSubject'))
        last_id = self.dbh.mysql_do(
            "SELECT id from SMSDB.Subjects ORDER BY id DESC")[0]['id']
        # testing delete function on just inserted subject
        self.subject_model.delete_subject_by_id(last_id)
        select = self.dbh.mysql_do(
            "SELECT * FROM SMSDB.Subjects WHERE id = '{0}'".format(last_id))

        if len(select) == 0:
            self.assertEquals(1,1)
        else:
            # try manualy delete our inserted subject and generate fail
            self.dbh.mysql_do(
                "DELETE FROM SMSDB.Subjects WHERE id = '{0}'".format(last_id))
            self.assertEquals(0,1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

