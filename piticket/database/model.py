

class Model:
    def __init__(self, db, fields):
        """
        :attr _db: dabatabase object to represent a session
        :type _db: piticket.database.DB
        :attr _records: a list of record objects
        :type _records: list
        :attr fields: a list of Field objects used to create the fields
        :type fields: list
        :attr column_names: a list of column names
        :type column_names: list
        :attr column_description: description of all the columns. A tuple of tuples. Each tuple has seven values 
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
        self._updated = False
        self.create()
        self.fetchall()

    def __len__(self):
        return len(self._records)

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
        for column_name in self.column_names:
            query += f" {column_name},"
        query = query.strip(',')
        query += ") VALUES ("
        for i in range(len(self.column_names)):
            query += " ?,"
        query = query.strip(',')
        query += ");"
        # Execute query in the database
        self._db.open()
        self._db._cursor.execute(query, data)
        self._db.close()
        
    def update(self):
        pass
    
    def delete(self):
        pass 

    def create(self):
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
    
    def fetchone(self, column, value):
        """Find and return a return a record given its id.
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
        self.column_names = list(map(lambda x: x[0], 
                                self._db._cursor.description))
        self.column_description = self._db._cusor.description
        records = self._db._cursor.fetchall()
        self._db.close()
        for record in records:
            record_dict = {}
            for k, v in zip(self.column_names, record):
                record_dict[k]=v 
            self._records.append(Record(self.__class__.__name__,**record_dict))
        
            
class Record():
    def __init__(self, table, **kwargs):
        self.data = kwargs
        self.table = table

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
    def __init__(
        self, name, f_type, null=False, primary_key=False, autoincrement=False, foreign_key=False
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
        return "<name:{},type:{},primary_key:{},autoincrement:{},foreign_key:{}>"\
        .format(self.name,self.type,self.primary_key,self.autoincrement,self.foreign_key)
    
    def create(self):
        self.params += self.type
        if self.primary_key:
            self.params += ' PRIMARY KEY'
        if self.autoincrement:
            self.params += ' AUTOINCREMENT'
        if self.null:
            self.params += ' NULL'
        else:
            self.params += ' NOT NULL'
        if self.foreign_key:
            self.params += ' '
        

    



