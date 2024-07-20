"""

"""
from sqlite3 import dbapi2 as Database

class DB:
    def __init__(self, filename):
        """
        :attr filename: the path of the database
        :type filename: str
        :attr _conn: connection to the database
        :type _conn: Connection
        :attr _cursor: cursor for the database
        :type _cursor: Cursor
        """
        self.filename = filename
        self.is_open = False
        self._conn = None
        self._cursor = None
        self.open()
    
    def __str__(self):
        return f"{self.__class__.__name__}"
        
    def open(self):
        """Open database, return a connection to the database, set the cursor and conn attributes.
        """
        if not self.is_open:
            self._conn = Database.Connection(self.filename)
            self._cursor = self._conn.cursor()
            self.is_open = True
            return 
        self.is_open = False

    def close(self):
        """Close the connection to the database.
        """
        if self.is_open:
            self._conn.commit()
            self._conn.close()
            self.is_open = False



