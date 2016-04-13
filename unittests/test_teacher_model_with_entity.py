"""Test Teachers model with entity"""

import unittest
from app.utils.dbdriver import DBDriver
from app.models.teachers_model_with_entity import Teacher, \
    ExtendedTeachersModel
from db import credentials


class TestTeachers(unittest.TestCase):
    """This class creates teacher objects to use them in Teacher Model"""

    def test_creation_of_teacher(self):
        """Test1: object teacher is created"""
        teacher = Teacher(1, "name", "login", "password", "email", "role_id",
                          "role_name", "school_id", "school_name")
        self.assertIsNotNone(teacher)


class TestTeachersModelWithEntity(unittest.TestCase):
    """This class is used to retrieve data about teachers from DB"""
    def setUp(self):
        """Creates a initial data and records for tests"""
        self.test_teacher_name = "testTeacherName"
        self.test_teacher_login = "testTeacherLogin"
        self.test_teacher_email = "testTeacherEmail"
        self.test_teacher_password = "testTeacherPassword"
        self.test_teacher_role_id = 1
        self.test_teacher_school_id = 1
        self.test_teacher_role_name = "testTeacherRoleName"
        self.test_teacher_school_name = "testTeacherSchoolName"
        self.extendedTeachersModel = ExtendedTeachersModel()

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.db = credentials[3]

        self.teacher_to_test = Teacher(1, self.test_teacher_name,
                                       self.test_teacher_login,
                                       self.test_teacher_password,
                                       self.test_teacher_email,
                                       self.test_teacher_role_id,
                                       self.test_teacher_role_name,
                                       self.test_teacher_school_id,
                                       self.test_teacher_school_name)
        self.teacher_to_test_ids = []

        self.orm = DBDriver()
        self.orm.connect(self.host, self.username, self.password, self.db)

        self.orm.insert('Teachers',
                        ('name', 'login', 'email', 'password', 'role_id'),
                        (self.teacher_to_test.name, self.teacher_to_test.login,
                         self.teacher_to_test.email,
                         self.teacher_to_test.password,
                         self.teacher_to_test.role_id))

        results = self.orm.mysql_do(
            ExtendedTeachersModel.select_teachers_query +
            ' WHERE t.name = "%s"' % self.teacher_to_test.name)

        self.orm.update('Teachers', 'school_id=%d' %
                        self.test_teacher_school_id,
                        'name="%s"' % self.teacher_to_test.name)

        for row in results:
            self.teacher_to_test_ids.append(row['id'])

    def tearDown(self):
        """Deletes all preparation for tests"""
        try:
            self.orm.delete('Teachers', 'name = "%s"' %
                            self.teacher_to_test.name)
            self.orm.delete('Teachers', 'name = "%s"' %
                            (self.teacher_to_test.name + 'Updated'))

        except Exception as error:
            print error
        finally:
            self.orm.close()

    def test_initORM(self):
        """Test2: ORM is initialized"""
        self.assertIsNotNone(self.extendedTeachersModel.initORM())

    def test_get_all_teachers_exists(self):
        """Test3: checks, whether get_all_teachers returns an object"""
        teachers = self.extendedTeachersModel.get_all_teachers()
        self.assertIsNotNone(teachers)

    def test_get_all_teachers_has_content(self):
        """Test4: checks, whether get_all_teachers is not empty"""
        teachers = self.extendedTeachersModel.get_all_teachers()
        self.assertTrue(len(teachers) > 0)

    def test_get_all_teachers_return_teacher_objects(self):
        """Test5: checks, that get_all_teachers returns an object
        in type of Teacher

        """
        teachers = self.extendedTeachersModel.get_all_teachers()
        for teacher in teachers:
            self.assertTrue(isinstance(teacher, Teacher))

    def test_get_teacher_by_id(self):
        """Test6: checks, that get_teacher_by_id return a Teacher object"""
        for id in self.teacher_to_test_ids:
            teacher = self.extendedTeachersModel.get_teacher_by_id(id)
            self.assertTrue(teacher[0].name == self.teacher_to_test.name)

    def test_get_all_teachers_by_role(self):
        """Test7: Get all teachers by role id"""
        teachers = self.extendedTeachersModel.get_all_teachers_by_role(
            self.teacher_to_test.role_id)
        self.assertIsNotNone(teachers)

    def test_get_all_teachers_by_school(self):
        """Test8: Get all teachers by school id"""
        teachers = self.extendedTeachersModel.get_all_teachers_by_school(
            self.teacher_to_test.school_id)
        self.assertIsNotNone(teachers)

    def test_update_teacher_by_id(self):
        """Test9: Update teacher by id"""
        teacher_to_update = Teacher(self.teacher_to_test_ids[0],
                                    self.test_teacher_name + 'Updated',
                                    self.test_teacher_login + 'Updated',
                                    self.test_teacher_password + 'Updated',
                                    self.test_teacher_email + 'Updated',
                                    self.test_teacher_role_id + 1,
                                    self.test_teacher_role_name,
                                    self.test_teacher_school_id,
                                    self.test_teacher_school_name)
        self.extendedTeachersModel.update_teacher_by_id(teacher_to_update)

        results = self.orm.mysql_do(
            ExtendedTeachersModel.select_teachers_query +
            ' where t.id = %d' % self.teacher_to_test_ids[0])
        self.assertTrue((results[0]['name'] == self.test_teacher_name +
                         'Updated') and
                        (results[0]['login'] == self.test_teacher_login +
                         'Updated') and
                        (results[0]['email'] == self.test_teacher_email +
                         'Updated') and
                        (results[0]['password'] == self.test_teacher_password +
                         'Updated') and
                        (results[0]['role_id'] == (self.test_teacher_role_id +
                                                   1)))

    def test_delete_teacher_by_id(self):
        """Test10: method delete_teacher_by_id"""
        teacher_count_before = \
            len(self.extendedTeachersModel.get_teacher_by_id(
                self.teacher_to_test_ids[0]))

        self.extendedTeachersModel.delete_teacher_by_id(
            self.teacher_to_test_ids[0])

        teacher_count_after = \
            len(self.extendedTeachersModel.get_teacher_by_id(
                self.teacher_to_test_ids[0]))

        self.assertTrue(teacher_count_before == teacher_count_after + 1)

    def test_insert_teacher(self):
        """Test11: method insert_teacher"""
        teacher_count_before = len(self.extendedTeachersModel.get_teacher_by_id
                                   (self.teacher_to_test_ids[0]))
        print "Count of teachers in Database before = ", teacher_count_before
        print "Now we add SQL query(+1 Teacher)"
        self.extendedTeachersModel.insert_teacher(Teacher
                                                  (1, "TeacherNameToInsert",
                                                   "TeacherLoginToInsert",
                                                   "TeacherEmailToInsert",
                                                   "TeacherPasswordToInsert",
                                                   "TeacherRoleIdToInsert",
                                                   "TeacherSchoolIdToInsert",
                                                   "TeacherRoleNameToInsert",
                                                   "TeacherSchoolNameToInsert"
                                                   ))
        teacher_count_after = len(self.extendedTeachersModel.get_teacher_by_id
                                  (self.teacher_to_test_ids[0]))
        print "Count of teachers in Database after SQL query = ", \
            teacher_count_after
        self.assertFalse(teacher_count_before == teacher_count_after)

    def test_set_role_id_to_teacher_by_id(self):
        """Test12: Set teacher's role id"""
        before = self.teacher_to_test.role_id
        self.teacher_to_test.role_id += 1
        self.extendedTeachersModel.set_role_id_to_teacher_by_id(
            self.teacher_to_test_ids[0], self.teacher_to_test.role_id)
        after = self.teacher_to_test.role_id
        self.assertTrue(before == after - 1)

    def test_set_school_id_to_teacher_by_id(self):
        """Test13: Set teacher's role id"""
        before = self.teacher_to_test.school_id
        self.teacher_to_test.school_id += 1
        self.extendedTeachersModel.set_school_id_to_teacher_by_id(
            self.teacher_to_test_ids[0], self.teacher_to_test.school_id)
        after = self.teacher_to_test.school_id
        self.assertTrue(before == after - 1)

    def test_set_password_to_teacher_by_id(self):
        """Test14: Set teacher's role id"""
        before = self.teacher_to_test.password
        self.teacher_to_test.password += 'New'
        self.extendedTeachersModel.set_password_to_teacher_by_id(
            self.teacher_to_test_ids[0], self.teacher_to_test.password)
        after = self.teacher_to_test.password
        self.assertTrue(before != after)

    def test_create_list_from_dbresult(self):
        """Test15: Make list of teacher objects from select"""
        results = self.orm.mysql_do(
            ExtendedTeachersModel.select_teachers_query)
        listdb = self.extendedTeachersModel._create_list_from_dbresult(results)
        self.assertIsInstance(listdb, list)


if __name__ == '__main__':
    unittest.main(verbosity=2)
