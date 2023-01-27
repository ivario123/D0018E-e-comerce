"""
This file will need to be updated when the sql schemas are done.
"""


from passlib.hash import sha256_crypt
from models import User
from result import Result, Error, Ok
from . import ssql
from ssql_builder import SSqlBuilder as ssql_builder


@ssql_builder.select(ssql, table_name="USER", select_fields=["Email", "Username", "Role"])
def get_user_by_email(Email, sql_query=None, connection=None, cursor=None):
    """
    Get a user by email
    """
    cursor.execute(
        sql_query, (Email,))
    result = cursor.fetchone()
    if result:
        return User.from_sql(result)
    else:
        return None


def auth_user(email, sugested_pass) -> Result:
    """
    Authenticates a user
    ---

    If the password matches the stored pass then 
    it returns the user wrapped in Ok.

    otherwise it returns an error.
    """
    with ssql as (conn, curs):
        curs.execute(
            "SELECT Password FROM USER WHERE Email=%s;", (email,)
        )
        result = curs.fetchone()
        if result:
            password = result[0]
        else:
            return Error("No such user")
    if sha256_crypt.verify(
        sugested_pass,
        password
    ):
        return Ok(get_user_by_email(email))
    else:
        return Error("Password do not match")


def add_new_user(user: User) -> Result:
    """
    Adds a new user to the sql database
    """
    with ssql as (conn, curs):
        curs.execute(
            "SELECT * FROM USER WHERE email = %s", (user.email,)
        )
        if curs.fetchone():
            return Error("User already exists")
        curs.execute(
            "INSERT INTO USER (Email, Username, Name, Surname, Password,Role) VALUES (%s, %s, %s, %s, %s, %s);",
            (user.email, user.username, user.name,
             user.surname, sha256_crypt.hash(user.password), "Admin")
        )
        # Check that the user now exists
        curs.execute(
            "SELECT * FROM USER where email = %s;", (user.email,)
        )
        if curs.fetchone():
            return Ok(user)
        else:
            Error("Failed to register user, try again later")
