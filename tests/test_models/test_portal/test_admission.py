#!/usr/bin/python3
"""test admission model
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
import unittest


class testAdmissionModel(unittest.TestCase):
    """test admission class

    Args:
        unittest (_type_): unittesst class
    """    
    @classmethod
    def setUpClass(cls):
        """set up for testing
        """
        cls.admission = Admission(
            username="jesa",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdha",
            admission_no="231"
        )
        cls.admission.save()

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
            "admission_no",
            "previous_school",
            "class_at_previous_school",
            "parent_id"
        ]

    def test_attr(self):
        """test admission attributes
        """
        for attribute in self.attributes:
            self.assertTrue(hasattr(self.admission, attribute))

        # Test default and not nullable attributes
        self.assertIsNotNone(self.admission.id)
        self.assertIsNotNone(self.admission.created_at)
        self.assertIsNotNone(self.admission.updated_at)
        self.assertIsNotNone(self.admission.email)
        self.assertIsNotNone(self.admission.username)
        self.assertIsNotNone(self.admission.firstName)
        self.assertIsNotNone(self.admission.lastName)
        self.assertIsNotNone(self.admission.middleName)
        self.assertIsNotNone(self.admission.admission_no)

    def test_method(self):
        """test admission mode metthod
        """
        admission = self.admission.to_dict()
        self.assertIsInstance(admission, dict)
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
            self.assertTrue(attribute in admission)
        for key in admission:
            self.assertTrue(hasattr(self.admission, key))
    
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(Admission.id.expression.type.python_type, str)
        self.assertEqual(Admission.username.expression.type.python_type, str)
        self.assertEqual(
            Admission.gender.expression.type.python_type,
            str
            )
        self.assertEqual(
            Admission.address.expression.type.python_type,
            str
            )
        self.assertEqual(
            Admission.phone_number.expression.type.python_type,
            int
            )
        self.assertEqual(
            Admission.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            Admission.updated_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(Admission.dob.expression.type.python_type, datetime)
        self.assertEqual(Admission.email.expression.type.python_type, str)
        self.assertEqual(Admission.firstName.expression.type.python_type, str)
        self.assertEqual(Admission.lastName.expression.type.python_type, str)
        self.assertEqual(Admission.middleName.expression.type.python_type, str)
        self.assertEqual(Admission.parent_id.expression.type.python_type, str)
        self.assertEqual(
            Admission.previous_school.expression.type.python_type,
            str
            )
        self.assertEqual(
            Admission.admission_no.expression.type.python_type,
            str
            )
        self.assertEqual(
            Admission.class_at_previous_school.expression.type.python_type,
            str
            )

    def test_save_method(self):
        """test save method
        """
        admission = Admission(
            username="solayof_ai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdah.com",
            admission_no="345"
        )
        self.assertIsNone(Admission.get(admission.id))
        admission.save()
        self.assertIsNotNone(Admission.get(admission.id))
        admission = Admission.get(admission.id)
        admission.delete()

    def test_delete_method(self):
        """test delete method
        """
        admission = Admission(
            username="solayof_ai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdh.com",
            admission_no="564"
        )
        admission.save()
        self.assertIsNotNone(Admission.get(admission.id))
        admission.delete()
        self.assertIsNone(Admission.get(admission.id))

    def test_get_id_method(self):
        """test get_id method
        """
        self.assertEqual(self.admission.id, self.admission.get_id())

    def test_relationship_attributes(self):
        """test relationship attributes
        """
        self.assertNotIsInstance(self.admission.parent, InstrumentedList)
        parent = Parent(
            username="jesp",
            firstName="roe",
            lastName="hes",
            middleName="hs",
            email="asd@gdhp",
            address="peace house",
            occupation="Teacher"
        )

        admission = Admission(
            username="solayof_aai",
            firstName="rose",
            lastName="jess",
            middleName="Joh",
            email="asd@gdhq.com",
            admission_no="5764"
        )
        parent.save()
        admission.parent_id = parent.id
        admission.save()
        self.assertIsInstance(admission.parent, Parent)
        self.assertIn(admission, parent.children)

        jss1 = Class(className="jss 1")
        jss1.save()
        self.assertNotIsInstance(admission.class_admitted, InstrumentedList)
        admission.Class_id = jss1.id
        admission.save()
        print(admission)
        self.assertIsInstance(admission.class_admitted, Class)
        self.assertIn(admission, jss1.admitted_students)
        parent.delete()
        admission.delete()
        jss1.delete()

    def test_get_method(self):
        """test get instance method with pk
        """
        admission = Admission.get(self.admission.id)
        self.assertIsNotNone(admission)
        self.assertEqual(admission.id, self.admission.id)
        self.assertEqual(admission.created_at, self.admission.created_at)
        self.assertEqual(admission.updated_at, self.admission.updated_at)
        self.assertEqual(admission.firstName, self.admission.firstName)
        self.assertEqual(admission.username, self.admission.username)
        self.assertEqual(admission.email, self.admission.email)
        admission.delete()
