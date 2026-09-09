import unittest

from app.routes.router import Router


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = Router()
        self.handler = lambda: None

    def test_add_and_resolve_route(self):
        self.router.add_route("GET", "/transactions", self.handler)

        resolved_handler, params = self.router.resolve("GET", "/transactions")

        self.assertIs(resolved_handler, self.handler)
        self.assertEqual(params, {})

    def test_normalize_method_to_uppercase(self):
        self.router.add_route("get", "/transactions", self.handler)

        resolved_handler, params = self.router.resolve("get", "/transactions")

        self.assertIs(resolved_handler, self.handler)
        self.assertEqual(params, {})

    def test_return_none_for_unknown_route(self):
        self.assertIsNone(self.router.resolve("GET", "/unknown"))

    def test_list_allowed_methods_for_path(self):
        self.router.add_route("POST", "/transactions", self.handler)
        self.router.add_route("GET", "/transactions", self.handler)

        methods = self.router.allowed_methods("/transactions")

        self.assertEqual(methods, ["GET", "POST"])

    def test_resolve_dynamic_route_with_path_parameter(self):
        self.router.add_route("DELETE", "/transactions/{id}", self.handler)

        resolved_handler, params = self.router.resolve(
            "DELETE",
            "/transactions/42",
        )

        self.assertIs(resolved_handler, self.handler)
        self.assertEqual(params, {"id": "42"})

    def test_list_allowed_methods_for_dynamic_path(self):
        self.router.add_route("GET", "/transactions/{id}", self.handler)
        self.router.add_route("DELETE", "/transactions/{id}", self.handler)

        methods = self.router.allowed_methods("/transactions/42")

        self.assertEqual(methods, ["DELETE", "GET"])


if __name__ == "__main__":
    unittest.main()
