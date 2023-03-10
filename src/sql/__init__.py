"""
Initiate the SSql class and set up the config
"""

from ssql import SSql
from configparser import ConfigParser

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
        "database": "V0.5",
    },
}

ssql = SSql(config["ssh"], config["mysql"])
"""
Our sql connection, this is fine to have in the global scope since the `SSql` abstraction introduces a mutex
on the sql connection.
"""
