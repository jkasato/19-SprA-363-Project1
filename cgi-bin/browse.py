#!/usr/bin/env python3

import mysql.connector
import cgi
import cgitb
from os import environ
from pathlib import Path
import re

PASSWORD = Path('password').read_text()


class BaseCGI(object):
    def __init__(self, template_path):
        cgitb.enable()
        self.connection = None
        self.headers = ["Content-Type: text/html"]
        self.html = Path('app.html').read_text()
        self.template = Path(template_path).read_text()
        self.results = {}
        self.error = None

        try:
            # parse the request -- todo (move generic logic here)

            # connect to database
            self.connection = mysql.connector.connect(user='root',
                                                      password=PASSWORD,
                                                      database='serious_project_1',
                                                      host='127.0.0.1')
            # do the work
            self._run()
        except mysql.connector.Error as error:
            self.error = "Error -- %s" % error
        finally:
            self.connection.close()
            self.respond()

    def _run(self):
        raise NotImplementedError

    def respond(self):
        for header in self.headers:
            print(header)
        print()  # blank line required, end of headers
        if not self.error:
            # replace placeholder in template with content
            for key in self.results:
                self.template = re.sub(r'\${' + key + '}', self.results[key], self.template)
            # replace placeholder in html with template
            result = self.html.replace('<!--${results}-->', self.template)
        else:
            result = self.html.replace('<!--${error}-->', "<strong>" + self.error + "</strong><br/><hr/>")
        print(result)

    def add_result(self, key, value):
        self.results[key] = value

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

    def query_get_all(self, query):
        c = self.connection.cursor()
        c.execute(query)
        return c.fetchall()

    def query_committed(self, query):
        c = self.connection.cursor()
        c.execute(query)
        self.connection.commit()

    @staticmethod
    def table_from_tuples(tuples_list):
        table_template = Path('./html-templates/table.html').read_text()

        # first tuple is the header
        header = tuples_list.pop(0)
        items = ''
        for item in header:
            items += '<th>' + item + '</th>'
        table_template = re.sub(r'\${head}', '<tr>' + items + '</tr>', table_template)

        # subsequent tuples are the data
        data_rows = ''
        for row in tuples_list:
            items = ''
            for item in row:
                items += '<td>' + str(item) + '</td>'
            data_rows += '<tr>' + items + '</tr>'

        table_template = re.sub(r'\${body}', data_rows, table_template)

        return table_template

    @staticmethod
    def table_from_list(data_list):
        table_template = Path('./html-templates/table.html').read_text()

        # first item is the header
        header = data_list.pop(0)
        table_template = re.sub(r'\${head}', '<tr><th>' + header + '</th></tr>', table_template)

        # subsequent items are the data
        data_rows = ''
        for row in data_list:
            items = ''
            data_rows += '<tr><td>' + str(row[0]) + '</td></tr>'  # fix -- hacky since query returns incomplete tuples

        table_template = re.sub(r'\${body}', data_rows, table_template)
        return table_template


class Browse(BaseCGI):
    q_inventory = '''
        SELECT i.name, need, have
        FROM inventory v
        JOIN item i ON v.item_id = i.id
        ORDER BY i.name;
        '''

    q_supplier = '''
        SELECT name, address, phone
        FROM supplier
        ORDER BY name;
        '''

    q_catalog = '''
        SELECT i.name, s.name, price, discontinued
        FROM catalog c
        JOIN item i ON c.item_id = i.id
        JOIN supplier s ON c.supplier_id = s.id
        ORDER BY i.name, discontinued, price, s.name;
        '''

    def __init__(self):
        super().__init__('./html-templates/browse.html')

    def _run(self):
        form = cgi.FieldStorage()
        target = None
        query_result = None

        if 'inventory' in form:
            target = "Browsing the Inventory"
            query_result = [('name', 'need', 'have')]
            query_result.extend(self.query_get_all(self.q_inventory))
        elif 'suppliers' in form:
            target = "Browsing the Suppliers"
            query_result = [('name', 'address', 'phone')]
            query_result.extend(self.query_get_all(self.q_supplier))
        elif 'catalog' in form:
            target = "Browsing the Catalog"
            query_result = [('item', 'supplier', 'price', 'discontinued')]
            query_result.extend(self.query_get_all(self.q_catalog))
        else:
            self.error = "ERROR -- UNAUTHORIZED REQUEST"
            return

        self.add_result('target', target)
        table = self.table_from_tuples(query_result)
        self.add_result('table', table)


Browse()
