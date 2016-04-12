"""Test DBDriver.py"""

import unittest
from app.utils.dbdriver import DBDriver
from db import credentials


class TestDBDriver(unittest.TestCase):
    """This class can connect to MySQL databases and run CRUD operations"""

    def setUp(self):
        """Creates a initial data and records for tests"""
        self.testdb = DBDriver()

        self.host = credentials[0]
        self.username = credentials[1]
        self.password = credentials[2]
        self.db = credentials[3]

        self.testdb.connect(self.host, self.username, self.password, self.db)
        self.testdb.mysql_do('create table TestTable (id int(10) '
                             'NOT NULL AUTO_INCREMENT, '
                             'Name VARCHAR(30) NOT NULL, PRIMARY KEY (id))')

    def tearDown(self):
        """Deletes all preparation for tests"""
        try:
            self.testdb.mysql_do('drop table if exists TestTable')
        except Exception as error:
            print error
        finally:
            self.testdb.close()

    def test_connect(self):
        """Connect to database"""
        self.assertIsNotNone(self.db)

    def test_mysql_do_negative(self):
        """Rollback in case there is any error"""
        result = self.testdb.mysql_do('SELECTS * FROM TestTable')
        self.assertIsNone(result)

    def test_insert(self):
        """Inserting info into the TestTable"""
        count_before = self.testdb.mysql_do('SELECT * FROM TestTable')
        self.testdb.insert('TestTable', ('Name',), ('Vasya',))
        count_after = self.testdb.mysql_do('SELECT * FROM TestTable')
        self.assertFalse(count_before == count_after)

    def test_get(self):
        """Getting info from the TestTable"""
        self.testdb.mysql_do('INSERT INTO `TestTable`(`Name`) VALUES("Gora")')
        result = self.testdb.get('TestTable', ('id', 'Name'))
        self.assertIsNotNone(result)

    def test_get_negative(self):
        """Rollback in case there is any error"""
        self.testdb.mysql_do('INSERT INTO `TestTable`(`Name`) VALUES("Gora")')
        result = self.testdb.get('TestTables', ('id', 'Name'))
        self.assertIsNone(result)

    def test_update(self):
        """Updating info in the TestTable"""
        self.testdb.mysql_do('INSERT INTO `TestTable`(`Name`) VALUES("Gora")')
        self.testdb.update('TestTable', 'name = "Alexey"', 'Name = "Gora"')
        result = self.testdb.mysql_do('SELECT Name FROM TestTable')
        self.assertTrue(result[0]['Name'] == "Alexey")

    def test_delete(self):
        """Deleting data from TestTable"""
        count_before = self.testdb.mysql_do('SELECT * FROM TestTable')
        self.testdb.mysql_do('INSERT INTO `TestTable`(`Name`) VALUES("Gora")')
        self.testdb.mysql_do('INSERT INTO `TestTable`(`Name`) VALUES("Alex")')
        self.testdb.delete('TestTable', "id = 1")
        count_after = self.testdb.mysql_do('SELECT * FROM TestTable')
        self.assertFalse(count_before == count_after)

    def test_extract_tuple_int(self):
        """Check if _extract_tuple returns tuple with elements of TestTable"""
        # self.testdb.mysql_do('INSERT INTO `TestTable`(`id`) VALUES("12345")')
        result = self.testdb._extract_tuple((1, 2, 3, 4, 5))
        result2 = self.testdb._extract_tuple(('hello, world!'))
        self.assertIsInstance(result, str)
        self.assertIsInstance(result2, str)


if __name__ == '__main__':
    unittest.main(verbosity=2)
