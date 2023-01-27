
class CategoryGroup:
    def __init__(self, name, categories):
        self.name = name
        self.categories = categories
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, CategoryGroup):
            return NotImplemented
        return self.name == __o.name