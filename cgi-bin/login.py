#!/usr/bin/env python3

import mysql.connector
import cgi
import cgitb


class Login(object):
    q_is_registered = 'select visits from login where userid = "%s"'
    q_valid_login = 'select visits from login where userid = "%s" and password = "%s"'
    q_insert_user = 'insert into login (userid, password, visits) values ("%s", "%s", "1")'
    q_update_user = 'update login set visits = visits + 1 where userid = "%s" and password = "%s"'

    def __init__(self, pw):
        cgitb.enable()
        self.connection = None
        try:
            # connect to database
            self.connection = mysql.connector.connect(user='root',
                                                      password=pw,
                                                      database='cst363',
                                                      host='127.0.0.1')
            # do the work
            self.run()
        except mysql.connector.Error as error:
            self.print_header()
            self.print_message("Error -- %s" % error)
            self.connection.close()
            raise error
        finally:
            self.connection.close()

    @staticmethod
    def print_header():
        print("Content-Type: text/html")  # HTML is following
        print()  # ------------------------ blank line required, end of headers
        print("<TITLE>CST363 homework 1</TITLE>")

    @staticmethod
    def print_message(message):
        print("<p>%s</p><br/>" % message)

    def query_get_first(self, query):
        c = self.connection.cursor()
        c.execute(query)
        return c.fetchone()

    def query_committed(self, query):
        c = self.connection.cursor()
        c.execute(query)
        self.connection.commit()

    def run(self):
        self.print_header()

        form = cgi.FieldStorage()

        # retrieve input values
        userid = form["userid"].value
        password = form["password"].value

        if 'register' in form:
            self.register_user(userid, password)
        elif 'login' in form:
            self.login_user(userid, password)
        else:
            self.print_message("ERROR -- not register or login")

    def register_user(self, userid, password):
        # does user already exist?
        user_visits = self.query_get_first(self.q_is_registered % userid)

        if user_visits is not None:
            # yes -> ask for different name
            self.print_message("Sorry, the username: '%s' is already in use." % userid)
        else:
            # no -> add new user, thank them
            self.query_committed(self.q_insert_user % (userid, password))
            self.print_message("Thank you for registering, %s." % userid)

    def login_user(self, userid, password):
        # is username & password valid?
        user_visits = self.query_get_first(self.q_valid_login % (userid, password))

        if user_visits is None:
            # no -> incorrect
            self.print_message("Sorry, either the provided username or password was not correct")
        else:
            # yes -> thank them, show visit count
            visits = user_visits[0] + 1
            self.query_committed(self.q_update_user % (userid, password))
            self.print_message("Thank you for visiting again, %s. This is visit number %s." % (userid, str(visits)))


Login('password')
