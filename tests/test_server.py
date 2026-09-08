import http.client
import json
import threading
import unittest

from http.server import HTTPServer

from app.controllers.transaction_controller import TransactionController
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
        service = TransactionService(repository)
        controller = TransactionController(service)

        router = Router()
        router.add_route("GET", "/transactions", controller.list_all)
        router.add_route("POST", "/transactions", controller.create)

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
        )
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        data = json.loads(response.read())
        response_headers = dict(response.getheaders())
        connection.close()

        return response.status, response_headers, data

    def post_json(self, data):
        return self.request(
            "POST",
            "/transactions",
            body=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

    def test_list_empty_transactions(self):
        status, headers, data = self.request("GET", "/transactions")

        self.assertEqual(status, 200)
        self.assertEqual(data, [])
        self.assertEqual(
            headers["Content-Type"],
            "application/json; charset=utf-8",
        )

    def test_create_and_list_transaction(self):
        status, _, transaction = self.post_json({
            "transaction_type": "income",
            "value": "1500.00",
            "description": "Salary",
        })

        self.assertEqual(status, 201)
        self.assertEqual(transaction, {
            "id": 1,
            "type": "income",
            "value": "1500.00",
            "description": "Salary",
        })

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
        status, _, data = self.post_json({
            "transaction_type": "income",
            "value": "1500.00",
        })

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
        status, _, data = self.post_json({
            "transaction_type": "transfer",
            "value": "1500.00",
            "description": "Transfer",
        })

        self.assertEqual(status, 422)
        self.assertEqual(
            data,
            {"error": "transaction_type must be 'income' or 'expense'"},
        )

    def test_reject_invalid_decimal_value(self):
        status, _, data = self.post_json({
            "transaction_type": "income",
            "value": "invalid",
            "description": "Salary",
        })

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


if __name__ == "__main__":
    unittest.main()
