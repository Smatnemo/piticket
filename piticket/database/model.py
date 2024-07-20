import sqlite3

class Model:
    def __init__(self, db, fields):
        """
        :attr _db: dabatabase object to represent a session
        :type _db: piticket.database.DB
        :attr _records: a list of record objects
        :type _records: list
        :attr fields: a list of Field objects used to create the fields
        :type fields: list
        :attr column_names: a list of column names queried after creating a model or adding a column
        :type column_names: list
        :attr column_description: description of all the columns. A tuple of tuples.
        Attribute is updated when the table is created or a column is added. 
        Each tuple has seven values 
                name
                type_code
                display_size
                internal_size
                precision
                scale
                null_ok
        :type column_description: tuple
        """
        self._db = db 
        self.fields = fields
        self.column_names = []
        self.column_description = ()
        self._records = []
        self._rows_updated = False
        self._metadata_updated = False 
        self.create_table()
        self._update()

    def __str__(self):
        return f"<Table:{self.__class__.__name__}, Column Description:{self.column_description}>"

    def __len__(self):
        return len(self._records)

    def _update(self):
        """Update this current model object"""
        self._update_metadata()
        self._update_records()

    def _update_records(self):
        """Update the list of records"""
        if self._rows_updated:
            records = self.fetchall()
            for record in records:
                record_dict = {}
                for k, v in zip(self.column_names, record):
                    record_dict[k]=v 
                self._records.append(Record(self.__class__.__name__,**record_dict))
        self._rows_updated = False

    def _update_metadata(self):
        """"""
        if self._metadata_updated:
            query = f"SELECT * FROM {self.__class__.__name__}"
            self._db.open()
            self._db._cursor.execute(query)
            # Create a list of valid field names when fetching data
            self.column_names = list(map(lambda x: x[0], 
                                    self._db._cursor.description))
            self.column_description = self._db._cursor.description
            self._db.close()
        self._metadata_updated = False

    def add_column(self, field):
        """Add a new column to the table"""
        query = f"ALTER TABLE ADD {field.name}"
        self._metadata_updated = True 
        self._update()

    def execute(self, query, data=()):
        self._db.open()
        if self._db.is_open:
            self._db._cursor.execute(query, data)
    
    def insert(self, **kwargs):
        """Insert data into a table using the class name.
        :param kwargs: dictionary with key as the name of the column and 
                        the value as data to be inserted
        :type kwargs: dictionary
        """
        # Created query
        query = f"""INSERT INTO {self.__class__.__name__} ("""
        data = []
        for key, value in kwargs.items():
            if self.column_names and key not in self.column_names:
                raise ValueError('Column name {} is not a valid field'.format(key))
            query += f" {key},"
            data.append(value)
        query = query.strip(',')
        query += ") VALUES ("
        for i in range(len(kwargs)):
            query += " ?,"
        query = query.strip(',')
        query += ");"

        data = tuple(data)
        # Execute query in the database
        self._db.open()
        try:
            self._db._cursor.execute(query, data)
        except sqlite3.IntegrityError as ex:
            print('Record exists: ', ex)
        self._db.close()
        # Updated Model
        self._rows_updated = True
        
    def update(self, id, **kwargs):
        """Update a record in a table given its id, the column name to be updated
        and value to change."""
        query = f"UPDATE {self.__class__.__name__} SET"
        for k,v in kwargs.items():
            query += f" {k}='{v}'"
        f" WHERE {self.column_names[0]}={id}"
        self._db.open()
        self._db._cursor.execute(query,data)
        self._db.close()
        self._rows_updated = True 
        # self._update()
        
    def delete(self):
        pass 

    def create_table(self):
        """Create a table from a subclass class' name.
        :param fields: a list of fields to be created
        :type fields: list
        """
        # Query used to create table from class name
        query = f"""Create table if not exists {self.__class__.__name__} ("""
        for field in self.fields:
            query += f" {field.name} {field.params}, "
        query = query.strip(', ')
        query += ");" 
        self._db.open()
        self._db._cursor.execute(query)
        self._db.close()
        self._metadata_updated = True
    
    def fetchone(self, column, value):
        """Find and return a record given its id.
        """
        for record in self._records:
            if hasattr(record, column):
                if getattr(record, column) == value:
                    return record

    def fetchall(self):
        """Find and return all the records.
        """
        query = f"""SELECT * FROM {self.__class__.__name__}"""
        self._db.open()
        self._db._cursor.execute(query)
        records = self._db._cursor.fetchall()
        self._db.close()
        return records
        
            
class Record():
    """A record represents a row of a table. It cannot modify a table. Each record is updated
        when the database table is updated.
    :attr data: This holds a dictionary of key value pairs, where the key is the name of
                 the column and the value is the value of that field
    :type data: dict
    :attr table: the name of the table a record is in
    :type table: str§§§                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    """
    def __init__(self, table, **kwargs):
        self.data = kwargs
        self.table = table  
        self.updated = False

    def __str__(self):
        """Dynamically generate and add the name of the columns"""
        return "<Table:{}, Record:{}>".format(self.table, self.data)
    
    def __repr__(self):
        """Use str repr here to dynamically represent the object"""
        return self.__str__()

    def __setattr__(self, name, value):
        """Called every time an attribute is set.
        """
        if name != 'data' and name in self.data:
            self.__setitem__(name, value)
        else:
            super(Record, self).__setattr__(name, value)

    def __setitem__(self, name, value):
        """"""
        if name not in self.data:
            raise ValueError('Column name {} not in {} table'.format(name, self.table))
        self.data[name] = value

    def __getitem__(self, name):
        """Return value from internal dictionary"""
        if name not in self.data:
            raise ValueError('Column name {} not in {} table'.format(name, self.table))
        return self.data[name]

    def __getattr__(self, name):
        """Return value of name from data or attribute"""
        return self.__getitem__(name)



class Field:
    """Use field to create columns in database. Give name and type at least to describe a field.
    All fields should be nullable to make it easy to create. only the primary field should not be
    null.
    """
    def __init__(
        self, name, f_type, null=True, primary_key=False, autoincrement=False, foreign_key=False
        ):
        self.name = name 
        self.type = f_type
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.foreign_key = foreign_key
        self.null = null 
        self.params = ''
        self.create()

    def __str__(self):
        return "<name:{},type:{},null:{},primary_key:{},autoincrement:{},foreign_key:{}>"\
        .format(self.name,self.type,self.null,self.primary_key,self.autoincrement,self.foreign_key)
    
    def create(self):
        self.params += self.type
        if self.primary_key:
            self.null = False
            self.params += ' PRIMARY KEY'
        if self.autoincrement:
            self.params += ' AUTOINCREMENT'
        if self.null:
            self.params += ' NULL'
        else:
            self.params += ' NOT NULL'
        if self.foreign_key:
            self.params += ' '
        

    



