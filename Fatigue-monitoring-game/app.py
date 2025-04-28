# app.py
from flask import Flask

app = Flask(__name__)

# --- Configurations ---
app.config['DATABASE'] = 'users.db'  # optional, just for clarity

# --- Import and Register Routes ---
from routes.main import main
app.register_blueprint(main)

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
