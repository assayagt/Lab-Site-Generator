# socketio_instance.py
from flask_socketio import SocketIO

socketio = None

def init_socketio(app):
    global socketio
    socketio = SocketIO(app, cors_allowed_origins=["http://lsg.cs.bgu.ac.il"], async_mode="gevent")
    return socketio