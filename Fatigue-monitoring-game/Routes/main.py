import sqlite3
from flask import Blueprint, request, jsonify, session, render_template

main = Blueprint('main', __name__)

@main.route('/dashboard')
def dashboard():
    name = session.get('name', 'Guest')
    role = session.get('role', 'unknown')
    your_score_value = 50 
    return render_template('dashboard.html', name=name, score=your_score_value)

@main.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    user_email = data.get('user_email')
    reaction_time = data.get('reaction_time')

    if not user_email or reaction_time is None:
        return jsonify({"error": "Missing data"}), 400

    fatigue_score = max(0, 100 - reaction_time // 10)

    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO game_sessions (user_email, game_type, fatigue_score, reaction_time)
        VALUES (?, ?, ?, ?)
    ''', (user_email, 'reaction', fatigue_score, reaction_time))

    conn.commit()
    conn.close()

    return jsonify({"message": "Score submitted successfully."}), 200
