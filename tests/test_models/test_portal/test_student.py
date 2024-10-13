#!/usr/bin/python3
"""test student model
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


class testStudentModel(unittest.TestCase):
    """test student class

    Args:
        unittest (_type_): unittesst class
    """    
    @classmethod
    def setUpClass(cls):
        """set up for testing
        """
        cls.student = Student(
            username="jedsa",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdha",
            admission_no="231",
            arm="A"
        )
        cls.student.save()

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
            "admission_no",
            "previous_school",
            "class_at_previous_school",
            "parent_id",
            "arm",
            "classroom_id",
            "_attendance"
        ]

    def test_attr(self):
        """test student attributes
        """
        for attribute in self.attributes:
            self.assertTrue(hasattr(self.student, attribute))

        # Test default and not nullable attributes
        self.assertIsNotNone(self.student.id)
        self.assertIsNotNone(self.student.created_at)
        self.assertIsNotNone(self.student.updated_at)
        self.assertIsNotNone(self.student.email)
        self.assertIsNotNone(self.student.username)
        self.assertIsNotNone(self.student.firstName)
        self.assertIsNotNone(self.student.lastName)
        self.assertIsNotNone(self.student.middleName)
        self.assertIsNotNone(self.student.admission_no)
        self.assertIsNotNone(self.student.arm)



    def test_method(self):
        """test student mode metthod
        """
        student = self.student.to_dict()
        self.assertIsInstance(student, dict)
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
            self.assertTrue(attribute in student)
        for key in student:
            self.assertTrue(hasattr(self.student, key))
    
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Student.id.expression.type.python_type, str)
        self.assertEqual(Student.username.expression.type.python_type, str)
        self.assertEqual(Student.gender.expression.type.python_type, str)
        self.assertEqual(Student.address.expression.type.python_type, str)
        self.assertEqual(Student.phone_number.expression.type.python_type, str)
        self.assertEqual(
            Student.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Student.updated_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Student.dob.expression.type.python_type,
            datetime
            )
        self.assertEqual(Student.email.expression.type.python_type, str)
        self.assertEqual(Student.firstName.expression.type.python_type, str)
        self.assertEqual(Student.lastName.expression.type.python_type, str)
        self.assertEqual(Student.middleName.expression.type.python_type, str)
        self.assertEqual(Student.parent_id.expression.type.python_type, str)
        self.assertEqual(
            Student.previous_school.expression.type.python_type,
            str)
        self.assertEqual(Student.admission_no.expression.type.python_type, str)
        self.assertEqual(
            Student.class_at_previous_school.expression.type.python_type,
            str
            )
        self.assertEqual(Student.arm.expression.type.python_type, str)
        self.assertEqual(Student.classroom_id.expression.type.python_type, str)
        self.assertEqual(Student.admission_no.expression.type.python_type, str)
        self.assertEqual(Student._attendance.expression.type.python_type, dict)

    def test_save_method(self):
        """test save method
        """
        student = Student(
            username="solayof_ai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdah.com",
            admission_no="345",
            arm="B"
        )
        self.assertIsNone(Student.get(student.id))
        student.save()
        self.assertIsNotNone(Student.get(student.id))
        student.delete()

    def test_delete_method(self):
        """test delete method
        """
        student = Student(
            username="solayof_ai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdh.com",
            admission_no="564",
            arm="D"
        )
        student.save()
        self.assertIsNotNone(Student.get(student.id))
        student.delete()
        self.assertIsNone(Student.get(student.id))

    def test_get_id_method(self):
        """test get_id method
        """
        self.assertEqual(self.student.id, self.student.get_id())

    def test_relationship_attributes(self):
        """test relationship attributes
        """
        self.assertNotIsInstance(self.student.parent, InstrumentedList)
        parent = Parent(
            username="jesp",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhp",
            address="peace house",
            occupation="Teacher",
        )

        student = Student(
            username="solayof_aai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdhq.com",
            admission_no="5764",
            arm="C"
        )
        parent.save()
        #Test student parent relationship
        student.parent_id = parent.id
        student.save()
        self.assertIsInstance(student.parent, Parent)
        self.assertIn(student, parent.children)
        adm = Admission.get(student.id)
        self.assertIn(adm, parent.children)
    
        #Test student classroom relationship
        jss1 = Class(className="jss 1")
        jss1.save()
        self.assertNotIsInstance(student.classroom, InstrumentedList)
        student.classroom_id = jss1.id
        student.save()
        classroom = student.classroom
        self.assertIsInstance(classroom, Class)
        self.assertIn(student, jss1.students)
        parent.delete()
        student.delete()
        jss1.delete()
        #Test student courses relationship
        self.assertIsInstance(student.courses, InstrumentedList)
        course = course(id="MTHH12", name="Mathematics")
        student.courses.append(course)
        self.assertIn(student, course.students)
        self.assertIn(course, student.courses)
        course.delete()
        #Test Student response relationship
        self.assertIsInstance(student.responses, InstrumentedList)
        response = Response(student_id=student.id)
        response.save()
        self.assertIn(response, student.responses)
        response.delete()
        #Test student scores relationship
        self.assertIsInstance(student.scores, InstrumentedList)
        score = Score(student_id=student.id)
        score.save()
        self.assertIn(score, student.responses)
        score.delete()
        student.delete()

    def test_get_method(self):
        """test get instance method with pk
        """
        student = Student.get(self.student.id)
        self.assertIsNotNone(student)
        self.assertEqual(student.id, self.student.id)
        self.assertEqual(student.created_at, self.student.created_at)
        self.assertEqual(student.updated_at, self.student.updated_at)
        self.assertEqual(student.firstName, self.student.firstName)
        self.assertEqual(student.username, self.student.username)
        self.assertEqual(student.email, self.student.email)
        student.delete()
