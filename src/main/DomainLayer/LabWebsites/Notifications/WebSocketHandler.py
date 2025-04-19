class WebSocketHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebSocketHandler, cls).__new__(cls)
            cls._instance.connected_users = {}  # domain -> { email: sid }
        return cls._instance

    def __init__(self):
        from src.main.DomainLayer.socketio_instance import socketio
        self.socketio = socketio

    def register_user(self, email, domain, sid):
        if domain not in self.connected_users:
            self.connected_users[domain] = {}
        self.connected_users[domain][email] = sid

    def unregister_user_by_sid(self, sid):
        for domain, users in list(self.connected_users.items()):
            for email, stored_sid in list(users.items()):
                if stored_sid == sid:
                    del self.connected_users[domain][email]
                    if not self.connected_users[domain]:
                        del self.connected_users[domain]
                    return

    def emit_to_user(self, domain, email, event, data):
        sid = self.connected_users.get(domain, {}).get(email)
        if sid:
            self.socketio.emit(event, data, to=sid)
            print(f"Emitted {event} to {email} on {domain}")
        else:
            print(f"User {email} on {domain} not connected.")

    def emit_to_all_in_domain(self, domain, event, data):
        users = self.connected_users.get(domain, {})
        for email, sid in users.items():
            self.socketio.emit(event, data, to=sid)
            print(f"Emitted {event} to {email} on {domain}")
