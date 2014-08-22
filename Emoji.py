import requests


class Emoji:
    """
    This class gets a list of emojis from the source
    """

    def __init__(self):
        r = requests.get('https://raw.githubusercontent.com/iamcal/emoji-data/master/emoji.json')
        self.raw_data = r.json()
        self.emojis = []
        for i in self.raw_data:
            self.emojis.append(self.str_to_emoji(i['unified']))

    def str_to_emoji(self, string):
        """
        Convert base-16 string to unicode string
        """
        if '-' in string:
            split_string = string.split('-')
            return self.str_to_emoji(split_string[0]).join(self.str_to_emoji(split_string[1]))
        else:
            return chr(int(string, 16))

