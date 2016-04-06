import unittest
from app.utils.dbdriver import DBDriver

from app.models.roles_model_with_entity import Role, \
    ExtendedRolesModel


class TestRole(unittest.TestCase):
    def test_creation_of_role(self):
        """ Basic smoke test: object role is created """
        role = Role(5, "Boss")
        self.assertIsNotNone(role)


class TestExtendedRolesModel(unittest.TestCase):
    select_roles_query = ' SELECT id, role_name  \
                            FROM Roles '

    def setUp(self):
        """Preparation"""
        self.test_role_name = "Boss"
        self.test_role_id = 40
        self.extendedRolesModel = ExtendedRolesModel()
        self.role_to_test = Role(self.test_role_id, self.test_role_name)

        from db import credentials
        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.db = credentials[3]

        orm = DBDriver()
        orm.connect(self.host, self.username, self.password, self.db)
        orm.insert('Roles', ('id', 'role_name'),
                   (self.test_role_id, self.test_role_name))

    def tearDown(self):
        """ Fixture that deletes all preparation for tests """
        try:
            orm = DBDriver()
            orm.connect(self.host, self.username, self.password, self.db)
            orm.delete('Roles', 'role_name = "%s"' % (self.test_role_name))
        except:
            pass
        finally: 
            orm.close()

    def test_initORM(self):
        """ Basic smoke test: ORM
         is initialized """
        self.assertIsNotNone(self.extendedRolesModel.initORM())

    def test_get_all_roles(self):
        """Get all roles"""
        role_to_test = self.extendedRolesModel._get_roles()
        self.assertIsNotNone(role_to_test)

    def test_get_role_by_id(self):
        """Get role by given id"""
        role = self.extendedRolesModel.get_role_by_id(40)
        self.assertTrue(role[0].role_name == self.test_role_name)

    def test_create_list_from_dbresult(self):
        """Check if func creates list"""
        role = self.extendedRolesModel._get_roles('WHERE id=%d' % (40))
        self.assertIsInstance(role, list)


if __name__ == "__main__":
    unittest.main(verbosity=2)