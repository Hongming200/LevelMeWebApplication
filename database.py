import mysql.connector

config = {
    'user' : 'root',
    'password' : 'MySQL123!',
    'host' : 'localhost',
    'database' : 'log'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
