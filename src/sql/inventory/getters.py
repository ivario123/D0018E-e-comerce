from models import Item
from models.category import CategoryGroup
from .. import ssql
from ssql_builder import SSqlBuilder as ssql_builder
from typing import List


def item_from_sql(item):
    """
    Assumes that the item is in the following order:
    (
        ProductName,
        ProductDescription,
        Price,
        Inventory,
        Image,
        SN
    )
    """
    return Item(
        name=item[0],
        description=item[1],
        price=item[2],
        stock=item[3],
        image=item[4],
        serial_number=item[5]
    )


@ssql_builder.base(ssql)
def get_all_items_with_category(categories: List[str], connection=None, cursor=None):
    fmt = ",".join(['%s' for _ in categories])
    query = f"SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE SN IN (SELECT SN FROM CATEGORY_ASSIGN WHERE Category IN ({fmt}) GROUP BY SN HAVING COUNT(*)={len(categories)});"
    cursor.execute(
        query, categories)
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ ssql_builder.base(ssql)
def get_all_items(connection=None, cursor=None):
    # Not using ssql_builder.select because we do not provide a where clause which is required by the select function
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT;")
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ ssql_builder.select(ssql, table_name="PRODUCT", select_fields=["ProductName", "ProductDescription", "Price", "Inventory", "Image", "SN"])
def get_item_by_name(ProductName, sql_query=None, connection=None, cursor=None):
    cursor.execute(
        sql_query, (ProductName,))
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ ssql_builder.base(ssql)
def get_all_super_categories(connection=None, cursor=None):
    cursor.execute(
        "SELECT Name FROM SUPERCATEGORY;")
    result = cursor.fetchall()
    if result:
        return [item[0] for item in result]
    else:
        return []


@ ssql_builder.base(ssql)
def super_categories_and_sub(connection=None, cursor=None):
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
