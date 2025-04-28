# app.py
from flask import Flask
from routes.auth import auth



# --- App Initialization ---
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# --- Configurations (Optional) ---
app.config['DATABASE'] = 'users.db'  # If you want to access this elsewhere

# --- Import and Register Blueprints ---
from routes.main import main
from routes.auth import auth  # New login system

app.register_blueprint(main)
app.register_blueprint(auth)

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
