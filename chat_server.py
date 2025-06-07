from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = "your_secret_key"
socketio = SocketIO(app)

USERS_FILE = "users.json"
online_users = set()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("chat_select"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    users = load_users()
    username = request.form["username"]
    password = request.form["password"]
    if username in users and users[username] == password:
        session["username"] = username
        return redirect(url_for("chat_select"))
    return "Invalid login. <a href='/'>Try again</a>"

@app.route("/signup", methods=["POST"])
def signup():
    users = load_users()
    username = request.form["username"]
    password = request.form["password"]
    if username in users:
        return "Username already exists. <a href='/'>Try again</a>"
    users[username] = password
    save_users(users)
    session["username"] = username
    return redirect(url_for("chat_select"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@app.route("/chat-select")
def chat_select():
    if "username" not in session:
        return redirect(url_for("home"))
    return render_template("chat_select.html", username=session["username"])

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("home"))
    room_name = request.args.get("room")
    if not room_name:
        return "Room not specified", 400
    return render_template("chat.html", room_name=room_name)

@socketio.on("join")
def handle_join(data):
    username = session.get("username", "Guest")
    room = data.get("room")
    join_room(room)
    emit("message", {
        "type": "join",
        "sender": username,
        "text": f"{username} has joined the room.",
        "id": str(uuid.uuid4())
    }, to=room)

@socketio.on("message")
def handle_message(data):
    username = session.get("username", "Guest")
    room = data.get("room")
    msg_text = data.get("msg")
    reply_to = data.get("replyTo")
    reply_text = data.get("replyText")
    message_payload = {
        "type": "chat",
        "id": str(uuid.uuid4()),
        "sender": username,
        "text": msg_text,
        "replyTo": reply_to,
        "replyText": reply_text
    }
    emit("message", message_payload, to=room)

@socketio.on("typing")
def handle_typing(data):
    username = data.get("username", "Guest")
    room = data.get("room")
    if room:
        socketio.emit("typing", {"username": username}, to=room, skip_sid=request.sid)

@socketio.on("room_select_connect")
def handle_room_select_connect(data):
    username = data.get("username")
    if username:
        online_users.add(username)
        emit("online_users", {"users": list(online_users)}, broadcast=True)

@socketio.on("room_select_disconnect")
def handle_room_select_disconnect(data):
    username = data.get("username")
    if username and username in online_users:
        online_users.remove(username)
        emit("online_users", {"users": list(online_users)}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)