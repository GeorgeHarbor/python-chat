from flask import session, render_template, redirect, url_for, request, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from . import main
from .db import get_db_connection
from .storage import rooms
from .utils import create_message
import uuid

@main.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('.login'))




@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'guest_login':
            session['username'] = f'guest-{uuid.uuid4().hex[:8]}'

            return redirect(url_for('.index'))
        else:
            username = request.form['username']
            password = request.form['password']

            with get_db_connection() as conn:
                user = conn.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
                if user and check_password_hash(user['password'], password):
                    session['username'] = user['username']
                    return redirect(url_for('.index'))
                else:
                    flash('Invalid username or password.', 'danger')
                    return render_template('login.html')

    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        with get_db_connection() as conn:
            try:
                conn.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                flash('Registration successful! Please log in.', 'success') 
                return redirect(url_for('.login'))
            except sqlite3.IntegrityError:
                flash('Username already exists. Try a different one.', 'danger')
                return render_template('register.html')
    return render_template('register.html')


@main.route('/logout')
def logout():
    session.pop('username', None)  
    session.pop('room', None)  
    session.pop('player_marker', None)  
    flash('You have been logged out.', 'info')
    return redirect(url_for('.login'))





@main.route('/join_room', methods=['POST'])
def join_room():
    room_name = request.form.get('room_name')
    username = session.get('username')

    if room_name not in rooms:
        rooms[room_name] = {
            'users': [username], 
            'messages': [create_message(username, f'Room created by {username}!')]
        }
    return redirect(url_for('main.room', room_name=room_name))

@main.route('/room/<room_name>')
def room(room_name):
    room = rooms[room_name]
    return render_template('room.html', room_name=room_name, room = room)

