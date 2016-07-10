# coding: utf-8
import configparser
import smtplib
import email
import datetime
import feedparser


class feednotifier:
    def __init__(self, text):
        print("Init" + text)

    def sendemail(student_email, student_name, mentor_email, mentor_name,
                  org_name, date):
        # mail = open(email, 'r')
        # msg = email.mime.text.MIMEText(mail.read())
        # mail.close()
        app_config = configparser.ConfigParser()
        app_config.read('config/app_config.ini')
        email_host = app_config.get('DEFAULT', 'email_host')
        email_user = app_config.get('DEFAULT', 'email_user')
        email_pass = app_config.get('DEFAULT', 'email_pass')
        msg = email.mime.text.MIMEText()
        orgs_config = configparser.ConfigParser()
        orgs_config.read('config/orgs.ini')
        admin_email = orgs_config.get('DEFAULT', 'owner_email')
        to_emails = [student_email, mentor_email, admin_email]
        msg['To'] = ", ".join(to_emails)
        msg['From'] = email_user
        msg['Subject'] = ('Notification regarding blog inactivity of ' +
                          student_name + '<' + student_email + '> (' +
                          org_name + ')')
        # TODO: Should we read the message from the app config file?
        blogs_config = configparser.ConfigParser()
        blogs_config.read('config/blogs.ini')
        activity_threshold = blogs_config.get('DEFAULT', 'activity_threshold')
        msg_body = ('This mail is to notify that the GSOC participant ' +
                    student_name + ' <' + student_email + '>' +
                    ' for the organisation ' + org_name +
                    ' under the mentor ' + mentor_name + ' <' + mentor_email +
                    '> has not updated their blog since ' +
                    activity_threshold +
                    ' days. We request you to continue writing blog posts.')
        msg.attach(email.mime.text.MIMEText(msg_body, _subtype='plain',
                   _charset='UTF-8'))
        server = smtplib.SMTP(email_host)
        server.ehlo()
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(email_user, to_emails, msg.as_string())
        server.quit()


def main():
    blogs_config = configparser.ConfigParser()
    blogs_config.read('config/blogs.ini')
    for blog in blogs_config.sections():
        blog_feed = feedparser.parse(blog)
        print(blog_feed.feed.title)

        # TODO: Any better way than this stupid try catch stuff?
        try:
            try:
                date = blog_feed.feed.published
            except:
                date = blog_feed.entries[0].updated
        except:
            date = blog_feed.entires[0].published

        # Get the number of days before we consider a blog to be inactive.
        threshold_days = blogs_config.get('DEFAULT', 'activity_threshold')
        today_date = datetime.datetime.now()
        # TODO: Is it okay to assume that the threshold_days will never be more
        # than a month?
        expiry_delta = datetime.timedelta(days=int(threshold_days))
        expiry_date = today_date - expiry_delta
        blog_date = datetime.datetime.strptime(date,
                                               "%a, %d %b %Y %I:%M:%S %Z")

        # If the post is older than when we expect a new one, send out emails.
        if blog_date < expiry_date:
            # Read the mentor info from orgs.ini
            # TODO: Should orgs.ini be generated from blogs.ini or be created
            # by the application admin?
            orgs_config = configparser.ConfigParser()
            orgs_config.read('config/orgs.ini')
            # Find corresponding org from orgs.ini
            for org in orgs_config.sections():
                if blogs_config.get(blog, 'org') == org:
                    # TODO: Possibility of multiple mentors?
                    mentor_email = orgs_config.get(org, 'mentor_email')
                    mentor_name = orgs_config.get(org, 'mentor_name')
                    org_name = org

            student_email = blogs_config.get(blog, 'owner_email')
            student_name = blogs_config.get(blog, 'owner_name')
            # Call a function with the student email, mentor email and date
            # when the last post was done.
            f = feednotifier('Hola')
            f.sendemail(student_email, student_name, mentor_email,
                        mentor_name, org_name, date)
            # TODO: Do we need a log file to track these events?

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
