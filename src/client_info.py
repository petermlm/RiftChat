class ClientInfo:
    def __init__(self, conn):
        self.conn = conn
        self.username = "Unknown"
        self.buff = bytes([])
