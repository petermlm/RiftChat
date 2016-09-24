import time


class ChatMessage:
    def __init__(self, username, message):
        self.timestamp = int(time.time() * 1000)
        self.username = username
        self.message = message

    def getObj(self):
        return {"timestamp": self.timestamp,
                "username": self.username,
                "message": self.message}
