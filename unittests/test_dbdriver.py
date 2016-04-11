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
        self.testdb.mysql_do('create table TestTable (id int(10), Name VARCHAR(30))')
        self.testdb.insert('TestTable', ('id', 'Name'), (1, "Alexey"))
        # countRowBefore = self.testdb.mysql_do('SELECT COUNT(*) FROM TestTable')
        # print '1 - Count of strings in database = ', countRowBefore[0]

    def tearDown(self):
        """Deletes all preparation for tests"""
        try:
            self.testdb.mysql_do('drop table if exists TestTable')
        except Exception as e:
            print(e)
        finally:
            self.testdb.close()
            print('Disconnected from database')
# ----------------------------------------------------------------------------------------------------------------

    def test_connect(self):
        """Connect to database"""
        self.assertIsNotNone(self.db)
        print('Connection with MYSQL database established')

    def test_insert(self):
        """Inserting info into the TestTable"""
        # countRowBefore = self.testdb.mysql_do('SELECT COUNT(*) FROM TestTable')
        # print 'Count of strings in database = ', countRowBefore
        self.testdb.insert('TestTable', ('id', 'Name'), (1, "Alexey"))
        # self.testdb.insert('TestTable', ('id', 'Name'), (2, "Vasya"))
        # Is really needed next string there ??????
        result = self.testdb.get('TestTable', ('id', 'Name'))
        # countRowAfter = self.testdb.mysql_do('SELECT COUNT(*) FROM TestTable')
        # print 'Count of strings in database = ', countRowBefore
        self.assertTrue(result[0]['Name'] == "Alexey")
        # self.assertTrue(countRowBefore == countRowAfter)
        print('TestTable was successfully created and new info was inserted')

    def test_get(self):
        """Getting info from the TestTable"""
        result = self.testdb.get('TestTable', ('id', 'Name'))
        # self.testdb.insert('TestTable', ('id', 'Name'), (1, "Alexey")) ???????
        self.assertIsNotNone(result)
        print('The information was successfully received')

    def test_update(self):
        """Update info in the TestTable"""
        self.testdb.update('TestTable', ('id', 'Name'), ('2', "Vasya"))
        result = self.testdb.get('TestTable', ('id', 'Name'))
        self.assertTrue(result[0]['Name'] == "Vasya")


if __name__ == '__main__':
    unittest.main(verbosity=2)
