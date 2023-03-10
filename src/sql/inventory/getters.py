from models.item import Item
from models.category import Category, CategoryGroup
from models.review import Review
from models.order import Order
from .. import ssql
from ssql_builder import SSqlBuilder as ssql_builder
from typing import List, Tuple, Dict
from mysql.connector.connection import MySQLConnection
from mysql.connector.connection import MySQLCursor


def item_from_sql(item, *args):
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
        serial_number=item[5],
    )


@ssql_builder.base(ssql)
def get_recommendations_for_user(
    UID: int, connection: MySQLConnection = None, cursor: MySQLCursor = None
) -> bool:
    similar_orders = """
SELECT USERORDER.PARCEL,COUNT(USERORDER.PARCEL) as similarity FROM USERORDER INNER JOIN PRODUCT ON USERORDER.SN = PRODUCT.SN 
	WHERE PRODUCT.SN IN (
		SELECT BASKET.SN FROM BASKET WHERE BASKET.UID = %s
	)
GROUP BY USERORDER.PARCEL ORDER BY similarity DESC;
"""
    product_query = """
SELECT PRODUCT.ProductName,PRODUCT.ProductDescription,PRODUCT.Price,PRODUCT.Inventory,PRODUCT.Image,PRODUCT.SN FROM PRODUCT RIGHT JOIN REVIEW ON REVIEW.SN=PRODUCT.SN  WHERE PRODUCT.SN IN(
SELECT USERORDER.SN FROM USERORDER JOIN PARCEL ON PARCEL.NR = USERORDER.PARCEL WHERE PARCEL.NR = %s AND USERORDER.SN NOT IN 
    (
        SELECT BASKET.SN FROM BASKET WHERE BASKET.UID=%s
    )
);
"""
    cursor.execute(similar_orders, (UID,))
    ret = cursor.fetchall()
    recommendations = []
    sns = {}
    cnt = 0
    # This search should not exceed ~2 orders since most orders are not identical
    for el in ret:
        (pid, _) = el
        cursor.execute(
            product_query,
            (
                pid,
                UID,
            ),
        )
        products = cursor.fetchall()
        # This is quite limited in depth, should not exceed ~10 products
        for product in products:
            sn = product[-1]
            if sn in sns.keys():
                continue
            sns[sn] = True
            recommendations.append(item_from_sql(product))
            cnt += 1
            if cnt == 4:
                return recommendations

    return recommendations


@ssql_builder.base(ssql)
def top5_products(
    connection: MySQLConnection = None, cursor: MySQLCursor = None
) -> List[Item]:
    query = """SELECT DISTINCT PRODUCT.ProductName,PRODUCT.ProductDescription,PRODUCT.Price,PRODUCT.Inventory,PRODUCT.Image,PRODUCT.SN,ROUND(AVG(REVIEW.Rating)) as Rating FROM PRODUCT LEFT JOIN REVIEW ON REVIEW.SN=PRODUCT.SN WHERE PRODUCT.Inventory > 0 AND Rating > 0 GROUP BY PRODUCT.SN ORDER BY Rating DESC LIMIT 4;"""
    cursor.execute(query)
    ret = cursor.fetchall()
    if not ret:
        return []

    def get_categories_for_sn(item: Item) -> Item:
        query = """SELECT SUPERCATEGORY.Name,CATEGORY.Name,SUPERCATEGORY.Color FROM SUPERCATEGORY INNER JOIN CATEGORY ON SUPERCATEGORY.ID=CATEGORY.SID INNER JOIN CATEGORY_ASSIGN ON CATEGORY_ASSIGN.Category=CATEGORY.Name WHERE CATEGORY_ASSIGN.SN = %s;"""

        cursor.execute(query, (item.serial_number,))
        item.assign_categories(
            [
                CategoryGroup(x[0], x[2], [Category(x[1], x[0])])
                for x in cursor.fetchall()
            ]
        )
        return item

    res = [item_from_sql(item) for item in ret]
    res = [get_categories_for_sn(item) for item in res]
    return res


