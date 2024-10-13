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


class testQuestionModel(unittest.TestCase):
    """test examination model

    Args:
        unittest (model): unittest package
    """
    @classmethod
    def setUpClass(cls) -> None:
        """set up for testing
        """
        cls.question = Question(mode="Test")
        cls.question.save()
        
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Question.id.expression.type.python_type, str)
        self.assertEqual(
            Question.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Question.updated_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Question.mode.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.option_A.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.option_B.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.option_C.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.option_D.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.option_E.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.answer.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.content.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.examination_id.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.course_id.expression.type.python_type,
            str
        )
        self.assertEqual(
            Question.pub_date.expression.type.python_type,
            datetime
        )
        
    def test_save_method(self):
        """test save method
        """
        question = Question(mode="Practice")
        self.assertIsNone(Question.get(question.id))
        question.save()
        self.assertIsNotNone(Question.get(question.id))
        
    def test_delete_method(self):
        """test delete method
        """
        question = Question(mode="Test")
        question.save()
        self.assertIsNotNone(Question.get(question.id))
        question.delete()
        self.assertIsNone(Question.get(question.id))
        
    def test_relationship_attributes(self):
        """test relationship attributes
        """
        question = Question(mode="Exam")
        #Test question examination relationship
        self.assertIsInstance(question.examination, InstrumentedList)
        exam = Examination(term="Second", mode="Practice")
        exam.save()
        question.examination_id = exam.id
        question.save()
        #Test question course relationship
        course = Course(code="PHY,", term="First")
        course.save()
        question.course_id = course.id
        question.save()
        self.assertEqual(question.course, course)
        self.assertIn(question, course.questions)
        #Test question response relationship
        response = Response()
        response.question_id = question.id
        response.save()
        self.assertIn(response, question.responses)
        self.assertEqual(response.question, question)
     
    def test_get_method(self):
        """test get instance method with pk
        """
        question = Question.get(self.question.id)
        self.assertIsNotNone(question)
        question.delete()

