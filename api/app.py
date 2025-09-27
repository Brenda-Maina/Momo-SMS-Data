import sys
import os
# Add the project root to Python path so we can import etl module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse as urlparse
from etl.parse_xml import parse_sms_xml

# Load the parsed data
TRANSACTIONS = parse_sms_xml('data/raw/momo.xml')

class MomoAPIHandler(BaseHTTPRequestHandler):
    
    def _send_response(self, status, data=None):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if data:
            self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse.urlparse(self.path)
        
        # GET /transactions - List all transactions
        if parsed_path.path == '/transactions' or parsed_path.path == '/transactions/':
            self._send_response(200, {
                "count": len(TRANSACTIONS),
                "transactions": TRANSACTIONS
            })
        
        # GET /transactions/{id} - Get specific transaction
        elif parsed_path.path.startswith('/transactions/'):
            parts = parsed_path.path.split('/')
            if len(parts) == 3 and parts[2].isdigit():
                transaction_id = int(parts[2])
                transaction = next((t for t in TRANSACTIONS if t['id'] == transaction_id), None)
                
                if transaction:
                    self._send_response(200, transaction)
                else:
                    self._send_response(404, {"error": "Transaction not found"})
            else:
                self._send_response(400, {"error": "Invalid transaction ID"})
        
        else:
            self._send_response(404, {"error": "Endpoint not found"})
    
    def do_POST(self):
        """Handle POST requests to create new transaction"""
        if self.path == '/transactions' or self.path == '/transactions/':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                try:
                    post_data = self.rfile.read(content_length)
                    new_transaction = json.loads(post_data)
                    
                    # Generate new ID
                    new_id = max([t['id'] for t in TRANSACTIONS]) + 1 if TRANSACTIONS else 1
                    new_transaction['id'] = new_id
                    TRANSACTIONS.append(new_transaction)
                    
                    self._send_response(201, {
                        "message": "Transaction created successfully",
                        "id": new_id,
                        "transaction": new_transaction
                    })
                    
                except json.JSONDecodeError:
                    self._send_response(400, {"error": "Invalid JSON"})
            else:
                self._send_response(400, {"error": "No data provided"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})
    
    def do_PUT(self):
        """Handle PUT requests to update existing transaction"""
        if self.path.startswith('/transactions/'):
            parts = self.path.split('/')
            if len(parts) == 3 and parts[2].isdigit():
                transaction_id = int(parts[2])
                
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    try:
                        put_data = self.rfile.read(content_length)
                        updated_data = json.loads(put_data)
                        
                        # Find and update the transaction
                        for i, transaction in enumerate(TRANSACTIONS):
                            if transaction['id'] == transaction_id:
                                # Update the transaction but keep the original ID
                                updated_data['id'] = transaction_id
                                TRANSACTIONS[i] = {**transaction, **updated_data}
                                
                                self._send_response(200, {
                                    "message": "Transaction updated successfully",
                                    "transaction": TRANSACTIONS[i]
                                })
                                return
                        
                        self._send_response(404, {"error": "Transaction not found"})
                        
                    except json.JSONDecodeError:
                        self._send_response(400, {"error": "Invalid JSON"})
                else:
                    self._send_response(400, {"error": "No data provided"})
            else:
                self._send_response(400, {"error": "Invalid transaction ID"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if self.path.startswith('/transactions/'):
            parts = self.path.split('/')
            if len(parts) == 3 and parts[2].isdigit():
                transaction_id = int(parts[2])
                
                # Find and remove the transaction
                for i, transaction in enumerate(TRANSACTIONS):
                    if transaction['id'] == transaction_id:
                        deleted_transaction = TRANSACTIONS.pop(i)
                        self._send_response(200, {
                            "message": "Transaction deleted successfully",
                            "deleted_transaction": deleted_transaction
                        })
                        return
                
                self._send_response(404, {"error": "Transaction not found"})
            else:
                self._send_response(400, {"error": "Invalid transaction ID"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})
    
    def log_message(self, format, *args):
        """Reduce log noise"""
        pass

def run_server(port=8000):
    """Start the API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MomoAPIHandler)
    
    print(f" MoMo API Server running on http://localhost:{port}")
    print("Available endpoints:")
    print("   GET    /transactions        - List all transactions")
    print("   GET    /transactions/:id    - Get specific transaction")
    print("   POST   /transactions        - Create new transaction") 
    print("   PUT    /transactions/:id    - Update transaction")
    print("   DELETE /transactions/:id    - Delete transaction")
    print("\n Test with: curl http://localhost:8000/transactions")
    
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()