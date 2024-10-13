#!/usr/bin/python3
"""test teacher model
"""
from datetime import datetime
from sqlalchemy.orm.collections import InstrumentedList
from models.cbt.examination import  Examination
from models.cbt.question import Question
from models.cbt.response import Response
from models.cbt.score import Score
from models.portal.admission import Admission
from models.portal.Class import Class
from models.portal.course import Course
from models.portal.parent import Parent
from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.teacher import Teacher
import unittest


class testTeacherModel(unittest.TestCase):
    """test teacher class

    Args:
        unittest (_type_): unittesst class
    """    
    @classmethod
    def setUpClass(cls):
        """set up for testing
        """
        cls.teacher = Teacher(
            username="jesat",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhat",
        )
        cls.teacher.save()

        cls.attributes = [
            "id",
            "created_at",
            "updated_at",
            "gender",
            "firstName",
            "middleName",
            "lastName",
            "username",
            "dob",
            "email",
            "phone_number",
            "address",
            "_id",
            "staff_id",
            "file_no",
            "grade_level",
            "previous_school",
            "date_transfer",
            "last_promote_date",
            "form_class_id"
            
        ]

    def test_attr(self):
        """test teacher attributes
        """
        for attribute in self.attributes:
            self.assertTrue(hasattr(self.teacher, attribute))

        # Test default and not nullable attributes
        self.assertIsNotNone(self.teacher.id)
        self.assertIsNotNone(self.teacher.created_at)
        self.assertIsNotNone(self.teacher.updated_at)
        self.assertIsNotNone(self.teacher.email)
        self.assertIsNotNone(self.teacher.username)
        self.assertIsNotNone(self.teacher.firstName)
        self.assertIsNotNone(self.teacher.lastName)
        self.assertIsNotNone(self.teacher.middleName)

    def test_method(self):
        """test teacher mode metthod
        """
        teacher = self.teacher.to_dict()
        self.assertIsInstance(teacher, dict)
        attributes = [
            "id",
            "email",
            "created_at",
            "updated_at",
            "firstName",
            "lastName",
            "username",
            "middleName"
        ]
        for attribute in attributes:
            self.assertTrue(attribute in teacher)
        for key in teacher:
            self.assertTrue(hasattr(self.teacher, key))
    
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Teacher.id.expression.type.python_type, str)
        self.assertEqual(Teacher.username.expression.type.python_type, str)
        self.assertEqual(Teacher.gender.expression.type.python_type, str)
        self.assertEqual(Teacher.address.expression.type.python_type, str)
        self.assertEqual(Teacher.phone_number.expression.type.python_type, str)
        self.assertEqual(
            Teacher.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Teacher.updated_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(Teacher.dob.expression.type.python_type, datetime)
        self.assertEqual(Teacher.email.expression.type.python_type, str)
        self.assertEqual(Teacher.firstName.expression.type.python_type, str)
        self.assertEqual(Teacher.lastName.expression.type.python_type, str)
        self.assertEqual(Teacher.middleName.expression.type.python_type, str)
        self.assertEqual(Teacher.staff_id.expression.type.python_type, str)
        self.assertEqual(
            Teacher.previous_school.expression.type.python_type,
            str
            )
        self.assertEqual(Teacher.file_no.expression.type.python_type, str)
        self.assertEqual(Teacher.grade_level.expression.type.python_type, str)
        self.assertEqual(
            Teacher.date_transfer.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Teacher.last_promote_date.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Teacher.form_class_id.expression.type.python_type,
            str
            )
        self.assertEqual(Teacher._id.expression.type.python_type, str)

    def test_save_method(self):
        """test save method
        """
        teacher = Teacher(
            username="solayof_ati",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdaht.com",
        )
        self.assertIsNone(Teacher.get(teacher.id))
        teacher.save()
        self.assertIsNotNone(Teacher.get(teacher.id))
        teacher.delete()

    def test_delete_method(self):
        """test delete method
        """
        teacher = Teacher(
            username="solayof_ati",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdth.com",
        )
        teacher.save()
        self.assertIsNotNone(Teacher.get(teacher.id))
        teacher.delete()
        self.assertIsNone(Teacher.get(teacher.id))

    def test_get_id_method(self):
        """test get_id method
        """
        self.assertEqual(self.teacher.id, self.teacher.get_id())

    def test_relationship_attributes(self):
        """test relationship attributes
        """
        self.assertIsInstance(self.teacher.course_teach, InstrumentedList)
        course = Course(term="Third", code="ANH")

        teacher = Teacher(
            username="solayof_arti",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdhyq.com",
        )
        #Test teacher course relationship
        course.teachers.append(teacher)
        teacher.save()
        course.save()
        self.assertIn(teacher, course.teachers)
        #Test teacher 
        self.assertNotIsInstance(teacher.formClass, InstrumentedList)
        jss1 = Class(className="jss 1")
        teacher.form_class_id = jss1.id
        jss1.save()
        self.assertIn(teacher, jss1.form_teacher)
        teacher.delete()
        jss1.delete()

    def test_get_method(self):
        """test get instance method with pk
        """
        teacher = Teacher.get(self.teacher.id)
        self.assertIsNotNone(teacher)
        teacher.delete()
