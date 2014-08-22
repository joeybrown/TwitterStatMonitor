from TwitterAPI import TwitterAPI
from TweetProcessor import TweetProcessor
from Variables import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET


class TweetCatcher:
    """
    Connects to twitter, catches tweets, and kicks off processing for those tweets
    """

    def __init__(self, stat_manager):
        self.processor = TweetProcessor()
        self.api = TwitterAPI(
            CONSUMER_KEY,
            CONSUMER_SECRET,
            ACCESS_TOKEN_KEY,
            ACCESS_TOKEN_SECRET)
        self.stat_manager = stat_manager

    def worker(self, tweet_data, time):
        """
        Worker for parallel processing
        """
        self.processor.process(tweet_data, time)
        self.stat_manager.set(self.processor.get_stats())


