import http.server
import socketserver
import os
import json
import urllib.request
import urllib.error
import hmac
import hashlib
import time
import base64

PORT = 3000

# Load .env
env_vars = {}
if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env_vars[k.strip()] = v.strip().strip("'").strip('"')

class DevServerHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Prevent caching for local dev testing
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_POST(self):
        if self.path == '/api/create-order':
            self.handle_create_order()
        elif self.path == '/api/verify-payment':
            self.handle_verify_payment()
        else:
            self.send_error(404, "Not Found")

    def handle_create_order(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            amount = req_data.get('amount')
            currency = req_data.get('currency', 'INR')
            if not amount:
                self.send_json_error(400, "Valid amount is required")
                return
                
            amount_val = float(amount)
            if amount_val < 1 or amount_val > 100000:
                self.send_json_error(400, "Amount must be between 1 and 100,000")
                return
                
            amount_in_paise = int(round(amount_val * 100))
            
            key_id = env_vars.get('RAZORPAY_KEY_ID')
            key_secret = env_vars.get('RAZORPAY_KEY_SECRET')
            
            if not key_id or not key_secret:
                self.send_json_error(500, "Razorpay credentials are not fully configured in local .env")
                return
                
            # Call Razorpay Orders API
            url = "https://api.razorpay.com/v1/orders"
            payload = json.dumps({
                "amount": amount_in_paise,
                "currency": currency.upper(),
                "receipt": f"receipt_order_{int(time.time() * 1000)}"
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=payload, headers={
                'Content-Type': 'application/json'
            })
            
            # Setup Basic Auth
            auth_str = f"{key_id}:{key_secret}"
            auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
            req.add_header('Authorization', f'Basic {auth_b64}')
            
            try:
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
            except urllib.error.HTTPError as he:
                error_body = he.read().decode('utf-8')
                print("Razorpay API HTTP Error:", he.code, error_body)
                self.send_json_error(he.code, f"Razorpay API Error: {error_body}")
                return
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "order_id": res_data['id'],
                "amount": res_data['amount'],
                "currency": res_data['currency'],
                "key_id": key_id
            }).encode('utf-8'))
            
        except Exception as e:
            print("Error creating order:", e)
            self.send_json_error(500, "Failed to create Razorpay order")

    def handle_verify_payment(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            order_id = req_data.get('razorpay_order_id')
            payment_id = req_data.get('razorpay_payment_id')
            signature = req_data.get('razorpay_signature')
            
            if not order_id or not payment_id or not signature:
                self.send_json_error(400, "Missing required payment details")
                return
                
            key_secret = env_vars.get('RAZORPAY_KEY_SECRET')
            if not key_secret:
                self.send_json_error(500, "RAZORPAY_KEY_SECRET is not configured in local .env")
                return
                
            msg = f"{order_id}|{payment_id}".encode('utf-8')
            generated_sig = hmac.new(key_secret.encode('utf-8'), msg, hashlib.sha256).hexdigest()
            
            if generated_sig == signature:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "Payment verified successfully"
                }).encode('utf-8'))
            else:
                self.send_json_error(400, "Payment signature verification failed")
                
        except Exception as e:
            print("Error verifying payment:", e)
            self.send_json_error(500, "Internal server error during verification")

    def send_json_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode('utf-8'))

if __name__ == '__main__':
    print(f"Starting local dev server at http://localhost:{PORT}...")
    with socketserver.TCPServer(("", PORT), DevServerHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
