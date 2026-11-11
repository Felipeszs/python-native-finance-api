import json

from decimal import InvalidOperation
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from app.controllers.transaction_controller import InvalidTransactionId


class RequestHandler(BaseHTTPRequestHandler):
    router = None

    frontend_directory = (
        Path(__file__).resolve().parent.parent / "frontend"
    )

    def _serve_frontend(self):
        path = urlsplit(self.path).path

        assets = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/styles.css": ("styles.css", "text/css; charset=utf-8"),
            "/app.js": ("app.js", "text/javascript; charset=utf-8"),
        }

        asset = assets.get(path)

        if asset is None:
            return False

        filename, content_type = asset

        try:
            content = (
                self.frontend_directory / filename
            ).read_bytes()

        except OSError:
            self._send_json(
                500,
                {"error": "internal server error"}
            )
            return True

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()

        self.wfile.write(content)

        return True

    def _send_json(self, status, data, headers=None):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        for name, value in (headers or {}).items():
            self.send_header(name, value)

        self.end_headers()
        self.wfile.write(response)

    def _resolve_handler(self, method):
        path = urlsplit(self.path).path

        result = self.router.resolve(method, path)

        if result is not None:
            return result

        allowed_methods = self.router.allowed_methods(path)

        if allowed_methods:
            self._send_json(
                405,
                {"error": "method not allowed"},
                {"Allow": ", ".join(allowed_methods)}
            )
        else:
            self._send_json(
                404,
                {"error": "route not found"}
            )

        return None

    def do_GET(self):
        if self._serve_frontend():
            return

        route = self._resolve_handler("GET")

        if route is None:
            return

        handler, params, serializer = route

        try:
            result = handler(**params)

            data = serializer(result)

        except InvalidTransactionId as error:
            self._send_json(400, {"error": str(error)})
            return

        except ValueError as error:
            self._send_json(400, {"error": str(error)})
            return

        except LookupError as error:
            self._send_json(404, {"error": str(error)})
            return

        except Exception:
            self._send_json(
                500,
                {"error": "internal server error"}
            )
            return

        self._send_json(200, data)

    def do_POST(self):
        route = self._resolve_handler("POST")

        if route is None:
            return

        handler, params, serializer = route

        content_type = self.headers.get("Content-Type", "")

        if content_type.split(";", 1)[0].strip().lower() != "application/json":
            self._send_json(
                415,
                {"error": "Content-Type must be application/json"}
            )
            return

        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            if content_length < 0:
                raise ValueError

        except ValueError:
            self._send_json(
                400,
                {
                    "error": "Content-Length must be a non-negative integer"
                }
            )
            return

        try:
            body_bytes = self.rfile.read(content_length)
            body = json.loads(body_bytes)

        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self._send_json(
                400,
                {"error": "request body must be valid JSON"}
            )
            return

        if not isinstance(body, dict):
            self._send_json(
                400,
                {"error": "request body must be a JSON object"}
            )
            return

        try:
            result = handler(body, **params)

            data = serializer(result)

        except KeyError as error:
            self._send_json(
                400,
                {"error": f"missing field: {error.args[0]}"}
            )
            return

        except (InvalidOperation, TypeError, ValueError) as error:
            self._send_json(
                422,
                {"error": str(error)}
            )
            return

        except LookupError as error:
            self._send_json(
                404,
                {"error": str(error)}
            )
            return

        except Exception:
            self._send_json(
                500,
                {"error": "internal server error"}
            )
            return

        self._send_json(201, data)

    def do_PUT(self):
        route = self._resolve_handler("PUT")

        if route is None:
            return

        handler, params, serializer = route

        content_type = self.headers.get("Content-Type", "")

        if content_type.split(";", 1)[0].strip().lower() != "application/json":
            self._send_json(
                415,
                {"error": "Content-Type must be application/json"}
            )
            return

        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            if content_length < 0:
                raise ValueError

        except ValueError:
            self._send_json(
                400,
                {
                    "error": "Content-Length must be a non-negative integer"
                }
            )
            return

        try:
            body_bytes = self.rfile.read(content_length)
            body = json.loads(body_bytes)

        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self._send_json(
                400,
                {"error": "request body must be valid JSON"}
            )
            return

        if not isinstance(body, dict):
            self._send_json(
                400,
                {"error": "request body must be a JSON object"}
            )
            return

        try:
            result = handler(body=body, **params)

            data = serializer(result)

        except KeyError as error:
            self._send_json(
                400,
                {"error": f"missing field: {error.args[0]}"}
            )
            return

        except InvalidTransactionId as error:
            self._send_json(400, {"error": str(error)})
            return

        except (InvalidOperation, TypeError, ValueError) as error:
            self._send_json(
                422,
                {"error": str(error)}
            )
            return

        except LookupError as error:
            self._send_json(
                404,
                {"error": str(error)}
            )
            return

        except Exception:
            self._send_json(
                500,
                {"error": "internal server error"}
            )
            return

        self._send_json(200, data)

    def do_PATCH(self):
        self._resolve_handler("PATCH")

    def do_DELETE(self):
        route = self._resolve_handler("DELETE")

        if route is None:
            return

        handler, params, serializer = route

        try:
            handler(**params)

        except InvalidTransactionId as error:
            self._send_json(400, {"error": str(error)})
            return

        except ValueError as error:
            self._send_json(400, {"error": str(error)})
            return

        except LookupError as error:
            self._send_json(404, {"error": str(error)})
            return

        except Exception:
            self._send_json(
                500,
                {"error": "internal server error"}
            )
            return

        self.send_response(204)
        self.end_headers()


def run_server(router):
    RequestHandler.router = router

    server = HTTPServer(
        ("localhost", 8000),
        RequestHandler
    )

    print("Server running at http://localhost:8000")

    server.serve_forever()
