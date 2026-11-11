from app.models.category import Category


class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def create_category(self, name):
        category = Category(name=name)

        return self.repository.save(category)

    def list_categories(self):
        return self.repository.find_all()

    def find_by_id(self, category_id):

        category = self.repository.find_by_id(category_id)

        if category is None:
            raise LookupError("Category not found")

        return category
