class Category:
    def __init__(self, name, supercategory):
        self.name = name
        self.supercategory = supercategory
        self.selected = False

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Category):
            return NotImplemented
        return self.name == __o.name

    def __repr__(self) -> str:
        return f"Category({self.name}, {self.supercategory})"


class CategoryGroup:
    def __init__(self, name, color, categories):
        self.name = name
        self.color = color
        self.categories = categories
        if isinstance(categories, list):
            self.categories = [Category(cat, name) for cat in categories]

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, CategoryGroup):
            return NotImplemented
        return self.name == __o.name

    def __repr__(self) -> str:
        return f"CategoryGroup({self.name}, {self.categories})"
