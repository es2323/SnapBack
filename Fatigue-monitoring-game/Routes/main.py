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
    fatigue_score = data.get('fatigue_score')
    accuracy = data.get('accuracy')
    errors = data.get('errors')
    completion_time = data.get('completion_time')

    if not all([user_email, game_type, reaction_time is not None, fatigue_score is not None]):
        return jsonify({"error": "Missing required data"}), 400

    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO game_sessions 
        (user_email, game_type, fatigue_score, reaction_time, accuracy, errors, completion_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_email, game_type, fatigue_score, reaction_time, accuracy, errors, completion_time))

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

@main.route('/results')
def results():
    user_email = session.get('email')
    if not user_email:
        flash("Login required.", "danger")
        return redirect(url_for('auth.login'))

    conn = sqlite3.connect("main.db", timeout=5)
    cursor = conn.cursor()

    # Get latest game data
    cursor.execute("""
        SELECT fatigue_score, reaction_time, accuracy, errors, completion_time
        FROM game_sessions
        WHERE user_email = ?
        ORDER BY timestamp DESC LIMIT 1
    """, (user_email,))
    game = cursor.fetchone()

    # Get latest check-in data
    cursor.execute("""
        SELECT rest_score, alert_score, motivation_score, discomfort
        FROM check_ins
        WHERE user_email = ?
        ORDER BY timestamp DESC LIMIT 1
    """, (user_email,))
    checkin = cursor.fetchone()
    conn.close()

    if not game or not checkin:
        flash("Not enough data. Please complete a game and check-in first.", "warning")
        return redirect(url_for('main.dashboard'))

    # Basic logic to blend survey + game score
    fatigue_game = game[0]
    survey_avg = sum(checkin[:3]) / 3  # rest, alert, motivation
    survey_bonus = (survey_avg - 3) * 5  # Range: [-10 to +10]

    discomfort_penalty = -5 if checkin[3] == "Yes" else 0
    final_fatigue = min(100, max(0, fatigue_game + survey_bonus + discomfort_penalty))

    # Build message
    if final_fatigue >= 80:
        message = "You're performing well today! Keep it up. 🎉"
    elif final_fatigue >= 60:
        message = "Mild signs of tiredness. Consider short breaks and hydration. 🧘‍♂️"
    elif final_fatigue >= 40:
        message = "You're showing signs of fatigue. Plan lighter tasks. ⚠️"
    else:
        message = "You seem very fatigued. Take care of yourself. 🛌"

    return render_template("results.html",
        score=int(final_fatigue),
        reaction=game[1],
        accuracy=game[2],
        errors=game[3],
        time=game[4],
        message=message
    )

@main.route('/manager_dashboard')
def manager_dashboard():
    if session.get('role') != 'manager':
        return redirect(url_for('main.dashboard'))  # Restrict access
    
    team = session.get('team')  # E.g., 'Team A'
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    # 1. Average Team Fatigue Score
    cursor.execute('''
        SELECT AVG(fatigue_score)
        FROM game_sessions
        WHERE user_email IN (
            SELECT email FROM users WHERE team = ?
        )
    ''', (team,))
    avg_score = round(cursor.fetchone()[0] or 0)

    # 2. Number of High Fatigue Alerts (score < 40 in last 3 days)
    cursor.execute('''
        SELECT date(timestamp), AVG(fatigue_score)
        FROM game_sessions
        WHERE user_email IN (SELECT email FROM users WHERE team = ?)
        GROUP BY date(timestamp)
        ORDER BY date(timestamp) DESC
        LIMIT 7
    ''', (team,))
    rows = cursor.fetchall()
    labels = [row[0] for row in rows][::-1]
    scores = [round(row[1], 1) for row in rows][::-1]

    high_alerts = sum(1 for row in rows[:3] if row[1] < 40)

    # 3. Check-in completion rate (past 7 days)
    cursor.execute('''
        SELECT COUNT(*) FROM check_ins 
        WHERE timestamp >= date('now', '-7 day') 
        AND user_email IN (SELECT email FROM users WHERE team = ?)
    ''', (team,))
    checkin_done = cursor.fetchone()[0]

    cursor.execute('''
        SELECT COUNT(*) FROM users WHERE team = ?
    ''', (team,))
    total_team = cursor.fetchone()[0]
    checkin_rate = int((checkin_done / (total_team * 7)) * 100) if total_team > 0 else 0

    conn.close()

    return render_template("manager_dashboard.html", 
    avg_score=avg_score, high_alerts=high_alerts, 
    checkin_rate=checkin_rate, labels=labels, scores=scores
)