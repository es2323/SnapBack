import sqlite3
import sys
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash, current_app
import subprocess
import random
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/dashboard')
def dashboard():
    name = session.get('name', 'Guest')
    role = session.get('role', 'unknown')
    your_score_value = 50 
    return render_template('dashboard.html', name=name, score=your_score_value)

@main.route('/start_game')
def start_game():
    user_email = session.get('email')
    if not user_email:
        flash("Please log in first", "danger")
        return redirect(url_for('auth.login'))
    game_type = random.choice(['reaction', 'focus'])  # pick one

    try:
        python_exe = sys.executable
        subprocess.Popen([
            python_exe,
            'run_game.py',
            game_type,
            user_email
        ], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

        flash(f"{game_type.capitalize()} game launched.", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for('main.dashboard'))

@main.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    user_email = data.get('user_email')
    game_type = data.get('game_type')
    reaction_time = data.get('reaction_time')

    if not user_email or reaction_time is None or not game_type:
        return jsonify({"error": "Missing data"}), 400

    fatigue_score = max(0, 100 - reaction_time // 10)

    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO game_sessions (user_email, game_type, fatigue_score, reaction_time)
        VALUES (?, ?, ?, ?)
    ''', (user_email, game_type, fatigue_score, reaction_time))

    conn.commit()
    conn.close()

    return jsonify({"message": "Score submitted successfully."}), 200


@main.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        user_email = session.get('email')
        rest = request.form['rest_score']
        alert = request.form['alert_score']
        motivation = request.form['motivation_score']
        discomfort = request.form['discomfort']

        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO check_ins (user_email, rest_score, alert_score, motivation_score, discomfort)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_email, rest, alert, motivation, discomfort))
        conn.commit()
        conn.close()

        flash("Thanks! Your check-in has been submitted.", "success")
        return redirect(url_for('main.dashboard'))

    today = datetime.today().strftime('%A, %d %B %Y')
    return render_template('checkin.html', date=today)
