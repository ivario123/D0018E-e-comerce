from models import Item
from models.category import Category, CategoryGroup
from models.review import Review
from models.order import Order
from .. import ssql
from ssql_builder import SSqlBuilder as ssql_builder
from typing import List, Tuple,Dict
from mysql.connector.connection import MySQLConnection
from mysql.connector.connection import MySQLCursor


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


@ssql_builder.select(ssql, "REVIEW", ["Rating,Text,Email"])
def get_reviews_for(sn, sql_query=None, connection=None, cursor=None):
    # Gets all the reviews for a given product,
    cursor.execute(sql_query, (sn,))

    def get_uname(email):
        sql_query = "SELECT UserName FROM USER WHERE Email=%s"
        cursor.execute(sql_query, (email,))
        return cursor.fetchone()[0]
    ret = cursor.fetchall()
    if not ret:
        connection.rollback()
        return []

    return [Review.from_sql(x, get_uname(x[2])) for x in ret]


@ssql_builder.base(ssql)
def get_average_review_for(SN, connection=None, cursor=None):
    sql_query = "SELECT ROUND(AVG(Rating)) FROM REVIEW WHERE SN=%s;"
    cursor.execute(sql_query, (SN,))
    ret = cursor.fetchone()
    if ret:
        return ret[0]
    return 0


@ssql_builder.select(ssql, "REVIEW", ["Rating,Text,Email"])
def get_reviews_for(sn, sql_query=None, connection=None, cursor=None):
    # Gets all the reviews for a given product,
    cursor.execute(sql_query, (sn,))

    def get_uname(email):
        sql_query = "SELECT UserName FROM USER WHERE Email=%s"
        cursor.execute(sql_query, (email,))
        return cursor.fetchone()[0]
    ret = cursor.fetchall()
    if not ret:
        connection.rollback()
        return []

    return [Review.from_sql(x, get_uname(x[2])) for x in ret]


@ssql_builder.base(ssql)
def get_orders_for_user(Email: str, connection: MySQLConnection = None, cursor: MySQLCursor = None) -> Dict[int,List[Order]]:
    query = """SELECT PARCEL.NR AS parcelId,PARCEL.Address,PARCEL.Zip,PARCEL.Status,PRODUCT.ProductName,PRODUCT.Image,USERORDER.Amount,USERORDER.Price FROM PRODUCT 
INNER JOIN USERORDER  ON PRODUCT.SN = USERORDER.SN INNER JOIN  PARCEL ON USERORDER.PARCEL = PARCEL.NR WHERE USERORDER.Email=%s ORDER BY PARCEL.NR;;"""
    cursor.execute(query,(Email,))
    ret = cursor.fetchall()
    if not ret:
        return {}
    result:Dict[int,List[Order]] = {}
    for row in ret:
        (parcelId,_,_,_,_,_,_,_) = row
        if parcelId not in result.keys():
            result[parcelId] = []
        result[parcelId].append(Order(*row))
    return result



@ssql_builder.base(ssql)
def get_average_review_for(SN, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    sql_query = "SELECT ROUND(AVG(Rating)) FROM REVIEW WHERE SN=%s;"
    cursor.execute(sql_query, (SN,))
    ret = cursor.fetchone()
    if ret:
        return ret[0]
    return 0


@ssql_builder.select(ssql, "REVIEW", ["Rating","Text","Email"])
def get_reviews_for(sn, sql_query: str = None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    # Gets all the reviews for a given product,
    cursor.execute(sql_query, (sn,))

    def get_uname(email):
        sql_query = "SELECT UserName FROM USER WHERE Email=%s"
        cursor.execute(sql_query, (email,))
        return cursor.fetchone()[0]
    ret = cursor.fetchall()
    if not ret:
        connection.rollback()
        return []

    return [Review.from_sql(x, get_uname(x[2])) for x in ret]


@ssql_builder.base(ssql)
def get_cart_for_user(email: str, connection: MySQLConnection = None, cursor: MySQLCursor = None) -> List[Tuple[Item, int]]:
    query = f"""SELECT PRODUCT.ProductName,PRODUCT.ProductDescription,PRODUCT.Price,PRODUCT.Inventory,PRODUCT.Image,PRODUCT.SN,BASKET.Amount FROM PRODUCT INNER JOIN BASKET ON PRODUCT.SN = BASKET.SN WHERE BASKET.Email=%s ;"""
    cursor.execute(query, (email,))
    result = cursor.fetchall()
    if result:
        return [(item_from_sql(x), x[-1]) for x in result]
    return []


@ssql_builder.base(ssql)
def get_all_items_with_category(categories: List[str], connection: MySQLConnection = None, cursor: MySQLCursor = None):
    fmt = ",".join(['%s' for _ in categories])
    query = f"""SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE SN IN
        (SELECT SN FROM CATEGORY_ASSIGN WHERE Category IN ({fmt}) GROUP BY SN HAVING COUNT(*)={len(categories)}) ORDER BY ProductName;"""
    cursor.execute(
        query, categories)
    result = cursor.fetchall()
    if result:
        ret = [item_from_sql(item) for item in result]
        return ret
    else:
        return []


@ ssql_builder.base(ssql)
def get_all_items(connection: MySQLConnection = None, cursor: MySQLCursor = None):
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT;")
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return []


@ ssql_builder.select(ssql, table_name="PRODUCT", select_fields=["ProductName", "ProductDescription", "Price", "Inventory", "Image", "SN"])
def get_item_by_name(ProductName, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    cursor.execute(
        sql_query, (ProductName,))
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ ssql_builder.select(ssql, table_name="PRODUCT", select_fields=["ProductName", "ProductDescription", "Price", "Inventory", "Image", "SN"])
def get_item_by_serial_number(SN, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    cursor.execute(
        sql_query, (SN,))
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ ssql_builder.base(ssql)
def get_all_super_categories(connection: MySQLConnection = None, cursor: MySQLCursor = None):
    cursor.execute(
        "SELECT Name FROM SUPERCATEGORY;")
    result = cursor.fetchall()
    if result:
        return [item[0] for item in result]
    else:
        return []


@ ssql_builder.base(ssql)
def super_categories_and_sub(connection: MySQLConnection = None, cursor: MySQLCursor = None):
    cursor.execute(
        "SELECT Name FROM SUPERCATEGORY;")
    super = cursor.fetchall()
    cursor.execute(
        f"SELECT Name,Super FROM CATEGORY;")
    result = cursor.fetchall()
    category_groups = [
        CategoryGroup(x[0], []) for x in super
    ]
    if not result:
        return []
    super_cats = {
        x[0]: [] for x in super
    }
    for category in result:
        super_cats[category[1]].append(
            Category(category[0], supercategory=category[1]))
    for group in category_groups:
        group.categories = super_cats[group.name]
    return category_groups


@ssql_builder.select(ssql, table_name="PRODUCT", select_fields=["ProductName", "ProductDescription", "Price", "Inventory", "Image", "SN"])
def get_item_by_search_SN(SN, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    """
    Get an item by SN
    """
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE SN=%s;", (SN,))
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ssql_builder.select(ssql, table_name="PRODUCT", select_fields=["ProductName", "ProductDescription", "Price", "Inventory", "Image", "SN"])
def get_item_by_search_name(name, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None):
    """
    Get an item by name
    """
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE ProductName LIKE %s;", (name,))
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None
