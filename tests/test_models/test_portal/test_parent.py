#!/usr/bin/python3
"""test teacher model
"""
from datetime import datetime
from sqlalchemy.orm.collections import InstrumentedList
from models.cbt.examination import  Examination
from models.cbt.question import Question
from models.cbt.response import Response
from models.cbt.score import Score
from models.portal.admission import Admission
from models.portal.Class import Class
from models.portal.parent import Parent
from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.teacher import Teacher
from tests.test_models.test_portal.test_user import testUserModel
import unittest


class testParentModel():
    """test parent model

    Args:
        testUserModel (_type_): parent model test class
    """
    @classmethod
    def setUpClass(cls):
        """set up for testing
        """
        cls.parent = Parent(
            username="jesp",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhp",
            address="peace house",
            occupation="Teacher"
        )
        cls.parent.save()

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
            "address",
            "occupation"
        ]

    def test_attr(self):
        """test parent attributes
        """
        for attribute in self.attributes:
            self.assertTrue(hasattr(self.parent, attribute))

        # Test default and not nullable attributes
        self.assertIsNotNone(self.parent.id)
        self.assertIsNotNone(self.parent.created_at)
        self.assertIsNotNone(self.parent.updated_at)
        self.assertIsNotNone(self.parent.email)
        self.assertIsNotNone(self.parent.username)
        self.assertIsNotNone(self.parent.firstName)
        self.assertIsNotNone(self.parent.lastName)
        self.assertIsNotNone(self.parent.middleName)
        self.assertIsNotNone(self.parent.address)
        self.assertIsNotNone(self.parent.occupation)

    def test_method(self):
        """test parent mode metthod
        """
        parent = self.parent.to_dict()
        self.assertIsInstance(parent, dict)
        attributes = [
            "id",
            "email",
            "created_at",
            "updated_at",
            "firstName",
            "lastName",
            "username",
            "middleName",
            "occupation",
            "address"
        ]
        for attribute in attributes:
            self.assertTrue(attribute in parent)
        for key in parent:
            self.assertTrue(hasattr(self.parent, key))
    
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Parent.id.expression.type.python_type, str)
        self.assertEqual(Parent.username.expression.type.python_type, str)
        self.assertEqual(Parent.gender.expression.type.python_type, str)
        self.assertEqual(Parent.address.expression.type.python_type, str)
        self.assertEqual(Parent.phone_number.expression.type.python_type, str)
        self.assertEqual(
            Parent.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Parent.updated_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(Parent.dob.expression.type.python_type, datetime)
        self.assertEqual(Parent.email.expression.type.python_type, str)
        self.assertEqual(Parent.firstName.expression.type.python_type, str)
        self.assertEqual(Parent.lastName.expression.type.python_type, str)
        self.assertEqual(Parent.middleName.expression.type.python_type, str)
        self.assertEqual(Parent.occupation.expression.type.python_type, str)

    def test_save_method(self):
        """test save method
        """
        parent = Parent(
            username="solayof_ai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdh.com"
        )
        self.assertIsNone(Parent.get(parent.id))
        parent.save()
        self.assertIsNotNone(Parent.get(parent.id))
        parent = Parent.get(parent.id)
        parent.delete()

    def test_delete_method(self):
        """test delete method
        """
        parent = Parent(
            username="solayof_ai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdh.com"
        )
        parent.save()
        self.assertIsNotNone(Parent.get(parent.id))
        parent.delete()
        self.assertIsNone(Parent.get(parent.id))

    def test_get_id_method(self):
        """test get_id method
        """
        self.assertEqual(self.parent.id, self.parent.get_id())

    def test_all_method(self):
        """test all method in the class
        """
        objs_dict = Parent.all()
        self.assertIn(self.parent.username, objs_dict)
        self.assertIn(self.parent.to_dict(), objs_dict.items())
        self.assertDictEqual(objs_dict[self.parent.username], self.parent.to_dict())

    def test_relationship_attributes(self):
        """test relationship attributes
        """
        self.assertIsInstance(self.parent.chilren, InstrumentedList)
        for student in self.parent.children:
            self.assertIsInstance(student, Admission)

    def test_get_method(self):
        """test get instance method with pk
        """
        parent = Parent.get(self.parent.id)
        self.assertIsNotNone(parent)
        self.assertEqual(parent.id, self.parent.id)
        self.assertEqual(parent.created_at, self.parent.created_at)
        self.assertEqual(parent.updated_at, self.parent.updated_at)
        self.assertEqual(parent.firstName, self.parent.firstName)
        self.assertEqual(parent.username, self.parent.username)
        self.assertEqual(parent.email, self.parent.email)
        self.assertEqual(parent.occupation, self.parent.occupation)
        self.assertEqual(parent.address, self.parent.address)
        parent.delete()
