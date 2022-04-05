# db_operations

##This module is used to add local csv file to database and perform crud operations on it.

## Dependencies
- ### ntpath
- ###  mysql.connector
- ### pandas  

## Quick Start

### Upload csv to database 
Create tablename in database in configure and add csv extracted data to database.           
:param filename: filename or absolute path of csv file to read.                                 
:param configure: Configuration of database with database name.                             
:param internal_csv_file: if method is called from outside app value is False ex. for testing.                                                               
:return: table name in which csv data is added.                                                                 
```python
from db_operations import create_record
table_name = create_record(file_path_fake_csv, configuration, Internal_csv_file=False) # Internal_csv_file=False 
```

### Delete Record
Delete record from the database for filter condition    
:param table_name: from row to delete         
:param filter_condn: condition at which row be delete    
:param configure: database configuration              
:return: tablename from which record is deleted
```python
from db_operations import delete_record
delete_record(tablename, filter_condn, configuration)
```
 