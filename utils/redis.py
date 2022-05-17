import redis
from utils.parser import load_from_text


def new_redis_client(data_dct):
    try:
        rd = redis.Redis(**data_dct)
        rd.client_list()
        yield rd
    except Exception as e:
        raise e
    finally:
        if rd and rd.connection:
            del rd


def new_redis_client_from_text(text, parse_type):
    try:
        data_dct = load_from_text(parse_type, text)
        return new_redis_client(data_dct)
    except Exception as e:
        raise e
