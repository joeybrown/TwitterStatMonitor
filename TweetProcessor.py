from threading import Lock
from time import time as time_now, ctime
from collections import Counter
from urllib.parse import urlparse
from Emoji import Emoji


class TweetProcessor():
    """
    This is where most of the heavy lifting happens. This is in charge of counting the things and making calculations
    based off of those counts
    """

    def __init__(self):
        self.lock = Lock()  # for parallel processing
        self.urls = Counter()
        self.emojis = Counter()
        self.hashtags = Counter()
        self.time_start = time_now()
        self.time_end = time_now()
        self.count = 0
        self.emoji_characters = Emoji().emojis  # this is a list of emojis
        self.count_tweet_containing_url = 0
        self.count_tweet_containing_photo_url = 0
        self.count_tweet_containing_emoji = 0

    def __append_urls(self, tweet_data):
        """
        Adds urls to a Counter object for easy processing
        """
        if 'entities' in tweet_data and 'urls' in tweet_data['entities']:
            url_data = tweet_data['entities']['urls']
            urls = []
            for u in url_data:
                parsed_uri = urlparse(u['expanded_url'])
                domain_name = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                urls.append(domain_name)
            if len(urls) > 0:
                self.urls.update(urls)
                self.count_tweet_containing_url += 1

                for url in urls:
                    if 'instagram' or 'pic.twitter.com' in url:
                        self.count_tweet_containing_photo_url += 1

    def __increment(self, tweet_data):
        if 'text' in tweet_data:
            self.count += 1

    def __append_emojis(self, tweet_data):
        """
        Adds emojis to a Counter object for easy processing
        """
        if 'text' in tweet_data:
            text = tweet_data['text']
            text_contains_emoji = False
            for char in self.emoji_characters:
                emoji_count = text.count(char)
                if emoji_count:
                    text_contains_emoji = True
                    self.emojis.update({char: emoji_count})
            if text_contains_emoji:
                self.count_tweet_containing_emoji += 1

    def __append_hashtags(self, tweet_data):
        """
        Adds hashtags to a Counter object for easy processing
        """
        if 'entities' in tweet_data and 'hashtags' in tweet_data['entities']:
            hashtag_data = tweet_data['entities']['hashtags']
            for h in hashtag_data:
                self.hashtags.update({h['text']: 1})

    def get_stats(self):
        seconds = self.time_end - self.time_start
        minutes = seconds/60
        hours = minutes/60

        return {
            'total_tweets': self.count,
            'top_hashtags': dict(self.hashtags.most_common(5)),

            'tweets_per_hr': self.count/hours,
            'tweets_per_min': self.count/minutes,
            'tweets_per_second': self.count/seconds,
            'recording_for_seconds': seconds,
            'time_start': ctime(self.time_start),
            'time_end': ctime(self.time_end),

            'top_emojis': dict(self.emojis.most_common(5)),
            'percent_of_tweets_that_contain_emojis':
                self.count_tweet_containing_url/self.count if self.count else 0.0,

            'top_urls': dict(self.urls.most_common(5)),
            'percent_of_tweets_that_contain_urls': self.count_tweet_containing_url/self.count if self.count else 0.0,
            'perent_of_tweets_that_contain_photo_url':
                self.count_tweet_containing_photo_url/self.count if self.count else 0.0,
        }

    def process(self, tweet_data, time):
        """
        This gets run for each tweet that comes in
        """

        self.lock.acquire()
        self.time_end = time
        try:
            self.__increment(tweet_data)
            self.__append_urls(tweet_data)
            self.__append_emojis(tweet_data)
            self.__append_hashtags(tweet_data)

        finally:
            self.lock.release()
