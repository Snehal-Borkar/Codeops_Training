from db_operations import create_record, add, show_data, update, delete_record, connect_db
import unittest
import logging
import pandas as pd
from pandas import read_csv
import mysql.connector
import os

LOG_FORMAT = " %(lineno)d %(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="../logs/csv_app_unit.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

configuration = {"user": "root", "password": "snehal", "host": "localhost", "database": "test_db", "port": 3306}
global TABLE_NAME
TABLE_NAME = "fakestoreapi"
class TestUnitDbOperations(unittest.TestCase):
    TestUnit_tablename = ""


    def test_adding_csv_in_db_successful(self):
        """
        Checks if csv data to database is successfully added by callling create_record() method
        from csv uploader app db_operations module, it takes three arguments- file_name or absolute file path ,
        database config and Internal_csv_file:bool value False if calling method from outside app.

        create_record() returns table name in which csv data is uploaded, which is further utilized to perform
        CRUD operations test.

        Test is performed by comparing database table dataframe and csv dataframe
        """

        file_path_fake_csv = (os.path.dirname(__file__)) + "/fakestoreapi.csv"

        table_name = create_record(file_path_fake_csv, configuration, Internal_csv_file=False)
        logger.debug("successfully created table %s",table_name)
        TestUnitDbOperations.TestUnit_tablename = table_name
        connection = connect_db(configuration)

        db_dataframe = pd.read_sql(f'SELECT * FROM {table_name}', con=connection)
        csv_dataframe = read_csv(file_path_fake_csv, keep_default_na=False)

        self.assertEqual(csv_dataframe.to_dict(), db_dataframe.to_dict())  # compare if dataframe contents are equal




    def test_read_database_table_successful(self):
        """
        Checks if read operation of the Database Table is successful mainly by comparing fetched
        RECORDS from database table and records returned by show_data() method
        """
        column_names, records, PK_columns_list, table_name = show_data(TestUnitDbOperations.TestUnit_tablename, configuration)
        logger.debug("successfully shown data of table %s",table_name)
        self.assertEqual(table_name, TestUnitDbOperations.TestUnit_tablename)  # compare read operation table name and csv added tablename
        logger.debug("%s from test_read_database_table_successful",TestUnitDbOperations.TestUnit_tablename)
        self.assertIsNotNone(column_names)  # checks if column names list is not none
        self.assertIsNotNone(PK_columns_list)  # checks if Primary key column names list is not none

        connection = connect_db(configuration)
        sql = f"SELECT * FROM {table_name}"
        my_cursor = connection.cursor()
        my_cursor.execute(sql)
        RECORDS = my_cursor.fetchall()  # records to compare with returned records from show_data() method

        self.assertEqual(records, RECORDS)  # compare records in database and records from show_data() method

    def test_read_from_db_unsuccessful(self):
        """ Checks if Read operation of the Database Table is unsuccessful """

        wrong_config = {"user": "root", "password": "snehal", "host": "localhost", "database": "test_d", "port": 3306}

        with self.assertRaises(mysql.connector.ProgrammingError):
            show_data(TestUnitDbOperations.TestUnit_tablename, wrong_config)

        INCORRECT_TABLE_NAME = "incorrect_table"
        with self.assertRaises(mysql.connector.ProgrammingError):
            show_data(INCORRECT_TABLE_NAME, configuration)
    def test_delete_row_in_db_successful(self):
        """ Checks if delete row operation in Database Table is Successful"""

        filter_condn = 'id = 1 AND title = "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops" AND price = 109.95 '
        # filter = 'id = 3'
        connection = connect_db(configuration)
        sql = f"SELECT * FROM {TestUnitDbOperations.TestUnit_tablename} WHERE {filter_condn}"
        my_cursor = connection.cursor()
        my_cursor.execute(sql)
        record_pre_delete = my_cursor.fetchall()

        table_name_ = delete_record(TestUnitDbOperations.TestUnit_tablename, filter_condn, configuration)
        self.assertEqual(table_name_, TestUnitDbOperations.TestUnit_tablename)

        connection = connect_db(configuration)
        sql = f"SELECT * FROM {TestUnitDbOperations.TestUnit_tablename} WHERE {filter_condn}"
        my_cursor = connection.cursor()
        my_cursor.execute(sql)
        record_post_delete = my_cursor.fetchall()
        self.assertNotEqual(record_pre_delete, record_post_delete)
        logger.debug("Delete row from table %s  with condition %s successfull ",TestUnitDbOperations.TestUnit_tablename,filter_condn)

    def test_delete_row_in_db_unsuccessful(self):
        """ Check if deleting rows in database is successful """
        wrong_config = {"user": "root", "password": "snehal", "host": "localhost", "database": "test_d", "port": 3306}
        filter_condn = 'id = 1'
        with self.assertRaises(mysql.connector.ProgrammingError):
            delete_record(TestUnitDbOperations.TestUnit_tablename, filter_condn, wrong_config)

        INCORRECT_TABLE_NAME = "incorrect_table"
        with self.assertRaises(mysql.connector.ProgrammingError):
            delete_record(INCORRECT_TABLE_NAME, filter_condn, configuration)

    def test_update_row_in_db_successful(self):
        """ Checks if Update operation for the Database Table is successful """

        filter_condn = "id = 10"
        sql = f"SELECT * FROM {TestUnitDbOperations.TestUnit_tablename} WHERE {filter_condn}"
        connection = connect_db(configuration)
        my_cursor = connection.cursor()
        my_cursor.execute(sql)
        record_pre_update = my_cursor.fetchall()

        update_SET = "price = 600"
        update(TestUnitDbOperations.TestUnit_tablename, update_SET, filter_condn, configuration)

        sql = f"SELECT * FROM {TestUnitDbOperations.TestUnit_tablename} WHERE {filter_condn}"
        connection = connect_db(configuration)
        my_cursor = connection.cursor()
        my_cursor.execute(sql)
        record_post_update = my_cursor.fetchall()
        self.assertNotEqual(record_pre_update, record_post_update)
        logger.debug("test_update_row_in_db_successful TestUnitDbOperations.TestUnit_tablename %s",
                     TestUnitDbOperations.TestUnit_tablename)



    def test_add_new_row_successful(self):
        """
        checks if new row added to database successfull.
        first three fields for any table with min'm 3 fields are considered as primary key therefore cannot be null
        """

        fields_1 = {'id': ['22'], 'title': ['Title of new row'], 'price': ['300'], 'description': [''],
                    'category': [''], 'image': [''], 'rating_rate': [''], 'rating_count': ['']}
        check_field_value1 = (22, "Title of new row", 300, None, None, None, None, None)
        sql_filter1 = 'id=22 AND title="Title of new row" AND price=300'

        fields_2 = {'id': ['23'], 'title': ['Title of new'], 'price': ['200'], 'description': [''],
                    'category': ['mens"s wear'], 'image': ['url'], 'rating_rate': ['5.1'], 'rating_count': ['30']}
        check_field_value2 = (23, 'Title of new', 200, None, 'mens"s wear', 'url', 5.1, 30)
        sql_filter2 = 'id=23 AND title="Title of new" AND price=200'

        add(TABLE_NAME, configuration, fields_1)
        logger.debug("%s", TABLE_NAME)
        sql = f'SELECT * FROM {TABLE_NAME} WHERE {sql_filter1}'
        connection = connect_db(configuration)
        my_cursor = connection.cursor()
        my_cursor.execute(sql)
        record_1 = my_cursor.fetchall()
        self.assertEqual(record_1[0], check_field_value1)  # compare record for condition added to database with
        # values-check_field_value1 to be added

        add(TABLE_NAME, configuration, fields_2)
        sql = f'SELECT * FROM {TABLE_NAME} WHERE {sql_filter2}'
        connection = connect_db(configuration)
        my_cursor = connection.cursor()
        my_cursor.execute(sql)
        record_2 = my_cursor.fetchall()
        self.assertEqual(record_2[0], check_field_value2)  # compare record for condition added to database with
        # values-check_field_value2 to be added

    def test_add_new_row_unsuccessfull(self):
        """
        checks if new row added to database is unsuccessfull
        first three fields for any table with min'm 3 fields are considered as primary key therefore cannot be null
        """

        def records():
            sql = f'SELECT * FROM {TABLE_NAME}'
            connection = connect_db(configuration)
            my_cursor = connection.cursor()
            my_cursor.execute(sql)
            record = my_cursor.fetchall()
            return record

        fields_1 = {'id': [''], 'title': [''], 'price': [''], 'description': ['my_description'],
                    'category': ['cate'], 'image': [''], 'rating_rate': ['3.2'], 'rating_count': ['500']}
        records_pre_add = records()
        add(TABLE_NAME, configuration, fields_1)
        records_post_add = records()
        self.assertEqual(records_pre_add, records_post_add)

        fields_2 = {'id': [''], 'title': ['This is title'], 'price': [''], 'description': ['my_description'],
                    'category': ['cate'], 'image': [''], 'rating_rate': ['3.2'], 'rating_count': ['500']}
        records_pre_add = records()
        add(TABLE_NAME, configuration, fields_2)
        records_post_add = records()
        self.assertEqual(records_pre_add, records_post_add)

        fields_2 = {'id': ['20'], 'title': [''], 'price': [''], 'description': ['my_description'],
                    'category': ['cate'], 'image': [''], 'rating_rate': ['3.2'], 'rating_count': ['500']}
        records_pre_add = records()
        add(TABLE_NAME, configuration, fields_2)
        records_post_add = records()
        self.assertEqual(records_pre_add, records_post_add)


if __name__ == "__main__":
    unittest.main()
