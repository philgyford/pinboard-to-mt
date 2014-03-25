# -*- coding: utf-8 -*-
import ConfigParser
import datetime
import MySQLdb
import pinboard
import sys
import urllib2


class PinboardToMT:

    def __init__(self, date=None):
        if date is None:
            self.date = datetime.datetime.utcnow().date()
        else:
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
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
                    'db_host',
                    'db_name',
                    'db_user',
                    'db_password',
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
        self.make_blog_post(links)

    def get_pinboard_links(self):
        try:
            p = pinboard.open(token=self.pinboard_api_token)
        except urllib2.HTTPError, error:
            raise PinboardToMTError("Can't connect to Pinboard: %s" % error)
        links = p.posts(date=self.date.strftime('%Y-%m-%d'))
        self.message("Fetched %s link(s) from Pinboard." % len(links))
        return links

    def make_blog_post(self, links):
        html = self.make_html(links)
        title = "Links for %s %s %s" % (self.date.strftime('%A'),
                                        self.date.strftime('%d').lstrip('0'),
                                        self.date.strftime('%B %Y'))
        try:
            db = MySQLdb.connect(host=self.db_host, user=self.db_user,
                                passwd=self.db_password, db=self.db_name)
        except MySQLdb.OperationalError, error:
            raise PinboardToMTError("Problem connecting to database: %s" % error)

        db.set_character_set('utf8')

        cur = db.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')

        try:
            cur.execute("""INSERT INTO mt_entry (entry_blog_id, entry_author_id,
                entry_title, entry_text, entry_created_on, entry_authored_on,
                entry_created_by, entry_status, entry_current_revision)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                    self.mt_blog_id,
                    self.mt_author_id,
                    title,
                    html,
                    datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    self.date.strftime('%Y-%m-%d 23:58:00'),
                    self.mt_author_id,
                    4, # Scheduled
                    0
            ))
        except UnicodeEncodeError, error:
            raise PinboardToMTError("Unicode encoding error: %s" % error)

        self.message("Added Movable Type entry (ID %s)." % db.insert_id())

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

    

