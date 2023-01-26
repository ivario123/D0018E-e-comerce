"""
This file will need to be updated when the sql schemas are done.
"""
from models import Item
from . import ssql
from ssql_builder import SSqlBuilder as ssql_builder


def item_from_sql(item):
    return Item(
        name=item[0],
        description=item[1],
        price=item[2],
        stock=item[3],
        image=item[4],
        serial_number=item[5]
    )


@ssql_builder.insert(ssql, "PRODUCT")
def create_item(ProductName, ProductDescription, Price, Image, Inventory, sql_query=None, connection=None, cursor=None):
    """
    Create an item
    """
    cursor.execute(
        sql_query, (ProductName, ProductDescription, Price, Image, Inventory))
    # Check if the item was created
    if not get_item_by_name(ProductName):
        return False
    return True


@ssql_builder.base(ssql)
def get_all_items(connection=None, cursor=None):
    """
    Get all items
    """
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT;")
    result = cursor.fetchall()
    print(result)
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ssql_builder.select(ssql, table_name="PRODUCT", select_fields=["ProductName", "ProductDescription", "Price", "Inventory", "Image", "SN"])
def get_item_by_name(ProductName, sql_query=None, connection=None, cursor=None):
    """
    Get an item by name
    """
    cursor.execute(
        sql_query, (ProductName,))
    result = cursor.fetchall()
    print(result)
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None
