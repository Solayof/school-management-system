#!/usr/bin/python3
"""test response model
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


class testResponseModel(unittest.TestCase):
    """Test response model

    Args:
        unittest (_type_): unittest package
    """
    @classmethod
    def setUpClass(cls) -> None:
        """set up for testing
        """
        cls.response = Response()
        cls.response.save()
    
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Response.id.expression.type.python_type, str)
        self.assertEqual(
            Response.created_at.expression.type.python_type,
            datetime
        )
        self.assertEqual(
            Response.updated_at.expression.type.python_type,
            datetime
        )
        self.assertEqual(
            Response.response.expression.type.python_type,
            str
        )
        self.assertEqual(
            Response.question_id.expression.type.python_type,
            str
        )
        self.assertEqual(
            Response.student_id.expression.type.python_type,
            str
        )
        self.assertEqual(
            Response.score_id.expression.type.python_type,
            str
        )
        
    def test_save_method(self):
        """test save method
        """
        response = Response()
        self.assertIsNone(Response.get(response.id))
        response.save()
        self.assertIsNotNone(Response.get(response.id))
        
    def test_delete_method(self):
        """test delete method
        """
        response = Response()
        response.save()
        self.assertIsNotNone(Response.get(response.id))
        response.delete()
        self.assertIsNone(Response.get(response.id))
        
    def test_relationship_attributes(self):
        """test relationship attributes
        """
        response = Response()
        response.save()
        #Test response question relationship
        question = Question(mode="TEst")
        response.question_id = question.id
        response.save()
        self.assertEqual(question, response.question)
        self.assertIn(response, question.responses)
        #Test response student relationship
        student = Student(
            username="jersa",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhar",
            admission_no="r231",
            arm="A"
        )
        student.save()
        response.student_id = student.id
        response.save()
        self.assertEqual(student, response.student)
        self.assertIn(response, student.responses)
        student.delete()
        #Test response score relationship
        score = Score("Test")
        score.save()
        response.score_id = score.id
        response.save()
        self.assertIn(response, score.responses)
        self.assertEqual(score, response.score)
        response.delete()
        score.delete()
      
    def test_get_method(self):
        """test get instance method with pk
        """
        response = Response.get(self.response.id)
        self.assertIsNotNone(response)
        response.delete()
