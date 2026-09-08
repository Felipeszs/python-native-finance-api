import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from app.views.transaction_view import TransactionView


class RequestHandler(BaseHTTPRequestHandler):
    router = None

    def do_GET(self):
        handler = self.router.resolve("GET", self.path)

        if handler is None:
            self.send_response(404)
            self.end_headers()
            return

        transactions = handler()

        data = TransactionView.serialize_transactions(transactions)
        response = json.dumps(data).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(response)

    def do_POST(self):
        handler = self.router.resolve("POST", self.path)

        if handler is None:
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(
            self.headers.get("Content-Length", 0)
        )

        body_bytes = self.rfile.read(content_length)

        body_string = body_bytes.decode("utf-8")

        body = json.loads(body_string)

        transaction = handler(body)

        data = TransactionView.serialize_transaction(
            transaction
        )

        response = json.dumps(data).encode()

        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(response)


def run_server(router):
    RequestHandler.router = router

    server = HTTPServer(
        ("localhost", 8000),
        RequestHandler
    )

    print("Server running at http://localhost:8000")

    server.serve_forever()
