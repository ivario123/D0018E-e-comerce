from result import Result, Error, Ok
from . import ssql
from ssql_builder import SSqlBuilder as ssql_builder

def search_db(search_input) -> Result:
    with ssql as (conn, curs):
        curs.execute(
            "SELECT * FROM PRODUCT WHERE SN=%s;", (search_input,)
        )
        if curs.fetchone():
            return Ok(search_input)
        else:
            Error("Failed to search, try again later")

