# School Management System
The project is intended to develop into full scale school management system. It will digitalized all the activities in school system, aim at reduce of manual labour and make record easy to access.
## Technology
- SQLAlchemy ORM
- Python
- MySQL

### Python Packages
- SQLAlchemy
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

This will drop the `school_db` and `test_db` if exist

    cat setups/db_setup.sql | mysql -uroot -p

***Create tables in the school_db database***

    DATABASE=school_db python manage.py

***Create two teacher with admin privileges***

    DATABASE=school_db python -m setups.admin

All the above steps can be achieve wtih a sign command

    DATABASE=school_db python -m setups.initializedb


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
- Moses Solomon Ayofemi <solomonayofemi@gmail.com>
