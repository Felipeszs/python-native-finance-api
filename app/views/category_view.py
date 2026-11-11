class CategoryView:

  @staticmethod
  def serialize_category(category):
    return {
      "id": category.id,
      "name": category.name
    }

  @staticmethod
  def serialize_categories(categories):
    return [
      CategoryView.serialize_category(category)
      for category in categories
    ]
