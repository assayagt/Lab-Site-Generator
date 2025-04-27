from flask_socketio import SocketIO

socketio = SocketIO(app, cors_allowed_origins=["http://lsg.cs.bgu.ac.il"], async_mode="gevent")