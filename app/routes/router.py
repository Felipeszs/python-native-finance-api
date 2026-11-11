class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler, serializer):
        self.routes[(method.upper(), path)] = (
            handler,
            serializer
        )

    def resolve(self, method, path):
        route = self.routes.get((method.upper(), path))

        if route is not None:
            handler, serializer = route

            return handler, {}, serializer

        for (route_method, route_path), route in self.routes.items():
            if route_method != method.upper():
                continue

            params = self._match_path(route_path, path)

            if params is None:
                continue

            handler, serializer = route

            return handler, params, serializer

        return None

    def allowed_methods(self, path):
        return sorted(
            {
                method
                for method, route_path in self.routes
                if self._match_path(route_path, path) is not None
            }
        )

    def _match_path(self, route_path, request_path):
        params = {}

        route_parts = route_path.strip("/").split("/")
        request_parts = request_path.strip("/").split("/")

        if len(route_parts) != len(request_parts):
            return None

        for route_part, request_part in zip(
            route_parts,
            request_parts,
            strict=True
        ):
            if route_part.startswith("{") and route_part.endswith("}"):
                parameter_name = route_part[1:-1]
                params[parameter_name] = request_part

            elif route_part != request_part:
                return None

        return params
