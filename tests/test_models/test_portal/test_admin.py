#!/usr/bin/python3
"""test admin model
"""
from datetime import datetime
from sqlalchemy.orm.collections import InstrumentedList
from models.customExcept import InvalidAdmin
from models.cbt.examination import  Examination
from models.cbt.question import Question
from models.cbt.response import Response
from models.cbt.score import Score
from models.portal.admission import Admission
from models.portal.admin import Admin
from models.portal.Class import Class
from models.portal.course import Course
from models.portal.parent import Parent
from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.teacher import Teacher
import unittest


class testClassModel(unittest.TestCase):
    """Test Admin model

    Args:
        unittest (_type_): unittest package
    """
    @classmethod
    def setUpClass(cls) -> None:
        """set up for testing
        """
        teacher = Teacher(
            username="jesat",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhat",
        )
        teacher.save()
        tea = Teacher.get(teacher.id)
        cls.admin = Admin(teacher_id=tea.id)
        cls.admin.save()
        
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Admin.id.expression.type.python_type, str)
        self.assertEqual(Admin.created_at.expression.type.python_type, datetime)
        self.assertEqual(Admin.updated_at.expression.type.python_type, datetime)
        self.assertEqual(Admin.teacher_id.expression.type.python_type, str)
        self.assertEqual(Admin.privileges.expression.type.python_type, dict)
        
    def test_save_method(self):
        """test save method
        """
        with self.assertRaises(InvalidAdmin) as error:
            admin = Admin(teacher_id="27955627956")
            self.assertEqual(error.exception.args[0], "User not a valid")
            
        teacher = Teacher(
            username="jestat",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhtat",
        )
        teacher.save()
        tea = Teacher.get(teacher.id)
        admin = Admin(teacher_id=tea.id)
        self.assertIsNone(Admin.get(admin.id))
        admin.save()
        self.assertIsNotNone(Admin.get(admin.id))
        
        admin.teacher_id = "wrtfgv374"
        with self.assertRaises(InvalidAdmin) as error:
            admin.save()
            self.assertEqual(error.exception.args[0], "User not valid")
        admin.delete()
        teacher.delete()
        
    def test_delete_method(self):
        """test delete method
        """
        teacher = Teacher(
            username="jestt",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhtt",
        )
        teacher.save()
        tea = Teacher.get(teacher.id)
        admin = Admin(teacher_id=tea.id)
        admin.save()
        self.assertIsNotNone(Admin.get(admin.id))
        admin.delete()
        self.assertIsNone(Admin.get(admin.id))
        teacher.delete()
    
    def test_admin_default_privileges(self):
        """test admin default privileges
        """
        for _, val in self.admin.privileges.items():
            self.assertFalse(val)
       
    def test_get_method(self):
        """test get instance method with pk
        """
        admin = Admin.get(self.admin.id)
        self.assertIsNotNone(admin)
        admin.delete()
