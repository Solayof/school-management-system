#!/usr/bin/python3

from os import getenv
from models.cbt.examination import Examination
from models.cbt.option import Option
from models.cbt.question import Question
from models.cbt.response import Response
from models.cbt.score import Score
from models.portal.admin import Admin
from models.portal.admission import Admission
from models.portal.Class import Class
from models.portal.course import Course
from models.portal.department import Department
from models.portal.parent import Parent
from models.portal.session import Session
from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.teacher import Teacher
from models.portal.user import User
from faker import Faker
import random

fake = Faker()

BLUE ="\033[34m"
GREEN = "\033[32m"
RESET = "\033[0m"
database = getenv("DATABASE", "school_db")

arms = ["A", "B", "C", "D"]
science = Department(name="Science")
science.save()
art = Department(name="Art")
art.save()
commercial = Department(name="Commercial")
commercial.save()

departments = Department.query.all()

for i in range(200):
  parent = Parent(
      username=fake.unique.user_name(),
      email=fake.unique.email(),
      firstName=fake.first_name(),
      middleName=fake.first_name(),
      lastName=fake.last_name()
      
    )
  parent.save()
  
print(GREEN + 
      f"--{Parent.query.count()} PARENTS CREATED--" + RESET)

for i in range(1, 4):
  cla = Class(className=f"jss {i}")
  cla.save()
for i in range(1, 4):
  cla = Class(className=f"sss {i}")
  cla.save()
print(GREEN + 
      f"--{Class.query.count()} CLASSES CREATED--" + RESET)
classes = Class.query.all()
for i in range(30):
  teacher = Teacher(
    username=fake.unique.user_name(),
      email=fake.unique.email(),
    firstName=fake.first_name(),
    middleName=fake.first_name(),
    form_class_id=random.choice(classes).id,
    lastName=fake.last_name()
  )
  teacher.save()
print(GREEN + 
      f"--{Teacher.query.count()} TEACHERS CREATED--" + RESET)
parents = Parent.query.all()
for i in range(500):
  student = Student(
      lastName=fake.last_name(),
      classroom_id=random.choice(classes).id,
      arm=random.choice(arms),
      admission_no=fake.unique.numerify(),
      username=fake.unique.user_name(),
      email=fake.unique.email(),
      firstName=fake.first_name(),
      middleName=fake.first_name(),
      parent_id=random.choice(parents).id
      )
  student.save()

print(GREEN + 
      f"--{Student.query.count()} STUDENTS CREATED--" + RESET)

print(GREEN + 
      f"--{database.upper()} SUCCESSFULLY POPULATED--" + RESET)  

# def creatadmin():
#     teacher = Teacher(
#         username="superadmin",
#         email="superadmin@school.com",
#         firstName=fake.first_name(),
#         middleName=fake.first_name(),
#         lastName=fake.last_name()
#       )
#     teacher.password = "superadmin"
#     teacher.save()
#     superadmin = Admin(teacher_id=teacher.id)
#     superadmin.privileges = {
#                 "create": True,
#                 "delete": True,
#                 "update": True,
#                 "superadmin": True
#             }

#     superadmin.save()

#     teacher = Teacher(
#         username="admin",
#         email="admin@school.com",
#         firstName=fake.first_name(),
#         middleName=fake.first_name(),
#         lastName=fake.last_name()
#       )
#     teacher.password = "admin"
#     teacher.save()
#     admin = Admin(teacher_id=teacher.id)
#     admin.privileges = {
#                 "create": True,
#                 "delete": True,
#                 "update": True,
#                 "superadmin": False
#     }


#     teacher = Teacher(
#         username="create",
#         email="create@school.com",
#         firstName=fake.first_name(),
#         middleName=fake.first_name(),
#         lastName=fake.last_name()
#       )
#     teacher.password = "create"
#     teacher.save()
#     admin = Admin(teacher_id=teacher.id)
#     admin.privileges = {
#                 "create": True,
#                 "delete": False,
#                 "update": False,
#                 "superadmin": False
#       }
#     admin.save()

#     print(GREEN + 
#           f"--{Admin.query.count()} USERS CREATED IN {database.upper()}--" + RESET)

#     print(GREEN + "ADNIN 1 LOGIN DETAILS" + RESET)
#     print(GREEN + "\t\tEmail: superadmin@school.com\n\t\tPassword: superadmin" + RESET)

#     print(GREEN + "ADNIN 2 LOGIN DETAILS" + RESET)
#     print(GREEN + "\t\tEmail: create@school.com\n\t\tPassword: create" + RESET)

#     student = Student(
#         username="student",
#         email="student@school.com",
#         firstName=fake.first_name(),
#         middleName=fake.first_name(),
#         lastName=fake.last_name()
#       )
#     student.password = "student"
#     student.admission_no = "78sa"
#     student.arm = "A"
#     student.save()
