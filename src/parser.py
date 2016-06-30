# coding: utf-8
import configparser
import feedparser
import smtplib
import datetime

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
    # Get the activity_threshold.
    expiry_days = config.get('DEFAULT', 'activity_threshold')
    today_date = datetime.datetime.now()
    # TODO: Is it okay to assume that the expiry_days will never be more than a month?
    expiry_delta = datetime.timedelta(days=expiry_days)
    # The date when the last post should have been done.
    expired_date = today_date - expiry_delta
    blog_date = datetime.datetime.strptime(date, "%a, %d %b %Y %I:%M:%S %Z")
    # If the post is older than when we expected a new one send out emails.
    if blog_date < expired_date:
        # Call a function with the student email, mentor email and date when the last post was done.
        sendmail(config.get(blog, 'owner_email'), config.get(blog, 'mentor_email'), date)
        # TODO: Do we need a log file to track these events?
    else:
        # TODO: Do we also need to track good students? (Doesn't make sense at all, left here just in case)