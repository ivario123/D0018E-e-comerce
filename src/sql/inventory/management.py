"""
This file will need to be updated when the sql schemas are done.
"""
from .. import ssql
from mysql.connector.connection import MySQLConnection
from mysql.connector.connection import MySQLCursor
from ssql_builder import SSqlBuilder as ssql_builder


@ssql_builder.insert(ssql, "REVIEW")
def create_review(
    SN, Text, Rating, Email, sql_query=None, connection=None, cursor=None
):
    cursor.execute(
        sql_query,
        (
            SN,
            Text,
            Rating,
            Email,
        ),
    )
    return True


@ssql_builder.base(ssql)
def update_review(
    SerialNumber: str,
    Review: str,
    Email: str,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    print(
        f"UPDATE REVIEW SET REVIEW.Text = {Review} WHERE REVIEW.SN = {SerialNumber} AND REVIEW.Email = {Email};"
    )
    cursor.execute(
        "UPDATE REVIEW SET REVIEW.Text = %s WHERE REVIEW.SN = %s AND REVIEW.Email = %s;",
        (
            Review,
            SerialNumber,
            Email,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def delete_review(
    SerialNumber: str,
    Email: str,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    cursor.execute(
        "DELETE FROM REVIEW WHERE SN = %s AND Email = %s;",
        (
            SerialNumber,
            Email,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def checkout_basket(
    Address: str,
    Zip: int,
    Email: int,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
) -> bool:
    """
    Creates a new parcel, adds orders to it, removes all relevant lines from basket.
    """
    # Raise exceptions to force rollback if any errors
    create_parcel_query = "INSERT INTO PARCEL (Address,Zip) VALUE (%s,%s);"
    insert_query = "INSERT INTO USERORDER (Email,SN,Amount,PARCEL,Price) SELECT %s,BASKET.SN,BASKET.Amount, PARCEL.NR,PRODUCT.Price FROM PARCEL,BASKET INNER JOIN PRODUCT ON PRODUCT.SN = BASKET.SN WHERE NR = LAST_INSERT_ID() AND BASKET.Email = %s;"
    update_stock = "UPDATE PRODUCT JOIN BASKET ON PRODUCT.SN = BASKET.SN SET PRODUCT.Inventory = PRODUCT.Inventory - BASKET.Amount WHERE BASKET.Email=%s;"
    remove_query = "DELETE FROM BASKET WHERE BASKET.Email=%s;"
    cursor.execute(
        create_parcel_query,
        (
            Address,
            Zip,
        ),
    )
    if cursor.rowcount == 0:
        raise Exception("Invalid parcel creation")
    cursor.execute(
        insert_query,
        (
            Email,
            Email,
        ),
    )
    if cursor.rowcount == 0:
        raise Exception("Invalid order creation")
    cursor.execute(update_stock, (Email,))
    if cursor.rowcount == 0:
        raise Exception("Invalid stock adjustment")
    cursor.execute(remove_query, (Email,))
    if cursor.rowcount == 0:
        raise Exception("Invalid clear basket")
    return True


@ssql_builder.base(ssql)
def category_name_change(
    Type: str,
    NewName: str,
    OldName: str,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
) -> bool:
    lbl = "SUPERCATEGORY" if Type == "grp" else "CATEGORY"
    query = f"""UPDATE {lbl} SET {lbl}.Name=%s WHERE {lbl}.Name = %s;"""

    cursor.execute(
        query,
        (
            NewName,
            OldName,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def update_super_category_color_by_name(
    Name: str,
    Color: str,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
) -> bool:
    print(Name)
    query = """UPDATE SUPERCATEGORY SET SUPERCATEGORY.COLOR=%s WHERE SUPERCATEGORY.Name = %s;"""

    cursor.execute(
        query,
        (
            Color,
            Name,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def delete_category_by_name(
    CategoryName: str,
    Type: str,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
) -> bool:
    lbl = "SUPERCATEGORY" if Type == "grp" else "CATEGORY"
    query = f"""DELETE FROM {lbl} WHERE {lbl}.Name = %s;"""

    cursor.execute(
        query,
        (CategoryName,),
    )
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def update_stock(
    SN: int, Stock: int, connection: MySQLConnection = None, cursor: MySQLCursor = None
) -> bool:
    query = """UPDATE PRODUCT SET PRODUCT.Inventory = %s WHERE PRODUCT.SN = %s;"""
    cursor.execute(
        query,
        (
            Stock,
            SN,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def update_price(
    SN: int, Price: int, connection: MySQLConnection = None, cursor: MySQLCursor = None
) -> bool:
    query = """UPDATE PRODUCT SET PRODUCT.Price=%s WHERE PRODUCT.SN = %s;"""
    cursor.execute(
        query,
        (
            Price,
            SN,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def add_to_basket(
    Email: str,
    ProductName: str,
    Amount: int,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
) -> bool:
    query = """INSERT INTO BASKET (SN,Email,Amount) VALUES ((SELECT SN FROM PRODUCT WHERE ProductName=%s),%s,%s);"""
    cursor.execute(query, (ProductName, Email, Amount))
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def remove_element_from_basket(
    Email: str,
    ProductName: str,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
) -> bool:
    query = """DELETE FROM BASKET WHERE BASKET.Email=%s AND BASKET.SN=(SELECT SN FROM PRODUCT WHERE PRODUCT.ProductName=%s);"""
    cursor.execute(
        query,
        (
            Email,
            ProductName,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.base(ssql)
def update_basket(
    Email: str,
    ProductName: str,
    Amount: int,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
) -> bool:
    query = """UPDATE BASKET SET BASKET.Amount=%s WHERE BASKET.Email=%s AND BASKET.SN=(SELECT SN FROM PRODUCT WHERE PRODUCT.ProductName=%s);"""
    cursor.execute(
        query,
        (
            Amount,
            Email,
            ProductName,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "PRODUCT")
def create_item(
    ProductName,
    ProductDescription,
    Price,
    Image,
    Inventory,
    sql_query=None,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    """
    Create an item
    """
    cursor.execute(
        sql_query, (ProductName, ProductDescription, Price, Image, Inventory)
    )
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "CATEGORY_ASSIGN")
def assign_category_to_item(
    SN,
    Category,
    sql_query=None,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    """
    Assign a category to an item
    """
    cursor.execute(sql_query, (SN, Category))
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "SUPERCATEGORY")
def create_super_category(
    Name: str,
    Color: str,
    sql_query=None,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    """
    Create a super_category
    """
    cursor.execute(
        sql_query,
        (
            Name,
            Color,
        ),
    )
    return cursor.rowcount != 0


@ssql_builder.insert(ssql, "CATEGORY")
def create_category(
    Name,
    Super,
    sql_query=None,
    connection: MySQLConnection = None,
    cursor: MySQLCursor = None,
):
    """
    Create a category
    """
    cursor.execute(sql_query, (Name, Super))
    return cursor.rowcount != 0
