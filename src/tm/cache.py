import pickle

from django.conf import settings
from redis import StrictRedis

from tm.helpers import gen_token


class Cache():
    def __init__(self):
        self.redis = StrictRedis(
            settings.REDIS['host'],
            settings.REDIS['port'],
            settings.REDIS['db']
        )

    def set(self, key, data, time=None):
        _data = pickle.dumps(data)
        if time:
            self.redis.setex(key, time, _data)
        else:
            self.redis.set(key, _data)

    def get(self, key):
        value = self.redis.get(key)
        try:
            return pickle.loads(value)
        except:
            return value

    def delete(self, key):
        self.redis.delete(key)

    def get_token(self, data):
        token = gen_token()
        self.set(token, data)
        return token
