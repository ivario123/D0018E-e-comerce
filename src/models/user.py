from flask_login import UserMixin


class User(UserMixin):
    """
    User abstraction class
    """

    def __init__(self, username, email, name=None, surname=None, password=None):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.password = password
        self.role = "User"

    def fields(self):
        return [self.email, self.username, self.name, self.surname, self.password]

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def from_sql(sql):
        # sql is a tuple of (id, username, email)
        user = User(sql[1], sql[0])
        user.role = sql[2]
        return user

    def get_id(self):
        return self.email
