from passlib.hash import sha256_crypt
from models import User
from result import Result, Error, Ok
from . import ssql
from ssql_builder import SSqlBuilder as ssql_builder


@ssql_builder.base(ssql)
def make_admin(email, connection=None, cursor=None):
    cursor.execute("UPDATE USER SET Role='admin' WHERE Email=%s;", (email,))
    return True


@ssql_builder.select(
    ssql, table_name="USER", select_fields=["Username", "Email", "Name", "Surname"]
)
def get_full_user_by_email(Email, sql_query=None, connection=None, cursor=None):
    cursor.execute(sql_query, (Email,))
    result = cursor.fetchone()
    if result:
        return User(*result)
    else:
        return None


@ssql_builder.base(ssql)
def update_user_by_email(Email: str, UserName: str, Name: str, Surname: str, connection=None, cursor=None) -> bool:
    query = """UPDATE USER SET USER.UserName=%s,USER.Name=%s,USER.Surname=%s WHERE USER.Email=%s;"""
    cursor.execute(query, (UserName, Name, Surname, Email,))
    return cursor.rowcount != 0


@ssql_builder.select(
    ssql, table_name="USER", select_fields=["Email", "Username", "Role"]
)
def get_user_by_email(Email, sql_query=None, connection=None, cursor=None):
    cursor.execute(sql_query, (Email,))
    result = cursor.fetchone()
    if result:
        return User.from_sql(result)
    else:
        return None


def auth_user(email, sugested_pass) -> Result:
    # Not using ssql_builder.select because we do might need a lot of time to hash the password, and retrieve the user
    # from the database.
    with ssql as (conn, curs):
        curs.execute("SELECT Password FROM USER WHERE Email=%s;", (email,))
        result = curs.fetchone()
        if result:
            password = result[0]
        else:
            conn.rollback()
            return Error("No such user")
    if sha256_crypt.verify(sugested_pass, password):
        return Ok(get_user_by_email(email))
    else:
        return Error("Password do not match")


def add_new_user(user: User) -> Result:
    # Not using ssql_builder.select because we do might need a lot of time to execute multiple queries
    with ssql as (conn, curs):
        curs.execute("SELECT * FROM USER WHERE email = %s", (user.email,))
        if curs.fetchone():
            return Error("User already exists")
        curs.execute(
            "INSERT INTO USER (Email, Username, Name, Surname, Password,Role) VALUES (%s, %s, %s, %s, %s, %s);",
            (
                user.email,
                user.username,
                user.name,
                user.surname,
                sha256_crypt.hash(user.password),
                "User",
            ),
        )
        # Check that the user now exists
        curs.execute("SELECT * FROM USER where email = %s;", (user.email,))
        if curs.fetchone():
            return Ok(user)
        else:
            conn.rollback()
            Error("Failed to register user, try again later")
