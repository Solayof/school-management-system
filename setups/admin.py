
from os import getenv
from models.cbt.examination import Examination
from models.cbt.question import Question
from models.cbt.response import Response
from models.cbt.score import Score
from models.portal.admin import Admin
from models.portal.admission import Admission
from models.portal.course import Course
from models.portal.Class import Class
from models.portal.parent import Parent
from models.portal.session import Session
from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.teacher import Teacher
from models.portal.user import User
from faker import Faker
import random


BLUE ="\033[34m"
GREEN = "\033[32m"
RESET = "\033[0m"
database = getenv("DATABASE", "school_db")

fake = Faker()

def creatadmin():
    teacher = Teacher(
        username="superadmin",
        email="superadmin@school.com",
        firstName=fake.first_name(),
        middleName=fake.first_name(),
        lastName=fake.last_name()
      )
    teacher.password = "superadmin"
    teacher.save()
    superadmin = Admin(teacher_id=teacher.id)
    superadmin.privileges = {
                "create": True,
                "delete": True,
                "update": True,
                "superadmin": True
            }

    superadmin.save()

    teacher = Teacher(
        username="admin",
        email="admin@school.com",
        firstName=fake.first_name(),
        middleName=fake.first_name(),
        lastName=fake.last_name()
      )
    teacher.password = "admin"
    teacher.save()
    admin = Admin(teacher_id=teacher.id)
    admin.privileges = {
                "create": True,
                "delete": True,
                "update": True,
                "superadmin": False
    }


    teacher = Teacher(
        username="create",
        email="create@school.com",
        firstName=fake.first_name(),
        middleName=fake.first_name(),
        lastName=fake.last_name()
      )
    teacher.password = "create"
    teacher.save()
    admin = Admin(teacher_id=teacher.id)
    admin.privileges = {
                "create": True,
                "delete": False,
                "update": False,
                "superadmin": False
      }
    admin.save()

    print(GREEN + 
          f"--{Admin.query.count()} USERS CREATED IN {database.upper()}--" + RESET)

    print(GREEN + "ADNIN 1 LOGIN DETAILS" + RESET)
    print(GREEN + "\t\tEmail: superadmin@school.com\n\t\tPassword: superadmin" + RESET)

    print(GREEN + "ADNIN 2 LOGIN DETAILS" + RESET)
    print(GREEN + "\t\tEmail: create@school.com\n\t\tPassword: create" + RESET)
