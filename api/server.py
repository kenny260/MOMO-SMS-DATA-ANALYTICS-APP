#!/usr/bin/env python3
"""
MoMo SMS Transaction REST API Server
CRUD endpoints with Basic Authentication
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
import os
import re
from datetime import datetime

CREDENTIALS = {"admin": "secure123"}


class TransactionAPI(BaseHTTPRequestHandler):
    """REST API handler with in-memory storage"""
    
    transactions = []
    next_id = 1
    
    @classmethod
    def load_data(cls):
        """Load transactions from JSON file"""
        try:
            with open('data/transactions.json', 'r') as f:
                cls.transactions = json.load(f)
                if cls.transactions:
                    cls.next_id = max(int(t['id']) for t in cls.transactions) + 1
        except:
            cls.transactions = []
    
    @classmethod
    def save_data(cls):
        """Save transactions to JSON file"""
        os.makedirs('data', exist_ok=True)
        with open('data/transactions.json', 'w') as f:
            json.dump(cls.transactions, f, indent=2)
    
    def authenticate(self):
        """Basic Authentication"""
        auth = self.headers.get('Authorization')
        if not auth:
            return False
        
        try:
            auth_type, credentials = auth.split(' ', 1)
            if auth_type.lower() != 'basic':
                return False
            
            decoded = base64.b64decode(credentials).decode()
            username, password = decoded.split(':', 1)
            return CREDENTIALS.get(username) == password
        except:
            return False
    
    def send_json(self, status, data):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_error(self, status, message):
        """Send error response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        if status == 401:
            self.send_header('WWW-Authenticate', 'Basic realm="API"')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}, indent=2).encode())
    
    def parse_body(self):
        """Parse JSON request body"""
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            return json.loads(body) if body else {}
        except:
            return None
    
    def do_GET(self):
        """Handle GET requests"""
        if not self.authenticate():
            self.send_error(401, "Unauthorized")
            return
        
        # GET /transactions
        if self.path == '/transactions':
            self.send_json(200, {
                "count": len(self.transactions),
                "transactions": self.transactions
            })
        
        # GET /transactions/{id}
        elif match := re.match(r'/transactions/(\d+)', self.path):
            tid = match.group(1)
            transaction = next((t for t in self.transactions if t['id'] == tid), None)
            
            if transaction:
                self.send_json(200, {"transaction": transaction})
            else:
                self.send_error(404, f"Transaction {tid} not found")
        
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        if not self.authenticate():
            self.send_error(401, "Unauthorized")
            return
        
        if self.path != '/transactions':
            self.send_error(404, "Endpoint not found")
            return
        
        data = self.parse_body()
        if data is None:
            self.send_error(400, "Invalid JSON")
            return
        
        # Validate required fields
        required = ['type', 'amount', 'sender', 'receiver']
        if missing := [f for f in required if f not in data]:
            self.send_error(400, f"Missing fields: {', '.join(missing)}")
            return
        
        # Validate type
        if data['type'].upper() not in ['SEND', 'RECEIVE', 'DEPOSIT', 'WITHDRAW', 'PAYMENT']:
            self.send_error(400, "Invalid transaction type")
            return
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                self.send_error(400, "Amount must be > 0")
                return
        except:
            self.send_error(400, "Invalid amount")
            return
        
        # Create transaction
        transaction = {
            "id": str(self.next_id),
            "type": data['type'].upper(),
            "amount": amount,
            "sender": data['sender'],
            "receiver": data['receiver'],
            "timestamp": data.get('timestamp', datetime.now().isoformat()),
            "status": data.get('status', 'completed'),
            "reference": data.get('reference', f"TXN{self.next_id:06d}")
        }
        
        self.transactions.append(transaction)
        self.next_id += 1
        self.save_data()
        
        self.send_json(201, {
            "message": "Transaction created",
            "transaction": transaction
        })
    
    def do_PUT(self):
        """Handle PUT requests"""
        if not self.authenticate():
            self.send_error(401, "Unauthorized")
            return
        
        match = re.match(r'/transactions/(\d+)', self.path)
        if not match:
            self.send_error(404, "Endpoint not found")
            return
        
        tid = match.group(1)
        transaction = next((t for t in self.transactions if t['id'] == tid), None)
        
        if not transaction:
            self.send_error(404, f"Transaction {tid} not found")
            return
        
        data = self.parse_body()
        if data is None:
            self.send_error(400, "Invalid JSON")
            return
        
        # Update fields
        if 'type' in data:
            if data['type'].upper() not in ['SEND', 'RECEIVE', 'DEPOSIT', 'WITHDRAW', 'PAYMENT']:
                self.send_error(400, "Invalid transaction type")
                return
            transaction['type'] = data['type'].upper()
        
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    self.send_error(400, "Amount must be > 0")
                    return
                transaction['amount'] = amount
            except:
                self.send_error(400, "Invalid amount")
                return
        
        if 'sender' in data:
            transaction['sender'] = data['sender']
        if 'receiver' in data:
            transaction['receiver'] = data['receiver']
        if 'status' in data:
            transaction['status'] = data['status']
        
        self.save_data()
        
        self.send_json(200, {
            "message": "Transaction updated",
            "transaction": transaction
        })
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if not self.authenticate():
            self.send_error(401, "Unauthorized")
            return
        
        match = re.match(r'/transactions/(\d+)', self.path)
        if not match:
            self.send_error(404, "Endpoint not found")
            return
        
        tid = match.group(1)
        transaction = next((t for t in self.transactions if t['id'] == tid), None)
        
        if not transaction:
            self.send_error(404, f"Transaction {tid} not found")
            return
        
        self.transactions = [t for t in self.transactions if t['id'] != tid]
        self.save_data()
        
        self.send_json(200, {
            "message": "Transaction deleted",
            "transaction": transaction
        })


def run_server(port=8000):
    """Start REST API server"""
    TransactionAPI.load_data()
    
    server = HTTPServer(('', port), TransactionAPI)
    print(f"Server running on http://localhost:{port}")
    print(f"Credentials: admin / secure123")
    print(f"Loaded {len(TransactionAPI.transactions)} transactions\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == '__main__':
    run_server()
