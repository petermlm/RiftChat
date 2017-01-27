from datetime import datetime
import sys


log_dt_format = "%Y-%m-%d %H:%M:%S"


def stdout(msg):
    log(sys.stdout, msg)

def stderr(msg):
    log(sys.stderr, msg)

def log(fd, msg):
    now = datetime.now()
    dt = now.strftime(log_dt_format)

    fd.write("{} {}\n".format(dt, msg))
