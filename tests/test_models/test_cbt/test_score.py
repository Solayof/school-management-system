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


class testScoreModel(unittest.TestCase):
    """Test response model

    Args:
        unittest (_type_): unittest package
    """
    @classmethod
    def setUpClass(cls) -> None:
        """set up for testing
        """
        cls.score = Score()
        cls.score.save()

    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Score.id.expression.type.python_type, str)
        self.assertEqual(
            Score.created_at.expression.type.python_type,
            datetime
        )
        self.assertEqual(
            Score.updated_at.expression.type.python_type,
            datetime
        )
        self.assertEqual(
            Score.student_id.expression.type.python_type,
            str
        )
        self.assertEqual(
            Score.mode.expression.type.python_type,
            str
        )
        self.assertEqual(
            Score.scores.expression.type.python_type,
            int
        )
        
    def test_all_method(self):
        """test all method in the class
        """
        scores = Score.all()
        self.assertIn(self.score.id , scores)
        self.assertDictEqual(scores[self.score.id], self.score.to_dict())
        
    def test_get_method(self):
        """test get instance method with pk
        """
        score = Score.get(self.score.id)
        self.assertIsNotNone(score)
        score.delete()
        
    def test_relationship_attributes(self):
        """test relationship attributes
        """
        score = Score(mode="Test")
        #Test score student relationship
        student = Student(
            username="jersca",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhasr",
            admission_no="sr231",
            arm="A"
        )
        student.save()
        score.student_id = student.id
        score.save()
        self.assertEqual(student, score.student)
        self.assertIn(score, student.scores)
        student.delete()
        #Test score response relationship
        response = Response(score_id=score.id)
        response.save()
        self.assertEqual(score, response.score)
        self.assertIn(response, score)
        response.delete()
        score.delete()
