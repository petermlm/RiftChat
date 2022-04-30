import os


class Config:
    host = os.getenv("HOST", "riftchat-server")
    port = int(os.getenv("PORT", "8000"))
