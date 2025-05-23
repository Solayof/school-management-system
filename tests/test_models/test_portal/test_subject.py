#!/usr/bin/python3
"""test subject model
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


class testSubjectModel(unittest.TestCase):
    """Test subject model

    Args:
        unittest (_type_): unittest class
    """
    @classmethod
    def setUpClass(cls) -> None:
        """set up for testing
        """
        cls.subject = Subject(term="first", name="Igbo Language", code="IGB")
        cls.subject.save()
    
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Subject.id.expression.type.python_type, str)
        self.assertEqual(Subject.name.expression.type.python_type, str)
        self.assertEqual(Subject.code.expression.type.python_type, str)
        self.assertEqual(
            Subject.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Subject.updated_at.expression.type.python_type,
            datetime
            )
        
    def test_save_method(self):
        """test save method
        """
        subject = Subject(term="first", name="Commerce", code="COM")
        subject.save()
        self.assertIsNotNone(Subject.get(subject.id))
        subject.save()
        self.assertIsNotNone(Subject.get(subject.id))
        subject.delete()
       
    def test_delete_method(self):
        """test delete method
        """
        subject = Subject(term="first", name="Chemistry", code="CHM")
        subject.save()
        self.assertIsNotNone(Subject.get(subject.id))
        subject.delete()
        self.assertIsNone(Subject.get(subject.id))
        
    def test_relationship_attributes(self):
        """test relationship attributes
        """
        subject = Subject(term="first", name="Chemis", code="CMM")
        self.assertIsInstance(
            subject.courses,
            InstrumentedList
            )
        subject.save()
        course = Course(code="Ans", term="first")
        course.subject_id = subject.id
        course.save()
        self.assertIn(course, subject.courses)
        subject.delete()
        course.delete()

    def test_get_method(self):
        """test get instance method with pk
        """
        subject = Subject.get(self.subject.id)
        self.assertEqual(subject, self.subject)
        self.subject.delete()
