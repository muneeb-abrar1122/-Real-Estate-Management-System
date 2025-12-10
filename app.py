from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'union-estate-secret-key-2024')
app.config['WTF_CSRF_ENABLED'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Admin session lasts 24 hours

# Initialize extensions
csrf = CSRFProtect(app)
CORS(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Data directory
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

CLIENTS_FILE = DATA_DIR / 'clients.json'
USERS_FILE = DATA_DIR / 'users.json'
ADMIN_CONFIG_FILE = DATA_DIR / 'admin_config.json'

# Helper functions for JSON file operations
def read_json_file(filepath):
    """Read JSON file, return empty list if file doesn't exist"""
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

def write_json_file(filepath, data):
    """Write data to JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def get_admin_password():
    """Get admin password from config file"""
    if ADMIN_CONFIG_FILE.exists():
        try:
            with open(ADMIN_CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('password', 'admin123')
        except:
            pass
    return 'admin123'

def set_admin_password(new_password):
    """Set admin password in config file"""
    config = {
        'password': new_password,
        'last_updated': datetime.now().isoformat()
    }
    try:
        with open(ADMIN_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except:
        return False

# User class for Flask-Login
class User:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    users = read_json_file(USERS_FILE)
    if any(u['username'] == username for u in users):
        return User(username)
    return None

# --- Main App Routes ---

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = read_json_file(USERS_FILE)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        
        if user:
            user_obj = User(username)
            login_user(user_obj)
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@csrf.exempt
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        users = read_json_file(USERS_FILE)
        
        # Check if username already exists
        if any(u['username'] == username for u in users):
            flash('Username already exists')
            return render_template('register.html')
        
        # Create new user
        new_user = {
            'id': str(int(datetime.now().timestamp() * 1000)),
            'username': username,
            'email': email,
            'password': password,
            'created_at': datetime.now().isoformat()
        }
        
        users.append(new_user)
        
        if write_json_file(USERS_FILE, users):
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

# --- Admin Panel Routes ---

@app.route('/admin/login', methods=['GET', 'POST'])
@csrf.exempt
def admin_login():
    # Always show login page - no session check
    if request.method == 'POST':
        password = request.form.get('password')
        admin_password = get_admin_password()
        
        if password == admin_password:
            session['admin_logged_in'] = True
            return redirect('/admin')
            
        flash('Invalid admin password')
    
    return render_template('admin/admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Clear session after access - require password next time
    session.pop('admin_logged_in', None)
    
    clients = read_json_file(CLIENTS_FILE)
    users = read_json_file(USERS_FILE)
    recent_clients = clients[:5] if clients else []
    
    return render_template('admin/dashboard.html', 
                         total_clients=len(clients),
                         total_users=len(users),
                         recent_clients=recent_clients)

# Admin Settings
@app.route('/admin/settings', methods=['GET', 'POST'])
@csrf.exempt
def admin_settings():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        admin_password = get_admin_password()
        
        if current_password != admin_password:
            flash('Current password is incorrect')
        elif new_password != confirm_password:
            flash('New passwords do not match')
        elif len(new_password) < 6:
            flash('Password must be at least 6 characters')
        else:
            if set_admin_password(new_password):
                flash('Admin password changed successfully!')
            else:
                flash('Failed to update password')
        
    clients = read_json_file(CLIENTS_FILE)
    users = read_json_file(USERS_FILE)
    
    return render_template('admin/settings.html',
                         total_clients=len(clients),
                         total_users=len(users))

# Admin Users Management
@app.route('/admin/users/list')
def admin_users_list():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    users = read_json_file(USERS_FILE)
    # Add created_at as datetime object for template
    for user in users:
        if 'created_at' in user:
            try:
                user['created_at'] = datetime.fromisoformat(user['created_at'])
            except:
                user['created_at'] = None
    
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/create', methods=['GET', 'POST'])
@csrf.exempt
def admin_users_create():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        users = read_json_file(USERS_FILE)
        
        # Check if username exists
        if any(u['username'] == username for u in users):
            flash('Username already exists')
            return render_template('admin/user_form.html', action='create')
        
        new_user = {
            'id': str(int(datetime.now().timestamp() * 1000)),
            'username': username,
            'email': email,
            'password': password,
            'created_at': datetime.now().isoformat()
        }
        
        users.append(new_user)
        
        if write_json_file(USERS_FILE, users):
            flash('User created successfully!')
            return redirect(url_for('admin_users_list'))
        else:
            flash('Failed to create user')
    
    return render_template('admin/user_form.html', action='create', user=None)

@app.route('/admin/users/edit/<user_id>', methods=['GET', 'POST'])
@csrf.exempt
def admin_users_edit(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    users = read_json_file(USERS_FILE)
    user = next((u for u in users if u.get('id') == user_id), None)
    
    if not user:
        flash('User not found')
        return redirect(url_for('admin_users_list'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username exists for other users
        if any(u['username'] == username and u.get('id') != user_id for u in users):
            flash('Username already exists')
            return render_template('admin/user_form.html', action='edit', user=user)
        
        # Update user
        for i, u in enumerate(users):
            if u.get('id') == user_id:
                users[i]['username'] = username
                users[i]['email'] = email
                if password:  # Only update password if provided
                    users[i]['password'] = password
                break
        
        if write_json_file(USERS_FILE, users):
            flash('User updated successfully!')
            return redirect(url_for('admin_users_list'))
        else:
            flash('Failed to update user')
    
    return render_template('admin/user_form.html', action='edit', user=user)

@app.route('/admin/users/delete/<user_id>', methods=['POST'])
@csrf.exempt
def admin_users_delete(user_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = read_json_file(USERS_FILE)
    updated_users = [u for u in users if u.get('id') != user_id]
    
    if write_json_file(USERS_FILE, updated_users):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to delete'}), 500

# Admin Clients Management
@app.route('/admin/clients')
def admin_clients():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    clients = read_json_file(CLIENTS_FILE)
    return render_template('admin/clients.html', clients=clients)

@app.route('/admin/clients/create', methods=['GET', 'POST'])
@csrf.exempt
def admin_clients_create():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        new_client = {
            'id': str(int(datetime.now().timestamp() * 1000)),
            'name': request.form.get('name', ''),
            'contact': request.form.get('contact', ''),
            'society': request.form.get('society', ''),
            'plotNo': request.form.get('plotNo', ''),
            'block': request.form.get('block', 'A'),
            'price': request.form.get('price', ''),
            'size': request.form.get('size', ''),
            'date': request.form.get('date', ''),
            'description': request.form.get('description', ''),
            'createdAt': datetime.now().isoformat()
        }
        
        clients = read_json_file(CLIENTS_FILE)
        clients.insert(0, new_client)
        
        if write_json_file(CLIENTS_FILE, clients):
            flash('Client created successfully!')
            return redirect(url_for('admin_clients'))
        else:
            flash('Failed to create client')
    
    return render_template('admin/client_form.html', edit_mode=False, edit_client=None)

@app.route('/admin/clients/edit/<client_id>', methods=['GET', 'POST'])
@csrf.exempt
def admin_clients_edit(client_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    clients = read_json_file(CLIENTS_FILE)
    client = next((c for c in clients if c.get('id') == client_id), None)
    
    if not client:
        flash('Client not found')
        return redirect(url_for('admin_clients'))
    
    if request.method == 'POST':
        for i, c in enumerate(clients):
            if c.get('id') == client_id:
                clients[i].update({
                    'name': request.form.get('name', ''),
                    'contact': request.form.get('contact', ''),
                    'society': request.form.get('society', ''),
                    'plotNo': request.form.get('plotNo', ''),
                    'block': request.form.get('block', 'A'),
                    'price': request.form.get('price', ''),
                    'size': request.form.get('size', ''),
                    'date': request.form.get('date', ''),
                    'description': request.form.get('description', '')
                })
                break
        
        if write_json_file(CLIENTS_FILE, clients):
            flash('Client updated successfully!')
            return redirect(url_for('admin_clients'))
        else:
            flash('Failed to update client')
    
    return render_template('admin/client_form.html', edit_mode=True, edit_client=client)

@app.route('/admin/clients/delete/<client_id>', methods=['POST'])
@csrf.exempt
def admin_clients_delete(client_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    clients = read_json_file(CLIENTS_FILE)
    updated_clients = [c for c in clients if c.get('id') != client_id]
    
    if write_json_file(CLIENTS_FILE, updated_clients):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to delete'}), 500

# --- API Routes - JSON File Storage ---

@app.route('/api/clients', methods=['GET'])
@login_required
def get_clients():
    """Get all clients from JSON file"""
    clients = read_json_file(CLIENTS_FILE)
    return jsonify(clients)

@app.route('/api/clients', methods=['POST'])
@csrf.exempt
@login_required
def create_client():
    """Create new client in JSON file"""
    data = request.json
    clients = read_json_file(CLIENTS_FILE)
    
    # Generate unique ID
    new_client = {
        'id': str(int(datetime.now().timestamp() * 1000)),
        **data,
        'createdAt': datetime.now().isoformat()
    }
    
    clients.insert(0, new_client)
    
    if write_json_file(CLIENTS_FILE, clients):
        return jsonify(new_client), 201
    else:
        return jsonify({'error': 'Failed to save'}), 500

@app.route('/api/clients/<client_id>', methods=['PUT'])
@csrf.exempt
@login_required
def update_client(client_id):
    """Update client in JSON file"""
    data = request.json
    clients = read_json_file(CLIENTS_FILE)
    
    # Find and update client
    for i, client in enumerate(clients):
        if client.get('id') == client_id:
            clients[i] = {**client, **data}
            if write_json_file(CLIENTS_FILE, clients):
                return jsonify(clients[i])
            else:
                return jsonify({'error': 'Failed to update'}), 500
    
    return jsonify({'error': 'Client not found'}), 404

@app.route('/api/clients/<client_id>', methods=['DELETE'])
@csrf.exempt
@login_required
def delete_client(client_id):
    """Delete client from JSON file"""
    clients = read_json_file(CLIENTS_FILE)
    
    # Filter out the client
    updated_clients = [c for c in clients if c.get('id') != client_id]
    
    if write_json_file(CLIENTS_FILE, updated_clients):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to delete'}), 500

@app.route('/api/clients/import', methods=['POST'])
@csrf.exempt
@login_required
def import_clients():
    """Import clients from uploaded JSON"""
    data = request.json
    
    if write_json_file(CLIENTS_FILE, data):
        return jsonify({'success': True, 'count': len(data)})
    else:
        return jsonify({'error': 'Failed to import'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
