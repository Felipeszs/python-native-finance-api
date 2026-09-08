class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler):
        self.routes[(method, path)] = handler

    def resolve(self, method, path):
        return self.routes.get((method, path))
