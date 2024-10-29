# School Management System
The project is intended to develop into full scale school management system. It will digitalized all the activities in school system, aim at reduce of manual labour and make record easy to access.
## Technology
- SQLAlchemy ORM
- Python
- MySQL
- Faker
- Flask
- Flask-login
- Flask-CORS
- Flassger
- Hashlib
# Setup
***Install the dependency***

    pip install -r requirements.txt
***Create database and user***
this will drop the `school_db` and `test_db` if exist

    cat setups/db_setup.sql | mysql -uroot -p

***Create tables in the school_db database***

    DATABASE=school_db python manage.py

***Create two teacher with admin privileges***

    DATABASE=school_db python -m setups.admin

## Development Stage
### Setup

***Create tables in the test_db database***

    DATABASE=test_db python manage.py
***Populate the test_db tables with fake data***

    DATABASE=test_db python -m setups.scripts

# API


## Production Stage
the project is still in Development Stage

## Author
- Moses Solomon Ayofemi <solomonsyofemi@gmail.com>
