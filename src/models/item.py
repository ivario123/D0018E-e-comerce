class Item:
    rating = 0

    def __init__(self, name, description, price, stock, image, serial_number):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image = image
        self.serial_number = serial_number
        self.categories = None

    def fields(self):
        return [
            self.name,
            self.description,
            self.price,
            self.stock,
            self.image,
            self.serial_number,
        ]

    def assign_categories(self, categories):
        self.categories = categories

    def __repr__(self):
        return f"Item('{self.name}', '{self.description}', '{self.price}', '{self.stock}', '{self.image}', '{self.serial_number}')"

    def add_rating(self, rating):
        self.rating = rating if rating else 0
