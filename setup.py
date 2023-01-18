import mysql.connector
from mysql.connector import errorcode
from database import cursor


DB_NAME = 'log'

TABLES = {}

TABLES['logs'] = (
    "CREATE TABLE `logs` ("
    " `id` int(11) NOT NULL AUTO_INCREMENT,"
    " `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    " `level` varchar(25) NOT NULL,"
    " `ip` varchar(25) NOT NULL,"
    " `result` varchar(10) NOT NULL,"
    " `event` varchar(250) NOT NULL,"
    " PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    print("Datebase {} created!".format(DB_NAME))

def create_tables():
    cursor.execute("USE {}".format(DB_NAME))

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table ({}) ".format(table_name), end="")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Already Exists")
            else:
                print(err.msg)


create_database()
create_tables()