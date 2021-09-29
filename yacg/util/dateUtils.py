import datetime


def getCurrentIsoDateTime():
    return datetime.datetime.utcnow().isoformat() + 'Z'
