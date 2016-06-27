# coding: utf-8
import configparser
import feedparser

config = configparser.ConfigParser()
config.read('blogs.ini')
for blog in config.sections():
    d = feedparser.parse(blog)
    print(d.feed.title)
    try:
        try:
            date = d.feed.published
        except:
            date = d.entries[0].updated
    except:
        date = d.entires[0].published
    print(config.get(blog, 'name') + ': ' + date)
