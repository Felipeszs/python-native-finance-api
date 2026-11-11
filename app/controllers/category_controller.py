class CategoryController:
    def __init__(self, service):
        self.service = service

    def create(self, body):
        name = body["name"]
        return self.service.create_category(name)

    def list_all(self):
        return self.service.list_categories()

    def get_by_id(self, id):
        try:
            category_id = int(id)

        except (ValueError, TypeError):
            raise ValueError("id must be a valid integer") from None

        return self.service.find_by_id(category_id)
