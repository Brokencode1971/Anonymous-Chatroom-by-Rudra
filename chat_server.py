from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/room/<room_name>')
def room(room_name):
    return render_template('chat.html', room_name=room_name)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    send(f"🔔 Someone joined room: {room}", to=room)

@socketio.on('message')
def handle_message(data):
    msg = data['msg']
    room = data['room']
    send(msg, to=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)