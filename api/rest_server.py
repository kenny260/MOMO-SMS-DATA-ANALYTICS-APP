#!/usr/bin/env python3
"""
REST API Server for MoMo SMS Transactions

Handles collection endpoints:
- GET /transactions
- POST /transactions

Integrates with existing ETL pipeline and data storage.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.collection_handlers import TransactionCollectionHandler

# Authentication configuration
VALID_CREDENTIALS = {
    "admin": "secure123"
}


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for Transaction REST API.
    Implements collection endpoints only.
    """

    collection_handler = TransactionCollectionHandler()

    def authenticate(self):
        """Verify Basic Authentication credentials"""
        auth_header = self.headers.get("Authorization")

        if not auth_header:
            return False

        try:
            auth_type, credentials = auth_header.split(" ", 1)
            if auth_type.lower() != "basic":
                return False

            decoded = base64.b64decode(credentials).decode("utf-8")
            username, password = decoded.split(":", 1)

            return VALID_CREDENTIALS.get(username) == password

        except Exception:
            return False

    def send_json_response(self, status_code, data=None, message=None):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        response = {}
        if message:
            response["message"] = message
        if data is not None:
            response["data"] = data

        self.wfile.write(json.dumps(response, indent=2).encode())

    def send_error_response(self, status_code, error_message):
        """Send error response"""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        if status_code == 401:
            self.send_header("WWW-Authenticate", 'Basic realm="Transaction API"')
        self.end_headers()

        self.wfile.write(
            json.dumps({"error": error_message}, indent=2).encode()
        )

    def do_GET(self):
        """Handle GET requests"""
        if not self.authenticate():
            self.send_error_response(401, "Unauthorized")
            return

        if self.path == "/transactions":
            try:
                result = self.collection_handler.get_all_transactions()
                self.send_json_response(200, result)
            except Exception as e:
                self.send_error_response(500, f"Server error: {str(e)}")
        else:
            self.send_error_response(404, "Endpoint not found")

    def do_POST(self):
        """Handle POST requests"""
        if not self.authenticate():
            self.send_error_response(401, "Unauthorized")
            return

        if self.path == "/transactions":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length == 0:
                    self.send_error_response(400, "Empty request body")
                    return

                body = self.rfile.read(content_length).decode("utf-8")

                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    self.send_error_response(400, "Invalid JSON format")
                    return

                result = self.collection_handler.add_transaction(data)

                if "error" in result:
                    self.send_error_response(400, result["error"])
                else:
                    self.send_json_response(
                        201,
                        result["transaction"],
                        result["message"]
                    )

            except Exception as e:
                self.send_error_response(500, f"Server error: {str(e)}")
        else:
            self.send_error_response(404, "Endpoint not found")

    def do_PUT(self):
        self.send_error_response(404, "Endpoint not found")

    def do_DELETE(self):
        self.send_error_response(404, "Endpoint not found")


def run_server(port=8000):
    """Start the REST API server"""
    server_address = ("", port)
    httpd = HTTPServer(server_address, TransactionAPIHandler)

    print("MoMo SMS Transaction REST API Server")
    print("-----------------------------------")
    print(f"Server URL: http://localhost:{port}")
    print("Authentication: Basic Auth (admin / secure123)")
    print()
    print("Available Endpoints:")
    print("  GET  /transactions")
    print("  POST /transactions")
    print()
    print("Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == "__main__":
    run_server()

