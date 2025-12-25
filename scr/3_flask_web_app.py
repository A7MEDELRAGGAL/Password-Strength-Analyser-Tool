from flask import Flask, request, render_template_string
import hashlib
import os
import re

app = Flask(__name__)

# ==========================================
# بيانات المشروع
# ==========================================
STUDENT_NAME = "Ahmed Mohammed Saad El-Raggal"
STUDENT_ID = "2221300"

# ==========================================
# المنطق البرمجي (Backend Logic)
# ==========================================
def analyze_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8: score += 1
    else: feedback.append("Weak Length (Must be 8+)")
    if re.search(r"\d", password): score += 1
    else: feedback.append("Missing Numbers (0-9)")
    if re.search(r"[A-Z]", password): score += 1
    else: feedback.append("Missing Uppercase (A-Z)")
    if re.search(r"[!@#$%^&*]", password): score += 1
    else: feedback.append("Missing Symbols (!@#$)")

    if score < 2: return "WEAK", "#e74c3c", feedback
    elif score < 4: return "MEDIUM", "#f39c12", feedback
    else: return "STRONG", "#27ae60", feedback

def detailed_encryption_process(password):
    # 1. الهاش العادي (بدون سالت) - غير آمن
    # SHA-256(Password)
    raw_hash = hashlib.sha256(password.encode()).hexdigest()

    # 2. توليد السالت (Random Salt)
    salt = os.urandom(16).hex()
    
    # 3. دمج الباسورد مع السالت (Combination)
    # هذا ما يدخل فعلياً في دالة الهاش المؤمنة
    combined_data = salt + password

    # 4. الهاش النهائي المؤمن
    # SHA-256(Salt + Password)
    final_hash = hashlib.sha256(combined_data.encode()).hexdigest()
    
    return raw_hash, salt, combined_data, final_hash

# ==========================================
# واجهة الويب (HTML/CSS)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Crypto Tool</title>
    <style>
        :root { --primary: #2c3e50; --accent: #3498db; --bg: #f4f6f7; }
        body { font-family: 'Segoe UI', monospace, sans-serif; background-color: var(--bg); margin: 0; padding: 20px; color: #333; }
        
        .container { max-width: 800px; margin: 0 auto; background: #fff; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
        
        .header { text-align: center; border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }
        .header h1 { color: var(--primary); margin: 0; }
        .header p { color: #7f8c8d; font-size: 0.9rem; }

        /* Input Styles */
        .input-group { position: relative; margin-bottom: 20px; }
        input[type="password"], input[type="text"] { width: 100%; padding: 15px; padding-right: 50px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; outline: none; box-sizing: border-box; }
        input:focus { border-color: var(--accent); }
        .toggle-btn { position: absolute; right: 15px; top: 15px; cursor: pointer; font-size: 1.2rem; }
        
        button { width: 100%; padding: 15px; background: var(--accent); color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #2980b9; }

        /* Results Styles */
        .results-area { display: {{ show_results }}; animation: fadeIn 0.5s; }
        
        .section-title { margin-top: 30px; font-size: 1.1rem; font-weight: bold; color: var(--primary); border-left: 4px solid var(--accent); padding-left: 10px; }
        
        .card { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 15px; }
        .card strong { display: block; font-size: 0.85rem; color: #555; margin-bottom: 5px; }
        
        .code { font-family: 'Consolas', 'Courier New', monospace; font-size: 0.9rem; word-break: break-all; padding: 10px; border-radius: 4px; }
        
        .bad { background: #ffeaea; color: #c0392b; border: 1px solid #ffcccc; } /* Red for Weak */
        .neutral { background: #e8f6f3; color: #16a085; border: 1px solid #d1f2eb; } /* Greenish for Salt */
        .good { background: #2c3e50; color: #2ecc71; border: 1px solid #34495e; } /* Dark for Final */

        .arrow { text-align: center; font-size: 1.5rem; color: #ccc; margin: 5px 0; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Encryption & Hashing Lab</h1>
        <p>Student: {{ name }} | ID: {{ id }}</p>
    </div>

    <form method="POST">
        <div class="input-group">
            <input type="password" id="pwdInput" name="password" placeholder="Enter password..." required value="{{ input_pwd }}">
            <span class="toggle-btn" onclick="togglePassword()">Show</span>
        </div>
        <button type="submit">Analyze & Secure</button>
    </form>

    {% if show_results == 'block' %}
    <div class="results-area">
        
        <div class="section-title">1. Password Strength Analysis</div>
        <div class="card" style="border-left: 5px solid {{ color }};">
            <h3 style="margin:0; color:{{ color }};">{{ strength }}</h3>
            {% if tips %}
            <ul style="margin: 10px 0 0 20px; color: #555; font-size: 0.9rem;">
                {% for tip in tips %} <li>{{ tip }}</li> {% endfor %}
            </ul>
            {% endif %}
        </div>

        <div class="section-title">2. Hashing Process (Step-by-Step)</div>
        
        <div class="card">
            <strong>Step 1: Raw Hash (Unsafe - No Salt)</strong>
            <div class="code bad">{{ raw_hash }}</div>
            <small style="color:#c0392b;">*If two users have the same password, they get this same hash.*</small>
        </div>

        <div class="arrow">Adding Protection</div>

        <div class="card">
            <strong>Step 2: Generated Salt (Random Value)</strong>
            <div class="code neutral">{{ salt }}</div>
        </div>

        <div class="card">
            <strong>Step 3: Combined Data (Salt + Password)</strong>
            <div class="code neutral" style="color:#333; background:#fff;">{{ combined_data }}</div>
            <small style="color:#7f8c8d;">*This is the actual text being hashed now.*</small>
        </div>

        <div class="arrow">Final Security</div>

        <div class="card" style="background: #eefcf3; border-color: #2ecc71;">
            <strong>Step 4: Final Stored Hash (SHA-256 of Combined Data)</strong>
            <div class="code good">{{ final_hash }}</div>
            <small style="color:#27ae60;">*This is what gets saved in the Database.*</small>
        </div>

    </div>
    {% endif %}
</div>

<script>
    function togglePassword() {
        var x = document.getElementById("pwdInput");
        if (x.type === "password") x.type = "text";
        else x.type = "password";
    }
</script>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    data = {
        'name': STUDENT_NAME, 'id': STUDENT_ID,
        'show_results': 'none', 'input_pwd': '',
        'strength': '', 'color': '', 'tips': [],
        'raw_hash': '', 'salt': '', 'combined_data': '', 'final_hash': ''
    }
    
    if request.method == 'POST':
        pwd = request.form.get('password')
        
        # 1. تحليل القوة
        strength, color, tips = analyze_strength(pwd)
        
        # 2. عملية التشفير التفصيلية
        raw_h, slt, comb, fin_h = detailed_encryption_process(pwd)
        
        data.update({
            'show_results': 'block', 'input_pwd': pwd,
            'strength': strength, 'color': color, 'tips': tips,
            'raw_hash': raw_h,
            'salt': slt,
            'combined_data': comb,
            'final_hash': fin_h
        })
        
    return render_template_string(HTML_TEMPLATE, **data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)