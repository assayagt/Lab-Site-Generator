from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins=["http://localhost:3000", "http://localhost:3001"], async_mode="threading")