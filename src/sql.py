"""
This file will need to be updated when the sql schemas are done.
"""


from passlib.hash import sha256_crypt
from ssql import SSql
from configparser import ConfigParser
from models import User
from result import Result, Error, Ok

ssql_secrets = ConfigParser()
ssql_secrets.read("../secrets/ssql.cfg")
config = {
    "ssh": {
        "host": ssql_secrets.get("ssh", "host"),
        "port": int(ssql_secrets.get("ssh", "port")),
        "user": ssql_secrets.get("ssh", "user_name"),
        "pass": ssql_secrets.get("ssh", "password"),
    },
    "mysql": {
        "host": ssql_secrets.get("mysql", "host"),
        "port": int(ssql_secrets.get("mysql", "port")),
        "user": ssql_secrets.get("mysql", "user_name"),
        "pass": ssql_secrets.get("mysql", "password"),
    }
}

ssql = SSql(config["ssh"], config["mysql"])
"""
our ssql connection, this should not be in global scope since python has no mutex 
locking, but it's fine for now
"""


def get_user_by_email(email):
    """
    Get a user by email
    """
    with ssql as (_conn, curs):
        curs.execute(
            "SELECT Email,Username,Role FROM USER WHERE email = %s;", (email,))
        result = curs.fetchone()
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
