"""
This file will need to be updated when the sql schemas are done.
"""
from models import Item
from models.category import CategoryGroup
from .. import ssql
from mysql.connector.connection import MySQLConnection
from mysql.connector.connection import MySQLCursor
from ssql_builder import SSqlBuilder as ssql_builder


@ssql_builder.insert(ssql, "REVIEW")
def create_review(SN, Text, Rating, Email, sql_query=None, connection=None, cursor=None):
    cursor.execute(sql_query, (SN, Text, Rating, Email,))


@ssql_builder.base(ssql)
def add_to_basket(Email: str, ProductName: str, Amount: int, connection: MySQLConnection = None, cursor: MySQLCursor = None) -> bool:
    query = """INSERT INTO BASKET (SN,Email,Amount) VALUES ((SELECT SN FROM PRODUCT WHERE ProductName=%s),%s,%s);"""
    print(query, (ProductName, Email, Amount))
    cursor.execute(query, (ProductName, Email, Amount))

    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def remove_element_from_basket(Email: str, ProductName: str, connection: MySQLConnection = None, cursor: MySQLCursor = None) -> bool:
    query = """DELETE FROM BASKET WHERE BASKET.Email=%s AND BASKET.SN=(SELECT SN FROM PRODUCT WHERE PRODUCT.ProductName=%s);"""
    cursor.execute(query, (Email, ProductName,))
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def update_basket(Email: str, ProductName: str, Amount: int, connection: MySQLConnection = None, cursor: MySQLCursor = None) -> bool:
    query = """UPDATE BASKET SET BASKET.Amount=%s WHERE BASKET.Email=%s AND BASKET.SN=(SELECT SN FROM PRODUCT WHERE PRODUCT.ProductName=%s);"""
    cursor.execute(query, (Amount, Email, ProductName,))
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "PRODUCT")
def create_item(ProductName, ProductDescription, Price, Image, Inventory, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    """
    Create an item
    """
    cursor.execute(
        sql_query, (ProductName, ProductDescription, Price, Image, Inventory))
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "CATEGORY_ASSIGN")
def assign_category_to_item(SN, Category, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    """
    Assign a category to an item
    """
    cursor.execute(
        sql_query, (SN, Category))
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "SUPERCATEGORY")
def create_super_category(Name, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    """
    Create a super_category
    """
    cursor.execute(
        sql_query, (Name,))
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "CATEGORY")
def create_category(Name, Super, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    """
    Create a category
    """
    cursor.execute(
        sql_query, (Name, Super))
    return cursor.rowcount != 0
