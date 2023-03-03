class Review:
    def __init__(self, username, rating, text, email=""):
        self.username = username
        self.rating = rating
        self.text = text
        self.email = email

    def from_sql(sql, username,email):
        """
        Creates a new review from the return of a sql request
        """
        return Review(rating=sql[0], text=sql[1], email=email,username=username)
