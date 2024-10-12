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
        course = Course(term="First", code="MTH11")
        course.classes.append(self.Class)
        course.save()
        self.assertIn(course, self.Class.courses)
        course.delete()
        #Test class class_admitted relationship
        self.assertIsInstance(self.Class.admitted_students, InstrumentedList)
        student = Student(
            username="solayof_aci",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdcq.com",
            admission_no="5h64",
            arm="C"
        )
        student.Class_id = self.Class.id
        student.save()
        self.assertIn(student, self.Class.admitted_students)
        student.delete()
        #Test class form_teacher relationship
        self.assertIsInstance(self.Class.form_teacher, InstrumentedList)
        teacher = Teacher(
            username="king",
            email="king@chs.com"
        )
        teacher.form_class_id = self.Class.id
        teacher.save()
        self.assertIn(teacher, self.Class.form_teacher)
        teacher.delete()
        #Test class students relationship
        self.assertIsInstance(self.Class.students, InstrumentedList)
        student = Student(
            username="solayof_ui",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gduq.com",
            admission_no="5j64",
            arm="C"
        )
        student.Class_id = self.Class.id
        student.save()
        self.assertIn(student, self.Class.students)
        student.delete()
        #Test class examination relationship
        self.assertIsInstance(self.Class.examination, InstrumentedList)
        exam = Examination(mode="Test")
        exam.class_id = self.Class.id
        exam.save()
        self.assertIn(exam, self.Class.examinations)
        exam.delete()
        
    def test_all_method(self):
        """test all method in the class
        """
        classes = Class.all()
        self.assertIn(self.Class.id , classes)
        self.assertDictEqual(classes[self.Class.id], self.Class.to_dict())
        
    def test_get_method(self):
        """test get instance method with pk
        """
        clas = Class.get(self.Class.id)
        self.assertIsNotNone(clas)
        clas.delete()