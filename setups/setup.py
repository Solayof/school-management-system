#/usr/bin/python3
import subprocess

#subprocess.run(["cd setups"], capture_output=True, text=True)
subprocess.run("cat setups/db_setup.sql | mariadb -uroot -proot", shell=True, capture_output=True, text=True)
subprocess.run(["python", "manage.py"], capture_output=True, text=True)
