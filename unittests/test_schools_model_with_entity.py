# -*- coding: utf-8 -*-
""" A couple of tests for testing module schools_model_with_entity """

import unittest

from app.utils.dbdriver import DBDriver
from app.models.schools_model_with_entity import School
from app.models.schools_model_with_entity import ExtendedSchoolsModel as e_s_m
from db import credentials


class TestSchool(unittest.TestCase):

    """ Class with methods, for testing School class """

    def test_creation_of_school(self):
        """ Basic smoke test: object school is created """
        school = School(1, "name", "address")
        self.assertIsNotNone(school)


class TestExtendedSchoolsModel(unittest.TestCase):

    """ Class with methods, for testing ExtendedSchoolModel class """

    def setUp(self):
        """ Fixture that creates a initial data and records for tests """
        self.test_school_id = 77777777777
        self.test_school_name = "testSchoolName"
        self.test_school_address = "testSchoolAddress"
        self.school_model = e_s_m()

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.database = credentials[3]

        self.test_school = School(self.test_school_id+1,
                                  self.test_school_name,
                                  self.test_school_address)
        self.school_to_test_ids = []

        self.orm = DBDriver()
        self.orm.connect(self.host, self.username, self.password, self.database)
        self.orm.insert('Schools', ('name', 'address'),
                        (self.test_school.name, self.test_school.address))
        results = self.orm.mysql_do(
            e_s_m.select_schools_query +
            ' where name = "{}"'.format(self.test_school.name))
        for row in results:
            self.school_to_test_ids.append(row['id'])

    def tearDown(self):
        """ Fixture that deletes all preparation for tests """
        try:
            self.orm.delete('Schools',
                            'name = "{0}" and address = "{1}"'
                            .format(self.test_school_name,
                                    self.test_school_address))
            self.orm.delete('Schools',
                            'name = "{0}" and address = "{1}"'
                            .format(self.test_school_name + 'Updated',
                                    self.test_school_address + 'Updated'))
        except Exception as error:
            print(error)
        finally:
            self.orm.close()

    def test_creation_of_ExtendedSchoolsModel(self):
        """ Basic smoke test: object ExtendedSchoolsModel is created """
        school_model = e_s_m()
        self.assertIsNotNone(school_model)

    def test_initORM(self):
        """ Basic smoke test: ORM is initialized """
        self.assertIsNotNone(self.school_model.initORM())

    def test_get_all_schools_exists(self):
        """ Test, that checks, whether get_all_schools returns an object """
        schools = self.school_model.get_all_schools()
        self.assertIsNotNone(schools)

    def test_get_all_schools_has_content(self):
        """ Test, that checks, whether get_all_schools is not empty """
        schools = self.school_model.get_all_schools()
        self.assertTrue(len(schools) > 0)

    def test_get_all_schools_return_school_objects(self):
        """  Test, that checks, whether get_all_schools returns an
        object in type of School """
        schools = self.school_model.get_all_schools()
        for school in schools:
            self.assertTrue(isinstance(school, School))

    def test_get_school_by_id(self):
        """ Tests,that method get_school_by_id returns apropriate object """
        for school_id in self.school_to_test_ids:
            school = self.school_model.get_school_by_id(school_id)
            self.assertTrue((school[0].name == self.test_school.name) and
                            (school[0].address == self.test_school.address))

    def test_update_school_by_id(self):
        """ Test method update_school_by_id """
        school_to_update = School(self.school_to_test_ids[0],
                                  self.test_school_name + 'Updated',
                                  self.test_school_address + 'Updated')
        self.school_model.update_school_by_id(school_to_update)

        results = self.orm.mysql_do(
            e_s_m.select_schools_query + ' where id = {}'.format(
                self.school_to_test_ids[0]))

        self.assertTrue(
            (results[0]['name'] == self.test_school_name + 'Updated') and
            (results[0]['address'] == self.test_school_address + 'Updated'))

    def test_delete_school_by_id(self):
        """ Test method delete_school_by_id """
        schools_count_before = \
            len(self.school_model.get_school_by_id(self.school_to_test_ids[0]))

        self.school_model.delete_school_by_id(self.school_to_test_ids[0])

        schools_count_after = \
            len(self.school_model.get_school_by_id(self.school_to_test_ids[0]))

        self.assertTrue(schools_count_before == schools_count_after + 1)

    def test_insert_school(self):
        """ Test method insert_school """
        schools_count_before = \
            len(self.school_model.get_school_by_id(self.school_to_test_ids[0]))
        self.school_model.insert_school(School(self.test_school_id,
                                               self.test_school_name,
                                               self.test_school_address))
        schools_count_after = \
            len(self.school_model.get_school_by_id(self.school_to_test_ids[0]))
        self.assertTrue(schools_count_before == schools_count_after - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
