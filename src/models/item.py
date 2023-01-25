
class Item:
    """
    A item has :
    - name
    - description
    - price
    - stock
    - image
    - serial number ( primary key )
    """

    def __init__(self, name, description, price, stock, image, serial_number):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image = image
        self.serial_number = serial_number

    def fields(self):
        return [self.name, self.description, self.price, self.stock, self.image, self.serial_number]

    def __repr__(self):
        return f"Item('{self.name}', '{self.description}', '{self.price}', '{self.stock}', '{self.image}', '{self.serial_number}')"
