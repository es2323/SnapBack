from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('snapback.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, role FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            name, role = user
            session['user_email'] = email
            session['user_name'] = name
            session['user_role'] = role
            return redirect(url_for('auth.dashboard'))
        else:
            return render_template('login.html', error="Invalid email or password.")
    
    return render_template('login.html')

@auth.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    name = session.get('user_name')
    role = session.get('user_role')
    
    return render_template('dashboard.html', name=name, role=role)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
