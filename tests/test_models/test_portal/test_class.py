#!/usr/bin/python3
"""test class model
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


class testClassModel(unittest.TestCase):
    """Test class model

    Args:
        unittest (_type_): unittest package
    """
    @classmethod
    def setUpClass(cls) -> None:
        """set up for testing
        """
        cls.Class = Class(className=" jss 2")
        cls.Class.save()
        
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Class.id.expression.type.python_type, str)
        self.assertEqual(
            Class.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Class.updated_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(Class.className.expression.type.python_type, str)
        self.assertEqual(Class.session.expression.type.python_type, str)
        
    def test_save_method(self):
        """test save method
        """
        jss3 = Class(className="jss 3")
        self.assertIsNone(Class.get(jss3.id))
        jss3.save()
        self.assertIsNotNone(Class.get(jss3.id))
        jss3.delete()
        
    def test_delete_method(self):
        """test delete method
        """
        jss1 = Class(clasName="jss 1")
        jss1.save()
        self.assertIsNotNone(Class.get(jss1.id))
        jss1.delete()
        self.assertIsNone(Class.get(jss1.id))
        
    def test_relationship_attributes(self):
        """test relationship attributes
        """
        #Test class courses relationship
        self.assertIsInstance(self.Class.courses, InstrumentedList)
        clas = Class(className="ssd 2")
        clas.save()
        course = Course(term="First", code="MTH11")
        course.classes.append(clas)
        course.save()
        self.assertIn(course, clas.courses)
        #Test class class_admitted relationship
        self.assertIsInstance(clas.admitted_students, InstrumentedList)
        student = Student(
            username="solayof_aci",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdcq.com",
            admission_no="5h64",
            arm="C"
        )
        # student.Class_id = clas.id
        student.save()
        adm = Admission.get(student.id)
        clas.admitted_students.append(adm)
        clas.save()
        self.assertIn(student, clas.admitted_students)
        student.delete()
        #Test class form_teacher relationship
        self.assertIsInstance(clas.form_teacher, InstrumentedList)
        teacher = Teacher(
            username="king",
            email="king@chs.com"
        )
        # teacher.form_class_id = clas.id
        teacher.save()
        clas.form_teacher.append(teacher)
        self.assertIn(teacher, clas.form_teacher)
        #Test class students relationship
        self.assertIsInstance(clas.students, InstrumentedList)
        student = Student(
            username="solayof_ui",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gduq.com",
            admission_no="5j64",
            arm="C"
        )
        clas.students.append(student)
        student.save()
        self.assertIn(student, clas.students)
        #Test class examination relationship
        self.assertIsInstance(clas.examinations, InstrumentedList)
        exam = Examination(
            term="first",
            name="Physics",
            session="2024/2025",
            mode="Test"
        )
        clas.examinations.append(exam)
        exam.save()
        clas.save()
        self.assertIn(exam, clas.examinations)
        clas.delete()
        course.delete()
        exam.delete()
        teacher.delete()
        student.delete()

    def test_get_method(self):
        """test get instance method with pk
        """
        clas = Class.get(self.Class.id)
        self.assertIsNotNone(clas)
        clas.delete()
