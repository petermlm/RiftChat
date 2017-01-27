import json


def dumps(msg_dict):
    js = bytes(json.dumps(msg_dict), "utf-8")
    js_len = len(js).to_bytes(8, byteorder="big")
    return js_len + js

def loads(buff):
    if len(buff) < 8:
        return buff, None

    js_len = int.from_bytes(buff[:8], byteorder="big")

    if len(buff) < 8 + js_len:
        return buff, None

    msg_dict = json.loads(str(buff[8:8+js_len], "utf-8"))

    return buff[8+js_len:], msg_dict
