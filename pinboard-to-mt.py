# -*- coding: utf-8 -*-
import ConfigParser
import datetime
import pinboard
import sys
import urllib2


class PinboardToMT:

    def __init__(self, date=None):
        if date is None:
            date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        self.date = date
        self.load_config()

    def load_config(self):
        config_file = sys.path[0] + '/pinboard.cfg'
        config = ConfigParser.SafeConfigParser()

        try:
            config.readfp(open(config_file))
        except IOError:
            raise PinboardToMTError("Can't read config file: " + config_file)

        settings = ['pinboard_api_token',
                    'mt_blog_id',
                    'mt_author_id',
                    'mt_post_time',
                    'include_tags',
                    'verbose']

        for setting in settings:
            setattr(self, setting, config.get('Settings', setting))

        # Assuming the Pinboard API token is always of the form
        # 'username:SOMECHARACTERS'
        self.pinboard_username = self.pinboard_api_token[:self.pinboard_api_token.index(':')]

    def start(self):
        links = self.get_pinboard_links()
        if len(links) == 0:
            return

        html = self.make_html(links)
        print links 
        print html

    def get_pinboard_links(self):
        try:
            p = pinboard.open(token=self.pinboard_api_token)
        except urllib2.HTTPError, error:
            raise PinboardToMTError("Can't connect to Pinboard: %s" % error)
        links = p.posts(date=self.date)
        self.message("Fetched %s link(s) from Pinboard." % len(links))
        return links

    def make_html(self, links):
        """The HTML that will be the blog entry."""
        html = ''
        for link in links:
            html += "<dt><a href=\"%s\">%s</a></dt>\n<dd>" % (
                                            link['href'], link['description']) 

            if link.get('extended', False):
                html += link['extended']

            if self.include_tags:
                tags = []
                for tag in link.get('tags', []):
                    tags.append(
                        '<a href="https://pinboard.in/u:%s/t:%s">%s</a>' % (
                                            self.pinboard_username, tag, tag))
                html += ' <span class="tags">%s</span>' % ', '.join(tags)

            html += "</dd>\n"

        html = "<dl class=\"links\">\n%s</dl>\n" % html
        return html

        
    def message(self, text):
        "Output debugging info, if in verbose mode."
        if self.verbose:
            print text



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

    

