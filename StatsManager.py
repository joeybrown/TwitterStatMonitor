from redis import StrictRedis
from multiprocessing import Lock
from Variables import REDIS_SERVER_PORT, REDIS_SERVER_HOST


class StatsManager:
    """
    Singleton that is shared between threads that is used to get and set stats to and from redis
    """

    def __init__(self):
        self.db = StrictRedis(host=REDIS_SERVER_HOST, port=REDIS_SERVER_PORT, db=0)
        self.lock = Lock()
        self.set({'total_tweets': 0})

    def set(self, stats):
        self.lock.acquire()
        try:
            self.db.set('stats', stats)
        finally:
            self.lock.release()

    def get(self):
        with self.lock:
            return eval(self.db.get('stats'))
