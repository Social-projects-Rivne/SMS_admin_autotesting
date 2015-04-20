#!/usr/bin/env python

import MySQLdb


class MySQLORM(object):

    """This class can connect to MySQL databases and run CRUD operations"""

    def connect(self, host, username, password, db):
        """Connect to database"""
        self.db = MySQLdb.connect(host, username, password, db)
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        #self.db.set_character_set('utf8')
        #self.cursor.execute('SET NAMES utf8;')
        #self.cursor.execute('SET CHARACTER SET utf8;')
        #self.cursor.execute('SET character_set_connection=utf8;')

    def mysql_do(self, sql):
        """Run MySQL operations"""
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit changes in the database
            self.db.commit()
            # Return fetched result
            return self.cursor.fetchall()
        except:
            # Rollback in case there is any error
            self.db.rollback()

    def insert(self, table, attrs, vals):
        """Run MySQL insert operations"""
        # Prepare SQL query to INSERT a record into the database
        if len(vals) == 1:
            vals = '("' + vals[0] + '")'
        _sql = 'INSERT INTO %s (%s) VALUES %s' % \
            (table, ', '.join(attrs), vals)
        self.mysql_do(_sql)

    def get(self, table, attrs):
        """Get data"""
        # Prepare SQL query to READ a data from the table
        _sql = 'SELECT %s FROM %s' % (', '.join(attrs), table)
        try:
            # Execute the SQL command
            self.cursor.execute(_sql)
            # Fetch all the rows
            self.rows = self.cursor.fetchall()
            # Return fetched result
            return self.rows
        except:
            # Rollback in case there is any error
            self.db.rollback()

    def update(self, table, change, condition):
        """Update data"""
        # Prepare SQL query to UPDATE required records
        _sql = 'UPDATE %s SET %s WHERE %s' % (table, change, condition)
        self.mysql_do(_sql)

    def delete(self, table, condition):
        """Delete data"""
        # Prepare SQL query to DELETE required records
        _sql = 'DELETE FROM %s WHERE %s' % (table, condition)
        self.mysql_do(_sql)

    def close(self):
        """Disconnect from database"""
        self.db.close()

if __name__ == '__main__':
    testdb = MySQLORM()

    print('Connecting to database')
    testdb.connect('localhost', 'mysqluser', 'passwrd', 'TESTDB')

    print('Executing any query')
    testdb.mysql_do('drop table if exists Test')
    testdb.mysql_do('create table Test (Name text, Age int, Role text)')

    print('Inserting values')
    testdb.insert('Test', ('Name', 'Age', 'Role'), ('Dave', 22, 'Student'))
    testdb.insert('Test', ('Name', 'Age', 'Role'), ('Nick', 20, 'Student'))
    # don't forget leave coma in tuples
    testdb.insert('Test', ('Name',), ('Red',))

    print('Reading data')
    # don't forget leave coma in tuples
    for row in testdb.get('Test', ('Name', )):
        print row
    for row in testdb.get('Test', ('Name', 'Age')):
        print row

    print('Updating data')
    testdb.update('Test', 'Name = "Ben"', 'id = 3')

    print('Deleting data')
    testdb.delete('Test', 'Age = 33')

    testdb.close()
    print('Disconnected from database')
