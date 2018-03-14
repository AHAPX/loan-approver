import pickle

from redis import StrictRedis

from django.conf import settings


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
