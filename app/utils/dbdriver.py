# -*- coding: utf-8 -*-
#!/usr/bin/env python

import MySQLdb


class DBDriver(object):

    """This class can connect to MySQL databases and run CRUD operations"""

    def connect(self, host, username, password, db):
        """Connect to database"""
        self.db = MySQLdb.connect(host, username, password,
                                  db, use_unicode=True, charset='utf8')
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

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
        _sql = 'INSERT INTO %s (%s) VALUES %s' % \
            (table, ', '.join(attrs), self._extract_tuple(vals))
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

    def _extract_tuple(self, vals):
        """(self, tuple) -> string

        Return the string presentation of tuple
        for our sql query.
        """
        loop_index = 1
        val = '('
        for field in vals:
            if isinstance(field, int):
                val += str(field)
                if loop_index < len(vals):
                    val += ', '
            elif isinstance(field, str):
                val += '"' + field + '"'
                if loop_index < len(vals):
                    val += ', '
            loop_index += 1
        val += ')'

        return val


if __name__ == '__main__':
    testdb = DBDriver()

    #print('Connecting to database')
    # testdb.connect('localhost', 'root', pass, 'SMSDB')

    #print('Executing any query')
    #testdb.mysql_do('drop table if exists Test')
    #testdb.mysql_do('create table Test (Name VARCHAR(30))')

    #print('Inserting values')
    #testdb.insert('Test', ('Name'), ('Dave',))
    #testdb.insert('Test', ('Name', 'Age', 'Role'), ('Nick', 20, 'Student'))
    # don't forget leave coma in tuples
    #testdb.insert('Schools', ('name', 'address',), ('Школа 1', 'вул.Дубен2',))

    #print('Reading data')
    # don't forget leave coma in tuples
    # for row in testdb.get('Schools', ('name',)):
    #    print row
    # for row in testdb.get('Test', ('Name', 'Age')):
    #    print row

    #print('Updating data')
    #testdb.update('Subjects', 'name = "укр"', 'Name = "newnewnew"')

    #print('Deleting data')
    #testdb.delete('Test', 'Age = 33')

    # testdb.close()
    print('Disconnected from database')