@ssql_builder.base(ssql)
def get_average_review_for(
    SN, connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    sql_query = "SELECT ROUND(AVG(Rating)) FROM REVIEW WHERE SN=%s;"
    cursor.execute(sql_query, (SN,))
    ret = cursor.fetchone()
    if ret:
        return ret[0]
    return 0


@ssql_builder.select(ssql, "REVIEW", ["Rating,Text,UID"])
def get_reviews_for(
    sn, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    # Gets all the reviews for a given product,
    cursor.execute(sql_query, (sn,))

    def get_uname(UID):
        sql_query = "SELECT UserName,Email FROM USER WHERE UID=%s"
        cursor.execute(sql_query, (UID,))
        return cursor.fetchone()

    ret = cursor.fetchall()
    if not ret:
        connection.rollback()
        return []

    return [Review.from_sql(x, *get_uname(x[2])) for x in ret]


@ssql_builder.base(ssql)
def get_orders_for_user(
    UID: str, connection: MySQLConnection = None, cursor: MySQLCursor = None
) -> Dict[int, List[Order]]:
    query = """SELECT PARCEL.NR AS parcelId,PARCEL.Address,PARCEL.Zip,PARCEL.Status,PRODUCT.ProductName,PRODUCT.Image,USERORDER.Amount,USERORDER.Price FROM PRODUCT 
INNER JOIN USERORDER  ON PRODUCT.SN = USERORDER.SN INNER JOIN  PARCEL ON USERORDER.PARCEL = PARCEL.NR WHERE USERORDER.UID=%s ORDER BY PARCEL.NR;"""
    cursor.execute(query, (UID,))
    ret = cursor.fetchall()
    if not ret:
        return {}
    result: Dict[int, List[Order]] = {}
    for row in ret:
        (parcelId, _, _, _, _, _, _, _) = row
        if parcelId not in result.keys():
            result[parcelId] = []
        result[parcelId].append(Order(*row))
    return result


@ssql_builder.base(ssql)
def get_all_orders(
    connection: MySQLConnection = None, cursor: MySQLCursor = None
) -> Dict[int, List[Order]]:
    cursor.execute(
        "SELECT PARCEL.NR AS parcelId,PARCEL.Address,PARCEL.Zip,PARCEL.Status,PRODUCT.ProductName,PRODUCT.Image,USERORDER.Amount,USERORDER.Price FROM PRODUCT INNER JOIN USERORDER ON PRODUCT.SN = USERORDER.SN INNER JOIN PARCEL ON USERORDER.PARCEL = PARCEL.NR ORDER BY PARCEL.NR;"
    )
    ret = cursor.fetchall()
    print(ret)
    if not ret:
        return {}
    result: Dict[int, List[Order]] = {}
    for row in ret:
        (parcelId, _, _, _, _, _, _, _) = row
        if parcelId not in result.keys():
            result[parcelId] = []
        result[parcelId].append(Order(*row))
    return result


@ssql_builder.base(ssql)
def get_average_review_for(
    SN, connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    sql_query = "SELECT ROUND(AVG(Rating)) FROM REVIEW WHERE SN=%s;"
    cursor.execute(sql_query, (SN,))
    ret = cursor.fetchone()
    if ret:
        return ret[0]
    return 0


@ssql_builder.base(ssql)
def get_cart_for_user(
    uid: int, connection: MySQLConnection = None, cursor: MySQLCursor = None
) -> List[Tuple[Item, int]]:
    query = f"""SELECT PRODUCT.ProductName,PRODUCT.ProductDescription,PRODUCT.Price,PRODUCT.Inventory,PRODUCT.Image,PRODUCT.SN,BASKET.Amount FROM PRODUCT INNER JOIN BASKET ON PRODUCT.SN = BASKET.SN WHERE BASKET.UID=%s ;"""
    cursor.execute(query, (uid,))
    result = cursor.fetchall()
    if result:
        return [(item_from_sql(x), x[-1]) for x in result]
    return []


@ssql_builder.base(ssql)
def get_all_items_with_category(
    categories: List[str],
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    fmt = ",".join(["%s" for _ in categories])
    query = f"""SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE SN IN
        (SELECT SN FROM CATEGORY_ASSIGN INNER JOIN CATEGORY ON CATEGORY_ASSIGN.Category=CATEGORY.id WHERE CATEGORY.Name IN ({fmt}) GROUP BY SN HAVING COUNT(*)={len(categories)}) ORDER BY ProductName;"""
    cursor.execute(query, categories)
    result = cursor.fetchall()
    if not result:
        return []

    res = [item_from_sql(item) for item in result]

    def get_categories_for_sn(item: Item) -> Item:
        query = """SELECT SUPERCATEGORY.Name,CATEGORY.Name,SUPERCATEGORY.Color,CATEGORY.ID,CATEGORY.SID FROM SUPERCATEGORY INNER JOIN CATEGORY ON SUPERCATEGORY.ID=CATEGORY.SID INNER JOIN CATEGORY_ASSIGN ON CATEGORY_ASSIGN.Category=CATEGORY.ID WHERE CATEGORY_ASSIGN.SN = %s;"""

        cursor.execute(query, (item.serial_number,))
        item.assign_categories(
            [
                CategoryGroup(x[4], x[0], x[2], [Category(x[3], x[1], x[4])])
                for x in cursor.fetchall()
            ]
        )
        return item

    res = [get_categories_for_sn(item) for item in res]
    return res


@ssql_builder.base(ssql)
def get_all_items(connection: MySQLConnection = None, cursor: MySQLCursor = None):
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT;"
    )
    result = cursor.fetchall()
    if not result:
        return []

    res = [item_from_sql(item) for item in result]

    def get_categories_for_sn(item: Item) -> Item:
        query = """SELECT SUPERCATEGORY.Name,CATEGORY.Name,SUPERCATEGORY.Color,SUPERCATEGORY.ID,CATEGORY.ID FROM SUPERCATEGORY INNER JOIN CATEGORY ON SUPERCATEGORY.ID=CATEGORY.SID INNER JOIN CATEGORY_ASSIGN ON CATEGORY_ASSIGN.Category=CATEGORY.ID WHERE CATEGORY_ASSIGN.SN = %s;"""

        cursor.execute(query, (item.serial_number,))
        item.assign_categories(
            [
                CategoryGroup(x[4], x[0], x[2], [Category(x[3], x[1], x[4])])
                for x in cursor.fetchall()
            ]
        )
        return item

    res = [get_categories_for_sn(item) for item in res]
    return res


@ssql_builder.select(
    ssql,
    table_name="PRODUCT",
    select_fields=[
        "ProductName",
        "ProductDescription",
        "Price",
        "Inventory",
        "Image",
        "SN",
    ],
)
def get_item_by_name(
    ProductName,
    sql_query=None,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    cursor.execute(sql_query, (ProductName,))
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ssql_builder.select(
    ssql,
    table_name="PRODUCT",
    select_fields=[
        "ProductName",
        "ProductDescription",
        "Price",
        "Inventory",
        "Image",
        "SN",
    ],
)
def get_item_by_serial_number(
    SN, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    cursor.execute(sql_query, (SN,))
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ssql_builder.base(ssql)
def get_all_super_categories_for_categories(
    categories: list[str],
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    fmt = ",".join(["%s" for _ in categories])
    query = f"""SELECT SUPERCATEGORY.ID,SUPERCATEGORY.Name,SUPERCATEGORY.Color,CATEGORY.Name,CATEGORY.ID FROM SUPERCATEGORY INNER JOIN CATEGORY ON SUPERCATEGORY.ID=CATEGORY.SID WHERE CATEGORY.Name IN ({fmt});"""
    cursor.execute(query, categories)

    ret = cursor.fetchall()
    if not ret:
        return []
    return [CategoryGroup(x[0], x[1], x[2], [Category(x[4], x[3], x[0])]) for x in ret]


@ssql_builder.base(ssql)
def get_all_super_categories(
    connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    cursor.execute("SELECT Name,ID FROM SUPERCATEGORY;")
    result = cursor.fetchall()
    if result:
        return result  # [item for item in result]
    else:
        return []


@ssql_builder.base(ssql)
def super_categories_and_sub(
    connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    cursor.execute("SELECT ID,Name,Color FROM SUPERCATEGORY;")
    super = cursor.fetchall()
    cursor.execute(f"SELECT ID,Name,SID FROM CATEGORY;")
    result = cursor.fetchall()
    category_groups = [CategoryGroup(*x, []) for x in super]
    if not result and not super:
        return []
    super_cats = {x[0]: [] for x in super}
    for category in result:
        super_cats[category[2]].append(Category(*category))
    for group in category_groups:
        group.categories = super_cats[group.id]
    return category_groups


@ssql_builder.select(
    ssql,
    table_name="PRODUCT",
    select_fields=[
        "ProductName",
        "ProductDescription",
        "Price",
        "Inventory",
        "Image",
        "SN",
    ],
)
def get_item_by_search_SN(
    SN, sql_query=None, connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    """
    Get an item by SN
    """
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE SN=%s;",
        (SN,),
    )
    result = cursor.fetchall()
    if result:
        return [item_from_sql(item) for item in result]
    else:
        return None


@ssql_builder.base(ssql)
def get_item_by_search_name(
    name, connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    """
    Get an item by name
    """
    cursor.execute(
        "SELECT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE ProductName LIKE %s;",
        (name,),
    )
    result = cursor.fetchall()

    def get_categories_for_sn(item: Item) -> Item:
        query = """SELECT SUPERCATEGORY.Name,CATEGORY.Name,SUPERCATEGORY.Color,CATEGORY.ID,CATEGORY.SID FROM SUPERCATEGORY INNER JOIN CATEGORY ON SUPERCATEGORY.ID=CATEGORY.SID INNER JOIN CATEGORY_ASSIGN ON CATEGORY_ASSIGN.Category=CATEGORY.ID WHERE CATEGORY_ASSIGN.SN = %s;"""

        cursor.execute(query, (item.serial_number,))
        item.assign_categories(
            [
                CategoryGroup(x[4], x[0], x[2], [Category(x[3], x[1], x[4])])
                for x in cursor.fetchall()
            ]
        )
        return item

    if result:
        ret = [item_from_sql(item) for item in result]
        ret = [get_categories_for_sn(item) for item in ret]
        return ret
    else:
        return []


@ssql_builder.base(ssql)
def get_all_items_with_super(
    super, connection: MySQLConnection = None, cursor: MySQLCursor = None
):
    cursor.execute(
        "SELECT DISTINCT ProductName,ProductDescription,Price,Inventory,Image,SN FROM PRODUCT WHERE SN IN (SELECT SN FROM CATEGORY_ASSIGN INNER JOIN CATEGORY ON CATEGORY_ASSIGN.Category = CATEGORY.ID INNER JOIN SUPERCATEGORY ON SUPERCATEGORY.ID = CATEGORY.SID WHERE CATEGORY.Name LIKE %s);",
        (super,),
    )
    result = cursor.fetchall()

    def get_categories_for_sn(item: Item) -> Item:
        query = """SELECT SUPERCATEGORY.Name,CATEGORY.Name,SUPERCATEGORY.Color,CATEGORY.ID,CATEGORY.SID FROM SUPERCATEGORY INNER JOIN CATEGORY ON SUPERCATEGORY.ID=CATEGORY.SID INNER JOIN CATEGORY_ASSIGN ON CATEGORY_ASSIGN.Category=CATEGORY.ID WHERE CATEGORY_ASSIGN.SN = %s;"""

        cursor.execute(query, (item.serial_number,))
        item.assign_categories(
            [
                CategoryGroup(x[4], x[0], x[2], [Category(x[3], x[1], x[4])])
                for x in cursor.fetchall()
            ]
        )
        return item

    if result:
        ret = [item_from_sql(item) for item in result]
        ret = [get_categories_for_sn(item) for item in ret]
        return ret
    else:
        return []


@ssql_builder.base(ssql)
def search_get_categories(SN: List[int], connection=None, cursor=None):
    list_SN = ",".join(["%s" for _ in SN])

    query = f"""SELECT DISTINCT SUPERCATEGORY.ID,SUPERCATEGORY.Name,SUPERCATEGORY.Color FROM SUPERCATEGORY INNER JOIN CATEGORY ON CATEGORY.SID=SUPERCATEGORY.ID INNER JOIN CATEGORY_ASSIGN ON CATEGORY.ID = CATEGORY_ASSIGN.Category WHERE SN in ({list_SN});"""
    cursor.execute(query, SN)
    super = cursor.fetchall()
    if not super:
        return []

    query = f"""SELECT DISTINCT CATEGORY.ID, CATEGORY.name, CATEGORY.SID FROM CATEGORY INNER JOIN CATEGORY_ASSIGN ON CATEGORY.ID = CATEGORY_ASSIGN.Category WHERE SN in ({list_SN});"""
    cursor.execute(query, SN)
    result = cursor.fetchall()

    category_groups = [CategoryGroup(*x, []) for x in super]
    if not result:
        return []
    super_cats = {x[0]: [] for x in super}
    for category in result:
        super_cats[category[-1]].append(Category(*category))
    for group in category_groups:
        group.categories = super_cats[group.id]
    return category_groups
