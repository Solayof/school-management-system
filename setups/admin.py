
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


fake = Faker()
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

admin = Admin(teacher_id=teacher.id)
admin.privileges = {
            "create": True,
            "delete": False,
            "update": False,
            "superadmin": False
}
