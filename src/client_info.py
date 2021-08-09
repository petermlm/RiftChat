from random import choice


class ClientInfo:
    def __init__(self, conn):
        self.conn = conn
        self.username = self.randomName()
        self.buff = bytes([])

    def randomName(self):
        choices = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))

        res = ""

        for i in range(10):
            res += chr(choice(choices))

        return res
