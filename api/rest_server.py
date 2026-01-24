#!/usr/bin/env python3
"""
REST API Server for MoMo SMS Transactions
Implements collection endpoints: GET /transactions, POST /transactions
Uses Python http.server module with Basic Authentication
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.collection_handlers import TransactionCollectionHandler

VALID_CREDENTIALS = {
    "admin": "secure123"
}


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Transaction REST API"""
    
    collection_handler = TransactionCollectionHandler()
    
    def authenticate(self):
        """Verify Basic Authentication credentials"""
        auth_header = self.headers.get('Authorization')
        
        if not auth_header:
            return False
        
        try:
            auth_type, credentials = auth_header.split(' ', 1)
            
            if auth_type.lower() != 'basic':
                return False
            
            decoded = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            return VALID_CREDENTIALS.get(username) == password
            
        except Exception:
            return False
    
    def send_json_response(self, status_code, data):
        """Send JSON response with proper headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_error_response(self, status_code, error_message):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        if status_code == 401:
            self.send_header('WWW-Authenticate', 'Basic realm="Transaction API"')
        self.end_headers()
        
        error = {"error": error_message}
        self.wfile.write(json.dumps(error, indent=2).encode())
    
    def do_GET(self):
        """Handle GET requests"""
        if not self.authenticate():
            self.send_error_response(401, "Unauthorized")
            return
        
        if self.path == '/transactions':
            try:
                result = self.collection_handler.get_all_transactions()
                self.send_json_response(200, result)
            except Exception as e:
                self.send_error_response(500, f"Internal server error: {str(e)}")
        else:
            self.send_error_response(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        if not self.authenticate():
            self.send_error_response(401, "Unauthorized")
            return
        
        if self.path == '/transactions':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                
                if content_length == 0:
                    self.send_error_response(400, "Empty request body")
                    return
                
                body = self.rfile.read(content_length).decode('utf-8')
                
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    self.send_error_response(400, "Invalid JSON format")
                    return
                
                result = self.collection_handler.add_transaction(data)
                
                if "error" in result:
                    self.send_error_response(400, result["error"])
                else:
                    self.send_json_response(201, result)
                    
            except Exception as e:
                self.send_error_response(500, f"Internal server error: {str(e)}")
        else:
            self.send_error_response(404, "Endpoint not found")


def run_server(port=8000):
    """Start the REST API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TransactionAPIHandler)
    
    print("="*70)
    print("MoMo SMS Transaction REST API Server")
    print("="*70)
    print(f"Server: http://localhost:{port}")
    print(f"Credentials: admin / secure123")
    print()
    print("Endpoints:")
    print("  GET  /transactions  - Retrieve all transactions")
    print("  POST /transactions  - Create new transaction")
    print()
    print("Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped")


if __name__ == '__main__':
    run_server()
