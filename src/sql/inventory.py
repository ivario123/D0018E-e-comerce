"""
This file will need to be updated when the sql schemas are done.
"""
from models import Item
from . import ssql


def item_from_sql(item):
    return Item(
        name=item[0],
        description=item[1],
        price=item[2],
        stock=item[3],
        image=item[4],
        serial_number=item[5]
    )


def get_all_items():
    """
    Get all items
    """
    with ssql as (_conn, curs):
        curs.execute(
            "SELECT * FROM PRODUCT;")
        result = curs.fetchall()
        print(result)
        if result:
            return [item_from_sql(item) for item in result]
        else:
            return None


def get_item_by_name(name):
    """
    Get an item by name
    """
    with ssql as (_conn, curs):
        curs.execute(
            "SELECT  * FROM PRODUCT WHERE ProductName = %s;", (name,))
            #(ProductName,ProductDescription,Price,Inventory,Image,SN) FROM PRODUCT WHERE ProductName = %s;", (name,))
        result = curs.fetchall()
        print(result)
        if result:
            return [item_from_sql(item) for item in result]
        else:
            return None


def add_item(Item):
    """
    Add an item to the database
    """
    print(Item.fields())
    with ssql as (_conn, curs):
        curs.execute(
            "INSERT INTO PRODUCT (ProductName, ProductDescription, Price, Inventory, Image) VALUES ('test', 'test', 10, 10, 'test');",

        )
        return True
