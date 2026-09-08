class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler):
        self.routes[(method.upper(), path)] = handler

    def resolve(self, method, path):
        return self.routes.get((method.upper(), path))

    def allowed_methods(self, path):
        return sorted(
            method
            for method, route_path in self.routes
            if route_path == path
        )
