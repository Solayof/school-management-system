#/usr/bin/python3
import subprocess


subprocess.run("cat setups/db_setup.sql | mariadb -uroot -proot", shell=True, capture_output=True, text=True)
subprocess.run(["python3", "manage.py"], capture_output=True, text=True)
subprocess.run(["python3", "-m", "setups.scripts"], capture_output=True, text=True)
