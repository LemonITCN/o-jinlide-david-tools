global data_pool


def init():
    global data_pool
    data_pool = {}


def set_value(key, value):
    global data_pool
    data_pool[key] = value


def get_value(key):
    global data_pool
    return data_pool[key]


def contain_key(key):
    global data_pool
    return key in data_pool
