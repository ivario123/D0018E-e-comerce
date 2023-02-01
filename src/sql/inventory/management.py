"""
This file will need to be updated when the sql schemas are done.
"""
from models import Item
from models.category import CategoryGroup
from .. import ssql
from ssql_builder import SSqlBuilder as ssql_builder


@ssql_builder.insert(ssql, "PRODUCT")
def create_item(ProductName, ProductDescription, Price, Image, Inventory, sql_query=None, connection=None, cursor=None):
    """
    Create an item
    """
    cursor.execute(
        sql_query, (ProductName, ProductDescription, Price, Image, Inventory))
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "CATEGORY_ASSIGN")
def assign_category_to_item(SN, Category, sql_query=None, connection=None, cursor=None):
    """
    Assign a category to an item
    """
    cursor.execute(
        sql_query, (SN, Category))
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "SUPERCATEGORY")
def create_super_category(Name, sql_query=None, connection=None, cursor=None):
    """
    Create a super_category
    """
    cursor.execute(
        sql_query, (Name,))
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "CATEGORY")
def create_category(Name, Super, sql_query=None, connection=None, cursor=None):
    """
    Create a category
    """
    cursor.execute(
        sql_query, (Name, Super))
    return cursor.rowcount != 0
