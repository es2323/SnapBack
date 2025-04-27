from app import db  # assuming db = SQLAlchemy(app) in your app.py

class GameSession(db.Model):
    __tablename__ = 'game_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    fatigue_score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())  # Auto timestamp

    def __init__(self, user_email, fatigue_score):
        self.user_email = user_email
        self.fatigue_score = fatigue_score

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
