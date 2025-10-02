# Anonymous-Chatroom-by-Rudra
# Ephemeral Chat Rooms [Tech Demo]

> **Warning:** 🚧 This is an unfinished project created for demonstration and testing purposes only. It is not intended for real-world use and lacks many security features of a production application.

A real-time, room-based chat application built to experiment with WebSockets, Flask, and deployment workflows on Render.

---

## 🚀 Live Demo

You can try out the live application here:

**[https://anonymous-chatroom-by-rudra-1.onrender.com]**

---

## 🧪 Test Credentials

To explore the chat, feel free to use any of the following pre-loaded accounts:

* **Username:** `admin` | **Password:** `admin123`
* **Username:** `testuser` | **Password:** `password`
* **Username:** `guest` | **Password:** `guest123`

---

## About This Project

This application was developed as a hands-on learning exercise. The primary goal was to build and deploy a full-stack application featuring real-time communication, manage a simple user session system, and understand the deployment process on a modern cloud platform. Users can create chatrooms and let the other users join their private room by letting them know the unique chatroom name. 

---

## Current Features

* **Real-Time Messaging:** Instant message delivery using Flask-SocketIO.
* **Dynamic Chat Rooms:** Ability to create and join unique chat rooms.
* **Simple User Authentication:** A basic login/signup system for session demonstration.
* **Typing Indicators:** See when other users in the room are typing.

---

## Technology Stack

* **Backend:** Python, Flask, Flask-SocketIO
* **Web Server:** Gunicorn with Eventlet
* **Deployment:** Render
* **Frontend:** HTML, CSS, JavaScript

---

## Current Status & Future Goals

This project is a **work-in-progress**. The current implementation uses a simple `users.json` file for user storage as a temporary placeholder, which is not suitable for production.

Future development goals include:
* Transition from `users.json` to a persistent database (e.g., PostgreSQL).
* Implement password hashing for proper security.
* Enhance the user interface and add more chat features.
