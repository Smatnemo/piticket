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
        
def main():
    db = DB('assets/piticket.db')
    fields = [Field('ord_id', 'INTEGER', primary_key=True, autoincrement=True), Field('product_id', 'INTEGER'), Field('price', 'FLOAT(6,2)')]
    order = Orders(db, fields)
    print(order)
    print(order.fetchone(1))
if __name__ == '__main__':
    main()