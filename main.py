from threading import Thread
from multiprocessing import Process
from time import time as time_now
from StatsManager import StatsManager
from StatServer import StatServer
from TweetCatcher import TweetCatcher
from requests.exceptions import ChunkedEncodingError


def catch_tweets(tweet_catcher):
    """
    Process to be spawned in parallel with main program
    Waits for tweets and processes them as they come in
    """
    while True:
        r = tweet_catcher.api.request('statuses/sample')
        try:
            for tweet_data in r:
                t = Thread(target=tweet_catcher.worker, kwargs={'tweet_data': tweet_data, 'time': time_now()})
                t.start()
        except (ChunkedEncodingError, TypeError) as e:
            # yeah... I don't really know why these errors happen, but just go ahead and keep processing
            print(e)
            continue


def main():
    stat_manager = StatsManager()
    Process(target=catch_tweets, kwargs={'tweet_catcher': TweetCatcher(stat_manager)}).start()
    StatServer(stat_manager).start()


main()