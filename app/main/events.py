from .. import socketio
from .storage import rooms
from flask_socketio import join_room, emit
from flask import session
from .utils import create_message

@socketio.on('join_room')
def handle_join_room_event(data):
    room_name = data['room_name']
    username = session.get('username')

    join_room(room_name)

    if username not in rooms[room_name]['users']:
        rooms[room_name]['users'].append(username)
        welcome_message = create_message(username, f'{username} has joined!')
        rooms[room_name]['messages'].append(welcome_message)
        emit('message', welcome_message, to=room_name)
        print(f"{username} joined {room_name}")
    else:
        print(f"{username} is already in {room_name}")

    emit('chat_history', rooms[room_name]['messages'], to=room_name)


@socketio.on('send_message')
def handle_send_message_event(data):
    room_name = data['room_name']
    username = session.get('username')
    message = data['message']

    rooms[room_name]['messages'].append(create_message(username, message))
    emit('message', create_message(username, message), to=room_name)

@socketio.on('leave_room')
def handle_leave_room_event(data):
    room_name = data['room_name']
    username = session.get('username')

    rooms[room_name]['users'].remove(username)
    leave_message = create_message(username, f'{username} has left!')
    rooms[room_name]['messages'].append(leave_message)
    emit('message', leave_message, to=room_name)
    print(f"{username} left {room_name}")
