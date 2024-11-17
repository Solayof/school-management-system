#!/usr/bin/python3
"""test examination model
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


class testExaminationModel(unittest.TestCase):
    """test examination model

    Args:
        unittest (model): unittest package
    """
    @classmethod
    def setUpClass(cls) -> None:
        """set up for testing
        """
        cls.exam = Examination(term="First", Mode="Test")
        cls.exam.save()
        
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Examination.id.expression.type.python_type, str)
        self.assertEqual(
            Examination.updated_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Examination.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Examination.pub_date.expression.type.python_type,
            datetime
        )
        self.assertEqual(
            Examination.mode.expression.type.python_type,
            str
        )
        self.assertEqual(
            Examination.term.expression.type.python_type,
            str
        )
        self.assertEqual(
            Examination.class_id.expression.type.python_type,
            str
        )
        self.assertEqual(
            Examination.course_id.expression.type.python_type,
            str
        )
        self.assertEqual(
            Examination.session.expression.type.python_type,
            str
        )
        
    def test_save_method(self):
        """test save method
        """
        exam = Examination(term="Second", mode="Practice")
        self.assertIsNone(Examination.get(exam.id))
        exam.save()
        self.assertIsNotNone(Examination.get(exam.id))
        exam.delete()
        
    def test_delete_method(self):
        """test delete method
        """
        exam = Examination(term="Second", mode="Practice")
        exam.save()
        self.assertIsNotNone(Examination.get(exam.id))
        exam.delete()
        self.assertIsNone(Examination.get(exam.id))
        exam.delete()
        
    def test_relationship_attributes(self):
        """test relationship attributes
        """
        exam = Examination(term="Second", mode="Practice")
        exam.save()
        #Test examanation course relationship
        self.assertNotIsInstance(exam.course, InstrumentedList)
        course = Course(name="Physics")
        course.save()
        exam.course_id = course.id
        exam.save()
        self.assertEqual(exam.course, course)
        course.delete()
        #Test examanation class relationship
        self.assertNotIsInstance(exam.Class, InstrumentedList)
        jss1 = Class(className="SSs 3")
        jss1.save()
        exam.class_id = jss1.id
        exam.save()
        self.assertEqual(exam.Class, jss1)
        jss1.delete()
        #Test examanation question(items) relationship
        self.assertIsInstance(exam.items, InstrumentedList)
        question = Question(mode="EXAM")
        question.save()
        question.examination_id = exam.id
        question.save()
        self.assertEqual(question.examination, exam)
        question.delete()
        exam.delete()
    
    def test_get_method(self):
        """test get instance method with pk
        """
        exam = Examination.get(self.exam.id)
        self.assertIsNotNone(exam)
        exam.delete()

