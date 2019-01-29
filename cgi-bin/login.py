#!/usr/bin/env python3

import mysql.connector
import cgi
import cgitb
from os import environ
from pathlib import Path

PASSWORD = Path('password').read_text()


# note: this one is different from the others
class BaseCGI(object):
    def __init__(self, title):
        cgitb.enable()
        self.connection = None
        self.headers = ["Content-Type: text/html"]
        self.body = ["<TITLE>%s</TITLE>" % title]

        try:
            # parse the request -- todo (move generic logic here)

            # connect to database
            self.connection = mysql.connector.connect(user='root',
                                                      password=PASSWORD,
                                                      database='cst363',
                                                      host='127.0.0.1')
            # do the work
            self._run()
        except mysql.connector.Error as error:
            self.add_tag("Error -- %s" % error)
        finally:
            self.respond()
            self.connection.close()

    def _run(self):
        raise NotImplementedError

    def respond(self):
        for header in self.headers:
            print(header)
        print()  # blank line required, end of headers
        for tag in self.body:
            print(tag)

    def add_tag(self, message):
        self.body.append("<p>%s</p><br/>" % message)

    @staticmethod
    def get_cookies():
        if 'HTTP_COOKIE' in environ:
            return environ['HTTP_COOKIE'].split(';')
        else:
            return dict()

    def add_cookie_to_header(self, key, value):
        self.headers.append("Set-Cookie: %s=%s" % (key, value))

    def query_get_first(self, query):
        c = self.connection.cursor()
        c.execute(query)
        return c.fetchone()

    def query_committed(self, query):
        c = self.connection.cursor()
        c.execute(query)
        self.connection.commit()


class Login(BaseCGI):
    q_is_registered = 'select visits from login where userid = "%s"'
    q_valid_login = 'select visits from login where userid = "%s" and password = "%s"'
    q_insert_user = 'insert into login (userid, password, visits) values ("%s", "%s", "1")'
    q_update_user = 'update login set visits = visits + 1 where userid = "%s" and password = "%s"'

    def __init__(self):
        super().__init__("CST363 SERIOUS BUSINESS project 1")

    def _run(self):
        form = cgi.FieldStorage()

        for cookie in self.get_cookies():
            self.add_tag(str(cookie))

        # retrieve input values
        userid = form["userid"].value
        self.add_cookie_to_header("user", userid)
        password = form["password"].value

        if 'register' in form:
            self.register_user(userid, password)
        elif 'login' in form:
            self.login_user(userid, password)
        else:
            self.add_tag("ERROR -- not register or login")

    def register_user(self, userid, password):
        # does user already exist?
        user_visits = self.query_get_first(self.q_is_registered % userid)

        if user_visits is not None:
            # yes -> ask for different name
            self.add_tag("Sorry, the username: '%s' is already in use." % userid)
        else:
            # no -> add new user, thank them
            self.query_committed(self.q_insert_user % (userid, password))
            self.add_tag("Thank you for registering, %s." % userid)
        # self.add_cookie_to_header(userid, password)

    def login_user(self, userid, password):
        # is username & password valid?
        user_visits = self.query_get_first(self.q_valid_login % (userid, password))

        if user_visits is None:
            # no -> incorrect
            self.add_tag("Sorry, either the provided username or password was not correct")
        else:
            # yes -> thank them, show visit count
            visits = user_visits[0] + 1
            self.query_committed(self.q_update_user % (userid, password))
            self.add_tag("Thank you for visiting again, %s. This is visit number %s." % (userid, str(visits)))


Login()
