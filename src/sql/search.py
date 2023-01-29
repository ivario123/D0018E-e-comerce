from models import Item
from result import Result, Error, Ok
from . import ssql
from ssql_builder import SSqlBuilder as ssql_builder



@ssql_builder.select(ssql, table_name="PRODUCT", select_fields=["SN"])
def get_products(search_input, sql_query=None, connection=None, cursor=None):
    cursor.execute(sql_query, (search_input,))
    print("in")
    result = cursor.fetchone()
    if result:
        return Item.id_from_sql(result)
    else:
        return None

def search_db(search_input) -> Result:
    """
    Checks database for matching items
    """ 
    with ssql as (conn, curs):
        curs.execute(
            "SELECT SN FROM PRODUCT WHERE SN=%s;", (search_input,)
        )
        result = curs.fetchone()
        if result == search_input:
            return Ok
        else:
            return Error("No such item was found.")
