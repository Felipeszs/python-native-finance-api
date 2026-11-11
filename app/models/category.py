class Category:
  def __init__(self, name: str):
    if not isinstance(name, str):
      raise TypeError('name must be a string')

    if not name.strip():
      raise ValueError('name cannot be empty')

    self.id = None
    self.name = name.strip()

