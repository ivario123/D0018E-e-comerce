
class Review:
    def __init__(self, username, rating, text):
        self.username = username
        self.rating = rating
        self.text = text

    def from_sql(sql, username):
        """
        Creates a new review from the return of a sql request
        """
        return Review(username=username, rating=sql[0], text=sql[1])
