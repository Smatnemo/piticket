

class Model:
    def __init__(self, db, fields):
        """
        :attr _db: dabatabase object to represent a session
        :type _db: piticket.database.DB
        :attr _records: a list of record objects
        :type _records: list
        :a
        """
        self._db = db 
        self.fields = fields
        self._records = []
        self.create()

    def __len__(self):
        pass

    def execute(self, query, data=()):
        self._db.open()
        if self._db.is_open:
            self._db._cursor.execute(query, data)
            return self._db._cursor.fetchall()
    
    def insert(self):
        pass 
    
    def update(self):
        pass
    
    def delete(self):
        pass 

    def create(self):
        """Create a table from a subclass class' name.
        :param fields: a list of fields to be created
        :type fields: list
        """
        query = f"""Create table if not exists {self.__class__.__name__} ("""
        for field in self.fields:
            query += f" {field.name} {field.params}, "
        query = query.strip(', ')
        query += ");" 
        self.execute(query)
        self._db.close()
    
    def fetchone(self, id):
        """Find and return a return a record given its id.
        """
        query = f"""SELECT * FROM {self.__class__.__name__}
                WHERE ord_id = {id}"""
        record = self.execute(query)
        
        print(record)
        return Record(self.__class__.__name__)

    def fetchall(self):
        """Find and return all the records.
        """
        return [Record() for record in self._records]


class Record:
    def __init__(self, table, **kwargs):
        self.data = kwargs
        self.table = table
        self.record_id = 1

    def __str__(self):
        """Dynamically generate and add the name of the columns"""
        return "<Record id:{}, Table:{}>".format(self.record_id,self.table)

    def __setattr__(self, name, value):
        """Called every time an attribute is set.
        """
        if name != 'data' and name in self.data:
            self.data[name] = value
        else:
            super(Record, self).__setattr__(name, value)

    def create(self):
        pass 


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
        

    



