import sys
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
from jinja2 import Environment, FileSystemLoader
import db_operations
import mysql.connector

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="./logs/request_manager.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

configuration = {"user": "root", "password": "snehal", "host": "localhost", "database": "csv_db", "port": 3306}


class RequestHandler(BaseHTTPRequestHandler):
    msg = {}
    filename = ''
    table_name = ''
    update_filter = ''

    def do_GET(self):
        if self.path.endswith('/'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            import os
            template = env.get_template('base.html')
            output = template.render(type='CSV')
            self.wfile.write(output.encode())
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 200))

        if self.path.endswith('/up_load'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            template = env.get_template('upload.html')
            output = template.render()
            self.wfile.write(output.encode())
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 200))

        if self.path.endswith('/message'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            template = env.get_template('message.html')
            output = template.render(send_msg=RequestHandler.msg, table=RequestHandler.table_name)
            self.wfile.write(output.encode())
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 200))
        if self.path.endswith('/sql_error_message'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            template = env.get_template('sql_message.html')
            output = template.render(msg=RequestHandler.msg)
            self.wfile.write(output.encode())
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 200))

        if self.path.endswith('/view_data'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            table_name = RequestHandler.table_name
            # print("table_name :", table_name)
            if not table_name:
                output = "upload table to view !"
                self.wfile.write(output.encode())
            else:

                try:
                    field_names, records, PK_field_list, table_name = db_operations.show_data(table_name, configuration)
                except mysql.connector.errors.ProgrammingError:
                    sys.exit(1)

                RequestHandler.table_name = table_name
                PK_value_list = [record[:3] for record in records]
                template = env.get_template('new_show_data.html')
                pk_data_dict = {}
                pk_data_list = []
                for v in PK_value_list:
                    for i in range(len(v)):
                        data = {PK_field_list[i]: v[i]}
                        pk_data_dict.update(data)
                        new_pk_data_dict = pk_data_dict.copy()
                    pk_data_list.append(new_pk_data_dict)

                list_of_all_dicts = []
                whole_dict = {}
                for i in range(len(records)):
                    whole_dict.update({"value": records[i]})
                    whole_dict.update({"PK_data": pk_data_list[i]})
                    new_dict = whole_dict.copy()
                    list_of_all_dicts.append(new_dict)
                # print(list_of_all_dicts)
                output = template.render(field_list=field_names, list_of_all_dicts=list_of_all_dicts)
                self.wfile.write(output.encode())
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 200))

        if self.path.endswith('/add_record'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            template = env.get_template('add_row_form.html')
            try:
                field_names = db_operations.add(RequestHandler.table_name, configuration)
            except (mysql.connector.errors.ProgrammingError, KeyError):
                sys.exit(1)
            output = template.render(filds=field_names)
            self.wfile.write(output.encode())
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 200))

    def PK_data_2_filter(self, fields):
        PK_field_dict = {}
        for key, value in fields.items():
            PK_field_dict.update({key: value[0]})
        # print("PK_field_dict flat : ", PK_field_dict)

        len_PK_field_dict = len(PK_field_dict)
        filter = ""
        count = 0
        for key, value in PK_field_dict.items():
            count += 1
            if count < len_PK_field_dict:
                filter += f'{key} = "{value}" AND '
            else:
                filter += f'{key} = "{value}" '
        return filter

    def do_POST(self):

        if self.path.endswith('/uploaded_data'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                      'CONTENT_TYPE': self.headers[
                                                                                          'Content-Type'], })

                RequestHandler.filename = form['up_file'].filename
                # print(RequestHandler.filename)
                data = form['up_file'].file.read()
                # print(data)
                if RequestHandler.filename.split(".")[-1] == "csv":
                    with open("csv_file.csv", "wb") as file:
                        file.write(data)
                    filename = RequestHandler.filename
                    try:
                        RequestHandler.table_name = db_operations.create_record(filename, configuration)
                    except (mysql.connector.errors.ProgrammingError, KeyError):
                        sys.exit(1)

                    message = RequestHandler.filename + " uploaded successfully !"
                    RequestHandler.msg = {"message": message, "message_type": "success"}
                    logger.info("%s", RequestHandler.msg["message"])

                else:

                    message = "cannot upload " + RequestHandler.filename + " - select valid CSV file !"
                    RequestHandler.msg = {"message": message, "message_type": "error"}
                    RequestHandler.table_name = None
                    logger.debug("%s", RequestHandler.msg["message"])
                    logger.info("%s", RequestHandler.msg["message"])
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/message')
                self.end_headers()
                logger.info("%s:%s - - [%s] %s -%s" %
                            (self.address_string(), self.server.server_port,
                             self.log_date_time_string(), self.requestline, 301))

        if self.path.endswith('/view_data'):  # '/show_data'
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            # print("ctype :", ctype)
            # print("pdict:", pdict)
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            fields = cgi.parse_multipart(self.rfile, pdict)
            # print("fields:", fields)
            table_name = fields['table'][0]
            try:
                field_names, records, PK_field_list, table_name = db_operations.show_data(table_name, configuration)
            except (mysql.connector.errors.ProgrammingError, KeyError):
                sys.exit(1)
            RequestHandler.table_name = table_name
            PK_value_list = [record[:3] for record in records]
            template = env.get_template('new_show_data.html')
            pk_data_dict = {}
            pk_data_list = []
            for v in PK_value_list:
                for i in range(len(v)):
                    data = {PK_field_list[i]: v[i]}
                    pk_data_dict.update(data)
                    new_pk_data_dict = pk_data_dict.copy()
                pk_data_list.append(new_pk_data_dict)

            list_of_all_dicts = []
            whole_dict = {}
            for i in range(len(records)):
                whole_dict.update({"value": records[i]})
                whole_dict.update({"PK_data": pk_data_list[i]})
                new_dict = whole_dict.copy()
                list_of_all_dicts.append(new_dict)
            # print(list_of_all_dicts)
            output = template.render(field_list=field_names, list_of_all_dicts=list_of_all_dicts)
            self.wfile.write(output.encode())
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 200))

        if self.path.endswith('/delete_record'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            fields = cgi.parse_multipart(self.rfile, pdict)
            filter = self.PK_data_2_filter(fields)
            try:
                db_operations.delete_record(RequestHandler.table_name, filter, configuration)
            except (mysql.connector.errors.ProgrammingError, KeyError):
                sys.exit(1)
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/view_data')
            self.end_headers()
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 301))

        if self.path.endswith('/update_record'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            fields = cgi.parse_multipart(self.rfile, pdict)
            filter = self.PK_data_2_filter(fields)
            PK_field_dict = {}
            for key, value in fields.items():
                PK_field_dict.update({key: value[0]})
            # print("PK_field_dict flat : ", PK_field_dict)
            try:
                record_dict, table_name, filter = db_operations.update_form_fill(RequestHandler.table_name, filter,
                                                                                 configuration)
                RequestHandler.update_filter = filter
            except (mysql.connector.errors.ProgrammingError, KeyError):
                sys.exit(1)
            template = env.get_template('update_form.html')
            output = template.render(record_dict=record_dict, PK_field_dict=PK_field_dict)
            self.wfile.write(output.encode())
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 200))

        if self.path.endswith('/update'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            fields = cgi.parse_multipart(self.rfile, pdict)
            # print("check fields if it has two form data:", fields)
            update_form_data_list = []
            for key, value in fields.items():
                if len(value[0]) == 0 or value[0] == "None":
                    data = f"{key} = NULL"
                else:
                    inv_comma_include_str = ''
                    for c in range(len(value[0])):
                        if value[0][c] == '"':
                            inv_comma_include_str += '""'
                        else:
                            inv_comma_include_str += value[0][c]
                    data = f'{key} = "{inv_comma_include_str}"'
                    # data = f'{key} = "{value[0]}"'
                update_form_data_list.append(data)
            delimiter = ","
            update_SET_str = delimiter.join(map(str, update_form_data_list))
            filter = RequestHandler.update_filter
            try:
                error_msg = db_operations.update(RequestHandler.table_name, update_SET_str, filter, configuration)
                # print(error_msg)
            except KeyError:
                sys.exit(1)

            if error_msg:
                RequestHandler.msg = error_msg
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/sql_error_message')
                self.end_headers()
                logger.info("%s:%s - - [%s] %s -%s" %
                            (self.address_string(), self.server.server_port,
                             self.log_date_time_string(), self.requestline, 301))
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/view_data')
            self.end_headers()
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 301))

        if self.path.endswith('/add'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            fields = cgi.parse_multipart(self.rfile, pdict)
            # print("fields from add row form : ", fields)
            try:
                error_msg = db_operations.add(RequestHandler.table_name, configuration, fields)
            except KeyError:
                sys.exit(1)
            if error_msg:
                RequestHandler.msg = error_msg
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/sql_error_message')
                self.end_headers()
                logger.info("%s:%s - - [%s] %s -%s" %
                            (self.address_string(), self.server.server_port,
                             self.log_date_time_string(), self.requestline, 301))

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/view_data')
            self.end_headers()
            logger.info("%s:%s - - [%s] %s -%s" %
                        (self.address_string(), self.server.server_port,
                         self.log_date_time_string(), self.requestline, 301))


def main():
    PORT = 8000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, RequestHandler)
    print("server running on port", PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
