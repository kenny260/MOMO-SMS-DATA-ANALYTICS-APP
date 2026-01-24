from http.server import BaseHTTPRequestHandler
from api.auth import check_auth

# Fake in-memory database for now
TRANSACTIONS = [
    {"id": 1, "amount": 1000},
    {"id": 2, "amount": 2500},
    {"id": 3, "amount": 500},
]

class RequestHandler(BaseHTTPRequestHandler):

    def do_DELETE(self):
        # 🔐 AUTH CHECK (protect ALL endpoints)
        if not check_auth(self.headers):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Secure API"')
            self.end_headers()
            self.wfile.write(b"401 Unauthorized")
            return

        # Expected path: /transactions/{id}
        parts = self.path.strip("/").split("/")

        if len(parts) != 2 or parts[0] != "transactions":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        try:
            transaction_id = int(parts[1])
        except ValueError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid ID")
            return

        # Search and delete
        global TRANSACTIONS
        for tx in TRANSACTIONS:
            if tx["id"] == transaction_id:
                TRANSACTIONS.remove(tx)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Transaction deleted successfully")
                return

        # If not found
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Transaction not found")
