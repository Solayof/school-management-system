from MySQLdb import Connection, Error
from os import getenv
import subprocess
from setups.admin import creatadmin


BLUE ="\033[34m"
GREEN = "\033[32m"
RESET = "\033[0m"


username = "root"
password = "Arisekola77#" #Arisekola.77#
hostname = "localhost"
database = getenv("DATABASE", "school_db")
print(GREEN + 
      "--CONNECTING DATABASE--" + RESET)
conn = Connection(
    host=hostname,
    password=password,
    database=database,
    user=username
)
if not conn:
    print(True)
coursor = conn.cursor()
with open('setups/db_setup.sql', 'r') as file:
    sql_queries = file.read().split(';')

print(GREEN + 
      "--RESETTING DATABASE--" + RESET)
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
print(GREEN + 
      f"--CREATING TABLES IN {database.upper()}--" + RESET)
#subprocess.run(["python", "manage.py"], capture_output=True, text=True)
print(GREEN + 
      f"--CREATING ADMIN USERS IN {database.upper()}--" + RESET)
creatadmin()


print(GREEN + 
      f"--{database.upper()} INITIALIZE SUCCESSFULLY--" + RESET)
