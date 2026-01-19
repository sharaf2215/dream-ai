import os
import datetime
import subprocess
import sys
from flask import Flask, request, jsonify, render_template

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
LOG_FILE = os.path.join(BASE_DIR, "brain.log")

# --- IMPORT THE NEW BRAIN ---
sys.path.append(os.path.dirname(BASE_DIR)) # Allow importing from parent
from brain.evolution.smart_developer import SmartDeveloper

app = Flask(__name__, template_folder=TEMPLATE_DIR)
developer = SmartDeveloper()

def log_message(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/brain-log')
def stream_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return "".join(f.readlines()[-20:])
    return "Waiting..."

@app.route('/get_mode', methods=['GET'])
def get_mode():
    try:
        if os.path.exists(developer.status_path):
            with open(developer.status_path, "r", encoding="utf-8") as f:
                mode = f.read().strip()
                if mode:
                    return jsonify({"mode": mode})
        return jsonify({"mode": "💤 IDLE"})
    except Exception:
        return jsonify({"mode": "💤 IDLE"})

@app.route('/command', methods=['POST'])
def receive_command():
    data = request.json
    task = data.get('task')
    
    log_message(f"📥 RECEIVED: {task}")
    
    # 1. Generate Code
    script_path = developer.generate_solution(task)
    
    # 2. Run Code
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        if not output: output = "Done (No Output)"
    except Exception as e:
        output = f"Error: {e}"

    log_message(f"📤 RESULT: {output}")
    return jsonify({"status": "success", "output": output})

if __name__ == '__main__':
    # Initialize Log
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f: f.write("SYSTEM REBOOTED.\n")
        
    print(f"🧠 BRIDGE: Online at http://localhost:3000")
    app.run(port=3000)