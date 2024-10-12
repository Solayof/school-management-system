#!/usr/bin/python3
"""test course model
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


class testCourseModel(unittest.TestCase):
    """test course class

    Args:
        unittest (_type_): unittesst class
    """
    @classmethod
    def setUpClass(cls) -> None:
        """set up for testing
        """
        cls.course = Course(name="English")
        cls.course.save()
        
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Course.id.expression.type.python_type, str)
        self.assertEqual(
            Course.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Course.updated_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(Course.term.expression.type.python_type, str)
        self.assertEqual(Course.code.expression.type.python_type, str)
        
    def test_save_method(self):
        """test save method
        """
        course = Course(name="History")
        self.assertIsNone(Course.get(course.id))
        course.save()
        self.assertIsNotNone(Course.get(course.id))
        course.delete()
        
    def test_delete_method(self):
        """test delete method
        """
        course = Course(name="Yoruba")
        course.save()
        self.assertIsNotNone(Course.get(course.id))
        course.delete()
        self.assertIsNone(Course.get(course.id))
        
    def test_relationship_attributes(self):
        """test relationship attributes
        """
        #Test students course relationship
        self.assertIsInstance(self.course.students, InstrumentedList)
        student = Student(
            username="solayof_aci",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdhc.com",
            admission_no="6764",
            arm="C"
        )
        
        student.courses.append(self.course)
        student.save()
        self.assertIn(student, self.course.students)
        #Test examiantions cousre relaionship
        self.assertIsInstance(self.course.examination, InstrumentedList)
        exam = Examination(mode="Test", course_id=self.course.id, term="First")
        exam.save()
        self.assertIn(exam, self.course.examination)
        #Test questions course relationship
        self.assertIsInstance(self.course.questions, InstrumentedList)
        question = Question(course_id=self.course.id)
        question.save()
        self.assertIn(question, self.course.questions)
        #Test subject course relationship
        self.assertNotIsInstance(self.course.subject, InstrumentedList)
        subject = Subject(name="Mathrmatics", code="MTH")
        subject.save()
        self.course.subject_id = subject.id
        self.course.save()
        self.assertEqual(subject, self.course.subject)
        #Test course class relationship
        ss1 = Class(className="ss 1")
        ss1.courses.append(self.course)
        ss1.save()
        self.assertIn(ss1, self.course.classes)
        self.assertIn(self.course, ss1.courses)
        
    def test_all_method(self):
        """test all method in the class
        """
        courses = Course.all()
        self.assertIn(self.course.id, courses)
        self.assertDictEqual(courses[self.course.id], self.course.to_dict())
        
    def test_get_method(self):
        """test get instance method with pk
        """
        course = Course.get(self.course.id)
        self.assertIsNotNone(course)
        self.assertEqual(course, self.course)
        self.course.delete()
