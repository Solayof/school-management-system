from MySQLdb import Connection, Error
from os import getenv
import subprocess


username = "root"
password = "Arisekola.77#"
hostname = "localhost"
database = getenv("DATABASE", "school_db")

conn = Connection(
    host=hostname,
    password=password,
    database=database,
    user=username
)

coursor = conn.cursor()
with open('setups/db_setup.sql', 'r') as file:
    sql_queries = file.read().split(';')

for sql_query in sql_queries:
    sql_query = sql_query.strip()
    if sql_query:
        coursor.execute(sql_query)
try:
    conn.commit()
except Error as e:
    print("An error occurred:", e)
finally:
    if conn:
        coursor.close()
        conn.close()

subprocess.run(["python3", "manage.py"], capture_output=True, text=True)
