# School Management System
The project is intended to develop into full scale school management system. It will digitalized all the activities in schoo system, aim at reduce of manual labour and make record easy to access. 
## Technology
- SQLAlchemy ORM
- Python
- MySQL
- Flask
- Flask-login
- Flask-CORS
- Swagger UI
- Flassger
- Hashlib
## Development Stage
### Setup
***Install the dependency***

    pip install -r requirements.txt
***Create database and user***
this will drop the `school_db` and `test_db` if exist

    cat setups/db_setup.sql | mysql -uroot -p

***Create tables in the school_db database***

    DATABASE=school_db python manage.py

***Create tables in the test_db database***

    DATABASE=test_db python manage.py
## Production Stage
the project is still in Development Stage

## Author
- Moses Solomon Ayofemi <solomonsyofemi@gmail.com>
