from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
from flask import flash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, role, team FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['email'] = email
            session['name'] = user[0]
            session['role'] = user[1]

            if user[1] == 'manager':
                return redirect(url_for('main.manager_dashboard'))
            elif user[1] == 'hr':
                return redirect(url_for('main.hr_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))

        else:
            flash("Invalid email or password.")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    name = session.get('name')
    role = session.get('role')
    
    return render_template('dashboard.html', name=name, role=role)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
