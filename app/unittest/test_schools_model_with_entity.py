import unittest
from app.utils.dbdriver import DBDriver

from app.models.schools_model_with_entity import School, \
    ExtendedSchoolsModel


class TestSchool(unittest.TestCase):
    def test_creation_of_school(self):
        """ Basic smoke test: object school is created """
        school = School(1, "name", "address")
        self.assertIsNotNone(school)


class TestExtendedSchoolsModel(unittest.TestCase):
    def setUp(self):
        """ Fixture that creates a initial data and records for tests """
        self.test_school_name = "testSchoolName"
        self.test_school_address = "testSchoolAddress"
        self.extendedSchoolsModel = ExtendedSchoolsModel()

        from db import credentials
        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.db = credentials[3]

        self.school_to_test = School(1, self.test_school_name, self.test_school_address)
        self.school_to_test_ids = []

        orm = DBDriver()
        orm.connect(self.host, self.username, self.password, self.db)
        orm.insert('Schools', ('name', 'address'),
                   (self.school_to_test.name, self.school_to_test.address))
        results = orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query + ' where name = "%s"' % self.school_to_test.name)
        for row in results:
            self.school_to_test_ids.append(row['id'])
        orm.close()

    def tearDown(self):
        """ Fixture that deletes all preparation for tests """
        try:
            orm = DBDriver()
            orm.connect(self.host, self.username, self.password, self.db)
            orm.delete('Schools', 'name = "%s" and address = "%s"' % (self.test_school_name, self.test_school_address))
            orm.delete('Schools', 'name = "%s" and address = "%s"' % (
            self.test_school_name + 'Updated', self.test_school_address + 'Updated'))
            orm.close()
        except:
            pass

    def test_initORM(self):
        """ Basic smoke test: ORM is initialized """
        self.assertIsNotNone(self.extendedSchoolsModel.initORM())

    def test_get_all_schools_exists(self):
        """ Test, that checks, whether get_all_schools returns an object """
        schools = self.extendedSchoolsModel.get_all_schools()
        self.assertIsNotNone(schools)

    def test_get_all_schools_has_content(self):
        """ Test, that checks, whether get_all_schools is not empty """
        schools = self.extendedSchoolsModel.get_all_schools()
        self.assertTrue(len(schools) > 0)

    def test_get_all_schools_return_school_objects(self):
        """  Test, that checks, whether get_all_schools returns an object in type of School """
        schools = self.extendedSchoolsModel.get_all_schools()
        for school in schools:  # ??????????????
            self.assertTrue(isinstance(school, School))

    def test_get_school_by_id(self):
        """ Tests,that method get_school_by_id returns apropriate object """
        for id in self.school_to_test_ids:  # ??????????????
            school = self.extendedSchoolsModel.get_school_by_id(id)
            self.assertTrue((school[0].name == self.school_to_test.name)
                            and (school[0].address == self.school_to_test.address))

    def test_update_school_by_id(self):
        """ Test method update_school_by_id """
        school_to_update = School(self.school_to_test_ids[0],
                                  self.test_school_name + 'Updated',
                                  self.test_school_address + 'Updated')
        self.extendedSchoolsModel.update_school_by_id(school_to_update)

        orm = DBDriver()
        orm.connect(self.host, self.username, self.password, self.db)
        results = orm.mysql_do(
            ExtendedSchoolsModel.select_schools_query + ' where id = %d' % self.school_to_test_ids[0])
        orm.close()

        self.assertTrue((results[0]['name'] == self.test_school_name + 'Updated') and
                        (results[0]['address'] == self.test_school_address + 'Updated'))

    def test_delete_school_by_id(self):
        """ Test method delete_school_by_id """
        schools_count_before = len(self.extendedSchoolsModel.get_school_by_id(self.school_to_test_ids[0]))
        self.extendedSchoolsModel.delete_school_by_id(self.school_to_test_ids[0])
        schools_count_after = len(self.extendedSchoolsModel.get_school_by_id(self.school_to_test_ids[0]))
        self.assertTrue(schools_count_before == schools_count_after + 1)

    def test_insert_school(self):
        """ Test method insert_school """
        schools_count_before = len(self.extendedSchoolsModel.get_school_by_id(self.school_to_test_ids[0]))
        self.extendedSchoolsModel.insert_school(School(777, "SchoolNameToInsert", "SchoolAddressToInsert"))
        schools_count_after = len(self.extendedSchoolsModel.get_school_by_id(self.school_to_test_ids[0]))
        self.assertTrue(schools_count_before == schools_count_after - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
