import pickle

from django.conf import settings
from redis import StrictRedis

from tm.helpers import gen_token, gen_pin


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

    def get(self, key, delete=False):
        value = self.redis.get(key)
        if delete:
            self.delete(key)
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

    def get_pin(self, data):
        pin = gen_pin()
        self.set(pin, data)
        return pin
