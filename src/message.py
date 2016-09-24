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


if __name__ == "__main__":
    d1 = dumps(123, {"lol": [1, 2, 3, 4, 5, 6, 7]})
    d2 = dumps(123, {"lol": ["lol", "xd", "ai", "ui"], "xd": 10})
    d = d1 + d2
    print("== Dump")
    print(d1)
    print(d2)
    print(d)

    print("== Load")
    nd, obj = loads(d)
    print(obj, nd)
    nd, obj = loads(nd)
    print(obj, nd)
