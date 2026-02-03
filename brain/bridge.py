import os
import datetime
import sys
from flask import Flask, request, jsonify, render_template

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
LOG_FILE = os.path.join(BASE_DIR, "brain.log")

# --- IMPORT THE NEW BRAIN ---
sys.path.append(os.path.dirname(BASE_DIR)) # Allow importing from parent
from brain.evolution.smart_developer import SmartDeveloper
from brain.evolution.executor import execute_code

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
        mode = "automatic"
        if os.path.exists(developer.status_path):
            with open(developer.status_path, "r", encoding="utf-8") as f:
                stored = f.read().strip()
                if stored:
                    mode = stored
        return jsonify({"status": "success", "mode": mode})
    except Exception:
        return jsonify({"status": "success", "mode": "automatic"})

@app.route('/command', methods=['POST'])
def receive_command():
    data = request.json
    task = data.get('task')
    
    log_message(f"📥 RECEIVED: {task}")
    
    # 1. Generate Code
    script_path = developer.generate_solution(task)
    
    # 2. Run Code
    output = execute_code(script_path, timeout_seconds=10, cwd=os.path.dirname(script_path))

    log_message(f"📤 RESULT: {output}")
    return jsonify({"status": "success", "output": output})

if __name__ == '__main__':
    # Initialize Log
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f: f.write("SYSTEM REBOOTED.\n")
        
    print(f"🧠 BRIDGE: Online at http://localhost:3000")
    app.run(port=3000)