import json

from decimal import InvalidOperation
from http.server import BaseHTTPRequestHandler, HTTPServer
from app.views.transaction_view import TransactionView


class RequestHandler(BaseHTTPRequestHandler):
    router = None

    def _send_json(self, status, data, headers=None):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header("Content-Length", str(len(response)))

        for name, value in (headers or {}).items():
            self.send_header(name, value)

        self.end_headers()
        self.wfile.write(response)

    def _resolve_handler(self, method):
        result = self.router.resolve(method, self.path)

        if result is not None:
            handler, params = result

            return handler, params

        allowed_methods = self.router.allowed_methods(self.path)

        if allowed_methods:
            self._send_json(
                405,
                {"error": "method not allowed"},
                {"Allow": ", ".join(allowed_methods)},
            )
        else:
            self._send_json(404, {"error": "route not found"})

        return None

    def do_GET(self):
        result = self._resolve_handler("GET")

        if result is None:
            return

        handler, params = result

        try:
            result = handler(**params)

            if params:
              data = TransactionView.serialize_transaction(result)
            else:
              data = TransactionView.serialize_transactions(result)

        except ValueError as error:
            self._send_json(400, {"error": str(error)})
            return

        except LookupError as error:
            self._send_json(404, {"error": str(error)})
            return

        except Exception:
            self._send_json(500, {"error": "internal server error"})
            return

        self._send_json(200, data)

    def do_POST(self):
        result = self._resolve_handler("POST")

        if result is None:
            return

        handler, params = result

        content_type = self.headers.get("Content-Type", "")

        if content_type.split(";", 1)[0].strip() != "application/json":
            self._send_json(
                415,
                {"error": "Content-Type must be application/json"},
            )
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            body = json.loads(body_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self._send_json(400, {"error": "request body must be valid JSON"})
            return

        if not isinstance(body, dict):
            self._send_json(400, {"error": "request body must be a JSON object"})
            return

        try:
            transaction = handler(body)

        except KeyError as error:
            self._send_json(
                400,
                {"error": f"missing field: {error.args[0]}"},
            )
            return

        except (InvalidOperation, TypeError, ValueError) as error:
            self._send_json(422, {"error": str(error)})
            return

        except Exception:
            self._send_json(500, {"error": "internal server error"})
            return

        data = TransactionView.serialize_transaction(transaction)
        self._send_json(201, data)

    def do_PUT(self):
        self._resolve_handler("PUT")

    def do_PATCH(self):
        self._resolve_handler("PATCH")

    def do_DELETE(self):
        self._resolve_handler("DELETE")


def run_server(router):
    RequestHandler.router = router

    server = HTTPServer(
        ("localhost", 8000),
        RequestHandler
    )

    print("Server running at http://localhost:8000")

    server.serve_forever()
