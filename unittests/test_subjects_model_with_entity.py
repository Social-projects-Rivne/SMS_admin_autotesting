import unittest
import sys, os
sys.path.insert(0,
                os.path.dirname(os.path.dirname
                                (os.path.abspath
                                 (__file__))))
from app.models.subjects_model_with_entity import Subject, ExtendedSubjectsModel
from app.utils.dbdriver import DBDriver
from config import credentials

class TestSubject(unittest.TestCase):

    def test_creation_of_subject(self):
        """Basic method to create subject"""
        subject = Subject(2, 'TestSubject')
        self.assertIsNotNone(subject)


class TestExtendedSubjectsModel(unittest.TestCase):

    """This class makes unit tests for specific
    classes Subject -> ExtendedSubjectsModel"""

    def setUp(self):
        self.subject_model = ExtendedSubjectsModel()
        self.subject_id = 1
        self.subject_name = 'newTestSubject'
        self.subject = Subject(self.subject_id, self.subject_name)

	# self.subject_model.insert_subject(self.subject)

    def tearDown(self):
        """Clear all preparations for test"""
	# self.subject_model.delete_subject_by_id(self.subject_id)

    def test_get_all_subjects(self):
        """Check if method returns a list of subjects"""
        result_list = self.subject_model.get_all_subjects()
        self.assertIsInstance(result_list, type(list()))

    def test_get_subject_by_id(self):
        """Trying to get subject by given id"""
        result_subject = self.subject_model.get_subject_by_id(1)
        self.assertEqual('Math', result_subject[0].name)

    def test_update_subject_by_id(self):
        """Check if function updates subject by id"""
        origin_subject_name = self.subject_model.get_subject_by_id(1)
        origin_subject_name = origin_subject_name[0].name
        new_subject = Subject(1, 'newSubjectName')
        self.subject_model.update_subject_by_id(new_subject)
        edited_subject = self.subject_model.get_subject_by_id(1)
        self.assertEqual(edited_subject[0].name,'newSubjectName')
        # return changes
        new_subject = Subject(1, origin_subject_name)
        self.subject_model.update_subject_by_id(new_subject)

    def test_insert_subject(self):
        self.subject_model.insert_subject(Subject(1,'newTestSubject'))
        dbh = self.subject_model.initORM()
        last_id = dbh.mysql_do('SELECT id from SMSDB.Subjects ORDER BY id DESC')[0]['id']
        # last_id = dbh.cursor.lastrowid
        dbh.close()
        # print(last_id)
        inserted_subject = self.subject_model.get_subject_by_id(last_id)[0]
        self.assertEqual(inserted_subject.name, 'newTestSubject')
        self.subject_model.delete_subject_by_id(last_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)

