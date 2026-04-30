"""
auth.py — User registration, login, logout, and password recovery routes
Author: Siddhi Singh (Full-Stack Lead)
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.database import get_db
from app import bcrypt

auth_bp = Blueprint('auth', __name__)

SECURITY_QUESTIONS = [
    'What is your favorite fruit?',
    'What city were you born in?',
    'What was the name of your first school?',
]


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('predict.upload'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('auth/login.html')

        db   = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user and bcrypt.check_password_hash(user['password'], password):
            session.clear()
            session['user_id']  = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('predict.upload'))

        flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('predict.upload'))

    if request.method == 'POST':
        username         = request.form.get('username', '').strip()
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        security_question = request.form.get('security_question', '').strip()
        security_answer   = request.form.get('security_answer', '').strip()

        # Validation
        if not username or not password or not security_question or not security_answer:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if len(security_answer) < 2:
            flash('Recovery answer must be at least 2 characters.', 'danger')
            return render_template('auth/register.html')

        db = get_db()
        existing = db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone()

        if existing:
            flash('Username already taken. Please choose another.', 'danger')
            return render_template('auth/register.html')

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        answer_hash = bcrypt.generate_password_hash(security_answer.lower().strip()).decode('utf-8')
        db.execute(
            'INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)',
            (username, pw_hash, security_question, answer_hash)
        )
        db.commit()

        flash('Account created! Please sign in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', security_questions=SECURITY_QUESTIONS)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if session.get('user_id'):
        return redirect(url_for('predict.upload'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash('Enter your username to continue.', 'danger')
            return render_template('auth/forgot_password.html')

        db = get_db()
        user = db.execute(
            'SELECT id, username, security_question FROM users WHERE username = ?', (username,)
        ).fetchone()

        if not user or not user['security_question']:
            flash('No recovery question is set for that account.', 'danger')
            return render_template('auth/forgot_password.html')

        session['reset_user_id'] = user['id']
        session['reset_username'] = user['username']
        return redirect(url_for('auth.verify_answer'))

    return render_template('auth/forgot_password.html')


@auth_bp.route('/verify-answer', methods=['GET', 'POST'])
def verify_answer():
    if session.get('user_id'):
        return redirect(url_for('predict.upload'))

    reset_user_id = session.get('reset_user_id')
    if not reset_user_id:
        return redirect(url_for('auth.forgot_password'))

    db = get_db()
    user = db.execute(
        'SELECT id, username, security_question, security_answer FROM users WHERE id = ?', (reset_user_id,)
    ).fetchone()

    if not user or not user['security_question']:
        session.pop('reset_user_id', None)
        session.pop('reset_username', None)
        flash('Recovery information is missing for this account.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        answer = request.form.get('security_answer', '').strip().lower()
        if not answer:
            flash('Please enter your answer.', 'danger')
            return render_template('auth/verify_answer.html', question=user['security_question'], username=user['username'])

        if not bcrypt.check_password_hash(user['security_answer'], answer):
            flash('Incorrect answer. Try again.', 'danger')
            return render_template('auth/verify_answer.html', question=user['security_question'], username=user['username'])

        session['password_reset_allowed'] = True
        return redirect(url_for('auth.reset_password'))

    return render_template('auth/verify_answer.html', question=user['security_question'], username=user['username'])


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if session.get('user_id'):
        return redirect(url_for('predict.upload'))

    if not session.get('password_reset_allowed') or not session.get('reset_user_id'):
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('auth/reset_password.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/reset_password.html')

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        db = get_db()
        db.execute(
            'UPDATE users SET password = ? WHERE id = ?',
            (pw_hash, session['reset_user_id'])
        )
        db.commit()

        session.pop('reset_user_id', None)
        session.pop('reset_username', None)
        session.pop('password_reset_allowed', None)

        flash('Password updated successfully. Please sign in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')


@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'success')
    return redirect(url_for('auth.login'))
