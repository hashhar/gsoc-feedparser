# coding: utf-8
import configparser
import feedparser

config = configparser.ConfigParser()
config.read('blogs.ini')
for blog in config.sections():
    d = feedparser.parse(blog)
    print(config.get(blog, 'name') + ': ' + d.entries[0].published)
