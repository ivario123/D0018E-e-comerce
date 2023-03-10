from typing import Callable
from functools import wraps
import sys
import os
import re
from sys import platform

CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"


class Cfg:
    cfg = {
        "ssh": {
            "user_name": "<uname>",
            "password": "<password>",
            "host": "<host>",
            "port": "22",
        },
        "mysql": {
            "user_name": "uname",
            "password": "<password>",
            "host": "127.0.0.1",
            "port": "3306",
            "database": "<db>",
        },
    }

    def __init__(self):
        pass

    def render(self) -> str:
        ret = "# Generated with the setup tool!\n\n"
        for key in self.cfg.keys():
            ret += f"[{key}]\n"
            for el in self.cfg[key].keys():
                ret += f"{el} = {self.cfg[key][el]}\n"
            ret += "\n"
        return ret

    def ssh(self):
        return f"""
{var("user_name")}= {val(self.cfg["ssh"]["user_name"])}
{var("password")}= {val(self.cfg["ssh"]["password"])}
{var("host")}= {val(self.cfg["ssh"]["host"])}
{var("port")}= {val(self.cfg["ssh"]["port"])}
        """

    def mysql(self):
        return f"""
{var("user_name")}= {val(self.cfg["mysql"]["user_name"])}
{var("password")}= {val(self.cfg["mysql"]["password"])}
{var("host")}= {val(self.cfg["mysql"]["host"])}
{var("port")}= {val(self.cfg["mysql"]["port"])}
{var("database")}= {val(self.cfg["mysql"]["database"])}
        """


cfg = Cfg()


def color(color_, text):
    """
    Taken from https://stackabuse.com/how-to-print-colored-text-in-python/
    """
    num1 = str(color_)
    return f"\033[38;5;{num1}m{text}\033[0;0m"


def var(v, l=10):
    return f"{color(12,v)}" + " " * (l - len(v))


def val(v):
    return f"{color(3,v)}"


def heading(text, boxing=50):
    print("\n" * 1)
    print("-" * boxing)
    print(
        "|",
        " " * (boxing // 2 - len(text) // 2 - 3),
        color(214, text),
        " " * (boxing // 2 - len(text) // 2 - 3),
        "|",
    )
    print("-" * boxing)
    print("\n" * 2)


def query(text):
    return color(11, text)


def clear():
    # Handle linux and windows differences
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    else:
        os.system("cls")


def remove_last_line():
    print(
        CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE,
    )
    sys.stdout.flush()


def get_in(*set):
    y = input()
    while y not in set:
        remove_last_line()
        y = input()
    return y


def get_file(extension):
    y = input()
    while y and y.split()[-1] != extension:
        print("File needs to be of type : " + extension)
        remove_last_line()
        y = input()
    return y


class SetupStep:
    header = ""

    def __init__(self, header="") -> None:
        self.header = header


def setup_step(step: SetupStep = None, question: str = ""):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            clear()
            if SetupStep:
                heading(step.header)
            if question:
                print(query(question))
            return func(*args, **kwargs)

        return wrapper

    return decorator


SSQL = SetupStep("SETTING UP THE SSQL CONFIG")
SSH = SetupStep("SSH SETUP")
MYSQL = SetupStep("MYSQL SETUP")


@setup_step(SSQL)
def ACCEPT(target_name: str, fmt: str, callback: Callable, args):
    print(
        f"""The current {target_name} config is:
{fmt}

Is this ok? y/n ( choosing no here will restart the setup )
    """
    )
    y = get_in("y", "n")
    if y != "y":
        callback(args)


@setup_step(SSH, "What is your ssh username?")
def SSH_UNAME(cfg):
    uname = input("username = ")
    while not uname:
        remove_last_line()
        uname = input("username = ")
    cfg.cfg["ssh"]["user_name"] = uname


@setup_step(SSH, "What is your ssh password?")
def SSH_PASS(cfg):
    uname = input("password = ")
    while not uname:
        remove_last_line()
        uname = input("password = ")
    cfg.cfg["ssh"]["password"] = uname


@setup_step(SSH, "What is your ssh ip?")
def SSH_IP(cfg):
    print("This needs to be a valid ip address")

    def valid_url(text: str) -> bool:
        m = re.findall(r"\d+\.\d+\.\d+\.\d+", text)
        if m:
            return m[0]
        else:
            return None

    inp = valid_url(input("ip = "))
    while not inp:
        remove_last_line()
        inp = valid_url(input("ip = "))
    cfg.cfg["ssh"]["host"] = inp


@setup_step(SSH, "What is your ssh port?")
def SSH_PORT(cfg):
    print("Press enter to keep port 22")
    inp = input("port = ")

    while not inp or not inp.isalnum():
        if not inp:
            break
        inp = input("port = ")

    cfg.cfg["ssh"]["port"] = inp if inp else "22"


def SET_SSH(*args):
    global cfg
    SSH_UNAME(cfg)
    SSH_PASS(cfg)
    SSH_IP(cfg)
    SSH_PORT(cfg)
    ACCEPT("ssh", cfg.ssh(), SET_SSH, args)


@setup_step(MYSQL, "What is your mysql username?")
def MYSQL_UNAME(cfg):
    uname = input("username = ")
    while not uname:
        remove_last_line()
        uname = input("username = ")
    cfg.cfg["mysql"]["user_name"] = uname


@setup_step(MYSQL, "What is your mysql password?")
def MYSQL_PASS(cfg):
    uname = input("password = ")
    while not uname:
        remove_last_line()
        uname = input("password = ")
    cfg.cfg["mysql"]["password"] = uname


@setup_step(MYSQL, "What is your mysql ip?")
def MYSQL_IP(cfg):
    print("This is relative to the host machine.")
    print("This needs to be a valid ip address.")

    def valid_url(text: str) -> bool:
        m = re.findall(r"\d+\.\d+\.\d+\.\d+", text)
        if m:
            return m[0]
        else:
            return None

    inp = valid_url(input("ip = "))
    while not inp:
        remove_last_line()
        inp = valid_url(input("ip = "))
    cfg.cfg["mysql"]["host"] = inp


@setup_step(MYSQL, "What is your mysql port?")
def MYSQL_PORT(cfg):
    print("Press enter to keep port 3306")
    inp = input("port = ")

    while not inp or not inp.isalnum():
        if not inp:
            break
        inp = input("port = ")

    cfg.cfg["mysql"]["port"] = inp if inp else "3306"


@setup_step(MYSQL, "What database should we connect to?")
def MYSQL_DB(cfg):
    database = input("database = ")
    while not database:
        remove_last_line()
        database = input("database = ")
    cfg.cfg["mysql"]["database"] = database


def SET_MYSQL(*args):
    global cfg
    MYSQL_UNAME(cfg)
    MYSQL_PASS(cfg)
    MYSQL_IP(cfg)
    MYSQL_PORT(cfg)
    MYSQL_DB(cfg)
    ACCEPT("mysql", cfg.mysql(), SET_MYSQL, args)


def WEBSITE_SETUP(*args) -> Callable:
    global cfg
    SET_MYSQL()
    SET_SSH()


if __name__ == "__main__":
    """
    Sets up the config file for the website

    Usage :
    ```bash
    python setup.py
    ```
    """
    WEBSITE_SETUP()
    clear()
    heading("Save file")
    with open("./secrets/ssql.cfg", "w") as f:
        f.writelines(cfg.render())
    clear()
    heading("That's it thank you for using the setup tool")
