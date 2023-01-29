"""
This file will need to be updated when the sql schemas are done.
"""
from models import Item
from models.category import CategoryGroup
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
        
@ssql_builder.select(ssql, table_name="PRODUCT", select_fields=["ProductName", "ProductDescription", "Price", "Inventory", "Image", "SN"])
def get_item_by_SN(SN, sql_query=None, connection=None, cursor=None):
    """
    Get an item by SN
    """
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE SN=%s;",(SN,))
    result = cursor.fetchall()
    print(result)
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ssql_builder.insert(ssql, "SUPERCATEGORY")
def create_supercategory(Name, sql_query=None, connection=None, cursor=None):
    """
    Create a supercategory
    """
    cursor.execute(
        sql_query, (Name,))
    # Check if the supercategory was created
    return True


@ssql_builder.base(ssql)
def get_all_supercategories(connection=None, cursor=None):
    """
    Get all supercategories
    """
    cursor.execute(
        "SELECT Name FROM SUPERCATEGORY;")
    result = cursor.fetchall()
    if result:
        return [item[0] for item in result]
    else:
        return []


@ssql_builder.insert(ssql, "CATEGORY")
def create_category(Name, Super, sql_query=None, connection=None, cursor=None):
    """
    Create a category
    """
    cursor.execute(
        sql_query, (Name, Super))

    print(cursor.rowcount, "record inserted.")
    # Check if the category was created
    return True


@ssql_builder.base(ssql)
def get_all_categories_grouped_by_supercategory(connection=None, cursor=None):
    """
    Get all categories grouped by supercategory
    """
    cursor.execute(
        "SELECT ANY_VALUE(Name),Super FROM CATEGORY GROUP BY Super;")
    result = cursor.fetchall()
    category_groups = []
    if not result:
        return []

    for cat in result:
        if cat[1] in category_groups:
            category_groups[cat[1]].categories.append(cat[0])
        else:
            category_groups.append(CategoryGroup(cat[1], [cat[0]]))
    return category_groups
