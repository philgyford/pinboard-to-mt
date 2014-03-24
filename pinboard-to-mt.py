import ConfigParser
import pinboard
import sys


class PinboardToMT:

    def __init__(self, date=None):
        self.date = date
        self.load_config()

    def load_config(self):
        config_file = sys.path[0] + '/pinboard.cfg'
        config = ConfigParser.SafeConfigParser()

        try:
            config.readfp(open(config_file))
        except IOError:
            raise PinboardToMTError("Can't read config file: " + config_file)

        settings = ['pinboard_api_token', 'verbose']

        for setting in settings:
            setattr(self, setting, config.get('Settings', setting))

    def start(self):
        self.get_pinboard_links()

    def get_pinboard_links(self):
        p = pinboard.open(token=self.pinboard_api_token)
        print p
        posts = p.posts(date='2014-03-16')
        print posts
        



class PinboardToMTError(Exception):
    pass


def main():
    date = None
    if len(sys.argv) == 2:
        date = sys.argv[1]

    p = PinboardToMT(date)
    p.start()


if __name__ == "__main__":
    main()

    

