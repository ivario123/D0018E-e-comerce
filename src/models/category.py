class Category:
    def __init__(self, id: int, name: str, supercategory: int):
        self.id = id
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
    def __init__(self, id: int, name: str, color: str, categories: list):
        self.id = id
        self.name = name
        self.color = color
        self.categories = categories
        if isinstance(categories, list):
            self.categories = [Category(-1, cat, name) for cat in categories]

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, CategoryGroup):
            return NotImplemented
        return self.name == __o.name

    def __repr__(self) -> str:
        return f"CategoryGroup({self.name}, {self.categories})"
