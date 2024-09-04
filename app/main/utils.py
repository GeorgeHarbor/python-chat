from datetime import datetime

def create_message(username, text):
    return {
        'username': username,
        'message': text,
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    }

