"""
Initiate the SSql class and set up the config
"""

from ssql import SSql
from configparser import ConfigParser

ssql_secrets = ConfigParser()
ssql_secrets.read("../secrets/ssql.cfg")
config = {
    "ssh": {
        "host": "130.240.200.96",
        "port": 22,
        "user": "amuobi-4",
        "pass": "vBoMgtRDJQpkWeHN",
    },
    "mysql": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "Master",
        "pass": "!123456789PASSWORD987654321password%",
        "database": "first_test"
    }
}

ssql = SSql(config["ssh"], config["mysql"])
"""
our ssql connection, this should not be in global scope since python has no mutex 
locking, but it's fine for now
"""
