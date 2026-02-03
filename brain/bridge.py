import os
import datetime
import sys
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_restx import Api, Resource, fields

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
LOG_FILE = os.path.join(BASE_DIR, "brain.log")

# --- IMPORT THE NEW BRAIN ---
sys.path.append(os.path.dirname(BASE_DIR)) # Allow importing from parent
from brain.evolution.smart_developer import SmartDeveloper
from brain.evolution.executor import execute_code

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = os.environ.get('DREAM_SECRET_KEY', 'dream_secret')

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- Simple User Model (for demo) ---
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "admin"
        self.password = "dreamai"  # In production, use hashed passwords!

    def get_id(self):
        return self.id

users = {"admin": User("admin")}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)
developer = SmartDeveloper()

# --- Flask-RESTX API Setup ---
api = Api(app, version='1.0', title='Dream AI API', description='API documentation for Dream AI', doc='/docs')

# --- API Namespace ---
ns = api.namespace('api', description='Dream AI operations')

# --- API Models ---
command_model = api.model('Command', {
    'task': fields.String(required=True, description='Task to perform')
})

# --- API Endpoints ---
@ns.route('/command')
class CommandResource(Resource):
    @api.expect(command_model)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        """Send a command to Dream AI and get the result"""
        try:
            data = api.payload
            task = data.get('task')
            log_message(f"📥 RECEIVED: {task}")
            script_path = developer.generate_solution(task)
            output = execute_code(script_path, timeout_seconds=10, cwd=os.path.dirname(script_path))
            log_message(f"📤 RESULT: {output}")
            return {"status": "success", "output": output}
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            log_message(f"[ERROR] api/command: {e}\n{tb}")
            api.abort(500, str(e))

def log_message(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")


# --- Dashboard Route with Debug Logging ---
@app.route('/')
@login_required
def dashboard():
    try:
        log_message(f"[DEBUG] dashboard: user={getattr(current_user, 'id', None)}, authenticated={getattr(current_user, 'is_authenticated', False)}")
        return render_template('dashboard.html', user=current_user)
    except Exception as e:
        log_message(f"[ERROR] dashboard: {e}")
        return "Dashboard error.", 500

# --- Default Route: Redirect to Login if Not Authenticated ---
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# --- Login Route ---

# --- Login Route with Debug Logging ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        log_message(f"[DEBUG] login attempt: username={username}, success={user is not None and password == getattr(user, 'password', None)}")
        if user and password == user.password:
            login_user(user)
            log_message(f"[DEBUG] login success: user={username}")
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
        log_message(f"[DEBUG] login failed: user={username}")
    return render_template('login.html')

# --- Logout Route ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/brain-log')
def stream_log():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return "".join(f.readlines()[-20:])
        return "Waiting..."
    except Exception as e:
        log_message(f"[ERROR] stream_log: {e}")
        return "Log error.", 500

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
    except Exception as e:
        log_message(f"[ERROR] get_mode: {e}")
        return jsonify({"status": "error", "mode": "automatic", "error": str(e)})

@app.route('/command', methods=['POST'])
def receive_command():
    try:
        data = request.json
        task = data.get('task')
        log_message(f"📥 RECEIVED: {task}")
        # 1. Generate Code
        script_path = developer.generate_solution(task)
        # 2. Run Code
        output = execute_code(script_path, timeout_seconds=10, cwd=os.path.dirname(script_path))
        log_message(f"📤 RESULT: {output}")
        return jsonify({"status": "success", "output": output})
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        log_message(f"[ERROR] receive_command: {e}\n{tb}")
        return jsonify({"status": "error", "error": str(e)})

if __name__ == '__main__':
    # Initialize Log
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f: f.write("SYSTEM REBOOTED.\n")
        
    print(f"🧠 BRIDGE: Online at http://localhost:3000")
    app.run(port=3000)