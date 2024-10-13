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
        subject = Subject(term="first", name="Chemistry", code="CHM")
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
        subject = Subject(term="first", name="Chemistry", code="CHM")
        self.assertIsInstance(
            subject.courses,
            InstrumentedList
            )
        course = Course(code="Ans", term="first")
        course.subject_id = self.subject.id
        course.save()
        self.assertIn(course, self.subject.courses)
        course.delete()
        
    def test_all_method(self):
        """test all method in the class
        """
        subjects = Subject.all()
        self.assertIn(self.subject.id, subjects)
        self.assertDictEqual(subjects[self.subject.id], self.subject.to_dict())
        
    def test_get_method(self):
        """test get instance method with pk
        """
        subject = Subject.get(self.subject.id)
        self.assertEqual(subject, self.subject)
        self.subject.delete()
