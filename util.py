from datetime import datetime


def get_new_timestamp():
    now = datetime.now()
    return str(datetime.timestamp(now))[:10:]
