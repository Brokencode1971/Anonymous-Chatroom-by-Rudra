from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
import json
import os

app = Flask(__name__)
app.secret_key = "any_random_secret_key"
socketio = SocketIO(app)

USERS_FILE = "users.json"

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
    room = data["room"]
    join_room(room)
    send(f"{username} has joined the room.", to=room)

@socketio.on("message")
def handle_message(data):
    username = session.get("username", "Guest")
    room = data["room"]
    msg = data["msg"]
    send(f"{username}: {msg}", to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)