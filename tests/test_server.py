import http.client
import json
import threading
import unittest
from http.server import HTTPServer

from app.controllers.transaction_controller import TransactionController
from app.controllers.category_controller import CategoryController
from app.repositories.category_repository import CategoryRepository
from app.services.category_service import CategoryService
from app.views.category_view import CategoryView
from app.views.transaction_view import TransactionView
from app.repositories.transaction_repository import TransactionRepository
from app.routes.router import Router
from app.server import RequestHandler
from app.services.transaction_service import TransactionService


class QuietRequestHandler(RequestHandler):
    def log_message(self, format, *args):
        pass


class TestTransactionServer(unittest.TestCase):
    def setUp(self):
        repository = TransactionRepository()
        categories = CategoryRepository()
        category_service = CategoryService(categories)
        category_service.create_category("General")
        category_controller = CategoryController(category_service)
        service = TransactionService(repository, categories)
        controller = TransactionController(service)

        router = Router()
        router.add_route("GET", "/transactions", controller.list_all, TransactionView.serialize_transactions)
        router.add_route("POST", "/transactions", controller.create, TransactionView.serialize_transaction)
        router.add_route("GET", "/transactions/{id}", controller.get_by_id, TransactionView.serialize_transaction)
        router.add_route(
            "DELETE",
            "/transactions/{id}",
            controller.delete_by_id,
            TransactionView.serialize_transaction,
        )
        router.add_route("PUT", "/transactions/{id}", controller.update_by_id, TransactionView.serialize_transaction)

        router.add_route("GET", "/categories", category_controller.list_all, CategoryView.serialize_categories)
        router.add_route("POST", "/categories", category_controller.create, CategoryView.serialize_category)
        router.add_route("GET", "/categories/{id}", category_controller.get_by_id, CategoryView.serialize_category)

        QuietRequestHandler.router = router
        self.server = HTTPServer(("127.0.0.1", 0), QuietRequestHandler)
        self.thread = threading.Thread(
            target=self.server.serve_forever,
            daemon=True,
        )
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection(
            "127.0.0.1",
            self.server.server_port,
            timeout=2,
        )
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        response_body = response.read()
        data = json.loads(response_body) if response_body else None
        response_headers = dict(response.getheaders())
        connection.close()

        return response.status, response_headers, data

    def post_json(self, data):
        if isinstance(data, dict):
            data = {"category_id": 1, **data}
        return self.request(
            "POST",
            "/transactions",
            body=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

    def put_json(self, path, data):
        data = {"category_id": 1, **data}
        return self.request(
            "PUT",
            path,
            body=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

    def test_categories_and_transaction_relationship(self):
        status, _, category = self.request(
            "POST", "/categories", body=json.dumps({"name": "Food"}),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(status, 201)
        self.assertEqual(self.request("GET", f"/categories/{category['id']}")[2], category)
        status, _, transaction = self.post_json({
            "transaction_type": "expense", "value": "10.00",
            "description": "Lunch", "category_id": category["id"],
        })
        self.assertEqual(status, 201)
        self.assertEqual(transaction["category_id"], category["id"])
        status, _, updated = self.put_json(f"/transactions/{transaction['id']}", {
            "transaction_type": "expense", "value": "11.00",
            "description": "Lunch", "category_id": 1,
        })
        self.assertEqual(status, 200)
        self.assertEqual(updated["category_id"], 1)

    def test_reject_missing_or_invalid_category(self):
        payload = {"transaction_type": "expense", "value": "10", "description": "Lunch"}
        for category_id in (0, -1, True, 1.5, "1"):
            with self.subTest(category_id=category_id):
                status, _, _ = self.post_json({**payload, "category_id": category_id})
                self.assertEqual(status, 422)
        status, _, data = self.post_json({**payload, "category_id": 999})
        self.assertEqual((status, data), (404, {"error": "category not found"}))
        self.assertEqual(self.request("GET", "/transactions")[2], [])
        self.assertEqual(self.request("GET", "/categories/999")[0], 404)

    def test_list_empty_transactions(self):
        status, headers, data = self.request("GET", "/transactions")

        self.assertEqual(status, 200)
        self.assertEqual(data, [])
        self.assertEqual(
            headers["Content-Type"],
            "application/json; charset=utf-8",
        )

    def test_create_and_list_transaction(self):
        status, _, transaction = self.post_json(
            {
                "transaction_type": "income",
                "value": "1500.00",
                "description": "Salary",
            }
        )

        self.assertEqual(status, 201)
        self.assertEqual(
            transaction,
            {
                "id": 1,
                "category_id": 1,
                "type": "income",
                "value": "1500.00",
                "description": "Salary",
            },
        )

        status, _, transactions = self.request("GET", "/transactions")

        self.assertEqual(status, 200)
        self.assertEqual(transactions, [transaction])

    def test_reject_invalid_json(self):
        status, _, data = self.request(
            "POST",
            "/transactions",
            body="{invalid",
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(status, 400)
        self.assertEqual(data, {"error": "request body must be valid JSON"})

    def test_reject_non_object_json(self):
        status, _, data = self.post_json([])

        self.assertEqual(status, 400)
        self.assertEqual(
            data,
            {"error": "request body must be a JSON object"},
        )

    def test_reject_missing_field(self):
        status, _, data = self.post_json(
            {
                "transaction_type": "income",
                "value": "1500.00",
            }
        )

        self.assertEqual(status, 400)
        self.assertEqual(data, {"error": "missing field: description"})

    def test_reject_unsupported_media_type(self):
        status, _, data = self.request(
            "POST",
            "/transactions",
            body="value=1500.00",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        self.assertEqual(status, 415)
        self.assertEqual(
            data,
            {"error": "Content-Type must be application/json"},
        )

    def test_reject_domain_validation_error(self):
        status, _, data = self.post_json(
            {
                "transaction_type": "transfer",
                "value": "1500.00",
                "description": "Transfer",
            }
        )

        self.assertEqual(status, 422)
        self.assertEqual(
            data,
            {"error": "transaction_type must be 'income' or 'expense'"},
        )

    def test_reject_invalid_decimal_value(self):
        status, _, data = self.post_json(
            {
                "transaction_type": "income",
                "value": "invalid",
                "description": "Salary",
            }
        )

        self.assertEqual(status, 422)
        self.assertEqual(data, {"error": "value must be a valid decimal"})

    def test_return_not_found_for_unknown_path(self):
        status, _, data = self.request("GET", "/unknown")

        self.assertEqual(status, 404)
        self.assertEqual(data, {"error": "route not found"})

    def test_return_method_not_allowed(self):
        status, headers, data = self.request("PUT", "/transactions")

        self.assertEqual(status, 405)
        self.assertEqual(headers["Allow"], "GET, POST")
        self.assertEqual(data, {"error": "method not allowed"})

    def test_delete_transaction(self):
        _, _, transaction = self.post_json(
            {
                "transaction_type": "expense",
                "value": "49.90",
                "description": "Groceries",
            }
        )

        status, _, data = self.request(
            "DELETE",
            f"/transactions/{transaction['id']}",
        )

        self.assertEqual(status, 204)
        self.assertIsNone(data)

        status, _, transactions = self.request("GET", "/transactions")

        self.assertEqual(status, 200)
        self.assertEqual(transactions, [])

    def test_return_not_found_when_deleting_unknown_transaction(self):
        status, _, data = self.request("DELETE", "/transactions/999")

        self.assertEqual(status, 404)
        self.assertEqual(data, {"error": "transaction not found"})

    def test_reject_invalid_transaction_id_on_delete(self):
        status, _, data = self.request("DELETE", "/transactions/invalid")

        self.assertEqual(status, 400)
        self.assertEqual(data, {"error": "id must be a valid integer"})

    def test_list_allowed_methods_for_transaction_resource(self):
        status, headers, data = self.request("PATCH", "/transactions/1")

        self.assertEqual(status, 405)
        self.assertEqual(headers["Allow"], "DELETE, GET, PUT")
        self.assertEqual(data, {"error": "method not allowed"})

    def test_update_transaction_preserves_id(self):
        _, _, created = self.post_json(
            {
                "transaction_type": "income",
                "value": "10.00",
                "description": "Original",
            }
        )
        update = {
            "transaction_type": "expense",
            "value": "120.50",
            "description": "Mercado",
        }

        status, _, updated = self.put_json(f"/transactions/{created['id']}", update)

        self.assertEqual(status, 200)
        self.assertEqual(
            updated,
            {
                "id": created["id"],
                "category_id": 1,
                "type": "expense",
                "value": "120.50",
                "description": "Mercado",
            },
        )
        self.assertEqual(
            self.request("GET", f"/transactions/{created['id']}")[2], updated
        )
        self.assertEqual(self.request("GET", "/transactions")[2], [updated])

    def test_update_transaction_with_query_string(self):
        _, _, created = self.post_json(
            {
                "transaction_type": "income",
                "value": "10.00",
                "description": "Original",
            }
        )

        status, _, updated = self.put_json(
            f"/transactions/{created['id']}?source=app",
            {
                "transaction_type": "expense",
                "value": "120.50",
                "description": "Mercado",
            },
        )

        self.assertEqual(status, 200)
        self.assertEqual(updated["id"], created["id"])

    def test_reject_invalid_transaction_id_on_update(self):
        status, _, data = self.put_json(
            "/transactions/invalid",
            {
                "transaction_type": "expense",
                "value": "120.50",
                "description": "Mercado",
            },
        )

        self.assertEqual(status, 400)
        self.assertEqual(data, {"error": "id must be a valid integer"})

    def test_return_not_found_when_updating_unknown_transaction(self):
        status, _, data = self.put_json(
            "/transactions/999",
            {
                "transaction_type": "expense",
                "value": "120.50",
                "description": "Mercado",
            },
        )

        self.assertEqual(status, 404)
        self.assertEqual(data, {"error": "transaction not found"})

    def test_reject_negative_content_length_on_put(self):
        status, _, data = self.request(
            "PUT",
            "/transactions/1",
            body="{}",
            headers={
                "Content-Type": "application/json",
                "Content-Length": "-1",
            },
        )

        self.assertEqual(status, 400)
        self.assertEqual(
            data, {"error": "Content-Length must be a non-negative integer"}
        )


if __name__ == "__main__":
    unittest.main()
