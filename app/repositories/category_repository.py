class CategoryRepository:
  def __init__(self):
    self.categories = []
    self.next_id = 1

  def save(self, category):
    category.id = self.next_id
    self.next_id += 1

    self.categories.append(category)

    return category

  def find_all(self):
    return self.categories

  def find_by_id(self, category_id):
    for category in self.categories:
      if category_id == category.id:
        return category
    return None
