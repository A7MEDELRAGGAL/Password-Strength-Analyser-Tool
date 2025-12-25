import http.server
import socketserver
import urllib.parse
import hashlib
import os
import re
import webbrowser

# ==========================================
# Project Configuration
# Student: Ahmed Mohammed Saad El-Raggal (ID: 2221300)
# ==========================================
STUDENT_NAME = "Ahmed Mohammed Saad El-Raggal"
PORT = 8000

# ==========================================
# Logic Layer
# ==========================================
def check_strength(password):
    score = 0
    feedback = []
    if len(password) >= 8: score += 1
    else: feedback.append("Weak Length (< 8)")
    if re.search(r"\d", password): score += 1
    else: feedback.append("No Numbers")
    if re.search(r"[A-Z]", password): score += 1
    else: feedback.append("No Uppercase")
    if re.search(r"[!@#$%^&*]", password): score += 1
    else: feedback.append("No Special Chars")

    if score < 2: return "WEAK", "#e74c3c", feedback
    elif score < 4: return "MEDIUM", "#f39c12", feedback
    else: return "STRONG", "#27ae60", feedback

def get_secure_hash(password):
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt, hashed

# ==========================================
# HTML Template
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Password Security Tool</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f6f7; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background-color: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 500px; text-align: center; }
        h1 { color: #2c3e50; margin-bottom: 5px; }
        .subtitle { color: #7f8c8d; font-size: 14px; margin-bottom: 25px; }
        input[type="text"] { width: 80%; padding: 12px; margin-bottom: 15px; border: 2px solid #ecf0f1; border-radius: 6px; outline: none; transition: 0.3s; }
        button { background-color: #3498db; color: white; padding: 12px; border: none; border-radius: 6px; cursor: pointer; width: 100%; }
        .result-box { margin-top: 30px; text-align: left; background: #fafafa; padding: 20px; border-radius: 8px; border-left: 5px solid #ccc; display: {display_style}; }
        .hash-code { background: #2c3e50; color: #2ecc71; padding: 10px; border-radius: 4px; font-family: monospace; word-break: break-all; font-size: 12px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Password Analyser</h1>
        <div class="subtitle">Developed by: {student_name}</div>
        <form method="POST">
            <input type="text" name="password" placeholder="Enter password..." required>
            <button type="submit">Analyze & Encrypt</button>
        </form>
        <div class="result-box" style="border-left-color: {color};">
            <h3>Result: <span style="background-color: {color}; color: white; padding: 2px 8px; border-radius: 4px;">{strength}</span></h3>
            <p>{tips}</p>
            <hr>
            <small>Salt:</small><div class="hash-code" style="color:#f1c40f">{salt}</div>
            <small>Hash:</small><div class="hash-code">{hash_result}</div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# Server Handler
# ==========================================
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = HTML_TEMPLATE.replace("{student_name}", STUDENT_NAME).replace("{display_style}", "none").replace("{color}", "#ccc").replace("{strength}", "").replace("{tips}", "").replace("{salt}", "").replace("{hash_result}", "")
        self.wfile.write(page.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = urllib.parse.parse_qs(post_data.decode('utf-8'))
        password = params.get('password', [''])[0]
        strength, color, tips = check_strength(password)
        salt, hashed = get_secure_hash(password)
        
        page = HTML_TEMPLATE.replace("{student_name}", STUDENT_NAME).replace("{display_style}", "block").replace("{color}", color).replace("{strength}", strength).replace("{tips}", ", ".join(tips) if tips else "Excellent!").replace("{salt}", salt).replace("{hash_result}", hashed)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

if __name__ == "__main__":
    print(f"Starting Local Server at http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}")
    try:
        with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass
