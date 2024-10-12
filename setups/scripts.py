#!/usr/bin/python3

from manage import *
from faker import Faker
import random

fake = Faker()

arms = ["A", "B", "C", "D"]

for i in range(200):
  parent = Parent(
      username=fake.unique.user_name(),
      email=fake.unique.email(),
      firstName=fake.first_name(),
      middleName=fake.first_name(),
      lastName=fake.last_name()
      
    )
  parent.save()

for i in range(1, 4):
  cla = Class(className=f"jss {i}")
  cla.save()
for i in range(1, 4):
  cla = Class(className=f"sss {i}")
  cla.save()
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
parents = Parent.query.all()
for i in range(1000):
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
  
teacher = Teacher(
    username="superadmin",
    email="superadmin@school.com",
    firstName=fake.first_name(),
    middleName=fake.first_name(),
    lastName=fake.last_name()
  )
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
teacher.save()
admin = Admin(teacher_id=teacher.id)
admin.privileges = {
            "create": True,
            "delete": True,
            "update": True,
            "superadmin": False
}
