class ClientInfo:
    def __init__(self, conn):
        self.conn = conn
        self.username = None
        self.buff = bytes([])
