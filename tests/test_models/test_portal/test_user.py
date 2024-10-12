#!/usr/bin/python3
"""test user base model
"""
from datetime import datetime
import unittest
from api.v1.views.portal import portal
from models.cbt.examination import Examination
from models.cbt.question import Question
from models.cbt.response import Response
from models.cbt.score import Score
from models.portal.admin import Admin
from models.portal.admission import Admission
from models.portal.Class import Class
from models.portal.course import Course
from models.portal.parent import Parent
from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.teacher import Teacher
from models.portal.user import User


class testUserModel(unittest.TestCase):
    """test usermodel class

    Args:
        unittest (_type_): unittest test case
    """
    @classmethod
    def setUpClass(cls):
        """set up for testing
        """
        cls.user = User(
            username="jes",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdh"
        )
        cls.user.save()

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
            "address"
        ]

    def test_attr(self):
        """test user attributes
        """
        for attribute in self.attributes:
            self.assertTrue(hasattr(self.user, attribute))

        # Test default and not nullable attributes
        self.assertIsNotNone(self.user.id)
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
        self.assertIsNotNone(self.user.email)
        self.assertIsNotNone(self.user.username)
        self.assertIsNotNone(self.user.firstName)
        self.assertIsNotNone(self.user.lastName)
        self.assertIsNotNone(self.user.middleName)

    def test_method(self):
        """test user mode metthod
        """
        user = self.user.to_dict()
        self.assertIsInstance(user, dict)
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
            self.assertTrue(attribute in user)
        for key in user:
            self.assertTrue(hasattr(self.user, key))
    
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(User.id.expression.type.python_type, str)
        self.assertEqual(User.username.expression.type.python_type, str)
        self.assertEqual(User.gender.expression.type.python_type, str)
        self.assertEqual(User.address.expression.type.python_type, str)
        self.assertEqual(User.phone_number.expression.type.python_type, int)
        self.assertEqual(User.created_at.expression.type.python_type, datetime)
        self.assertEqual(User.updated_at.expression.type.python_type, datetime)
        self.assertEqual(User.dob.expression.type.python_type, datetime)
        self.assertEqual(User.email.expression.type.python_type, str)
        self.assertEqual(User.firstName.expression.type.python_type, str)
        self.assertEqual(User.lastName.expression.type.python_type, str)
        self.assertEqual(User.middleName.expression.type.python_type, str)

    def test_save_method(self):
        """test save method
        """
        user = User(
            username="solayof_ai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdh.com"
        )
        self.assertIsNone(User.get(user.id))
        user.save()
        self.assertIsNotNone(User.get(user.id))
        user = User.get(user.id)
        user.delete()

    def test_delete_method(self):
        """test delete method
        """
        user = User(
            username="solayof_ai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdh.com"
        )
        user.save()
        self.assertIsNotNone(User.get(user.id))
        user.delete()
        self.assertIsNone(User.get(user.id))

    def test_get_id_method(self):
        """test get_id method
        """
        self.assertEqual(self.user.id, self.user.get_id())

    def test_all_method(self):
        """test all method in the class
        """
        objs_dict = User.all()
        self.assertIn(self.user.username, objs_dict)
        self.assertDictEqual(objs_dict[self.user.username], self.user.to_dict())

    def test_get_method(self):
        """test get instance method with pk
        """
        user = User.get(self.user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user.id)
        self.assertEqual(user.created_at, self.user.created_at)
        self.assertEqual(user.updated_at, self.user.updated_at)
        self.assertEqual(user.firstName, self.user.firstName)
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.email, self.user.email)
        user.delete()
