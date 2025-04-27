from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.main import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snapback.db'  # or whatever you named it
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import your routes
from routes.main import main
app.register_blueprint(main)
