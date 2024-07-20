from model import Model
from database import DB
from model import Field

class Orders(Model):
    """This class represents the Orders table and inherits from Model"""
    def __init__(self, db, fields):
        Model.__init__(self, db, fields)

class WindowSettings(Model):
    """This setting is for Windows"""
    def __init__(self, db, fields):
        Model.__init__(self, db, fields)

