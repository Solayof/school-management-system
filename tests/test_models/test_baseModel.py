#!/usr/bin/python3
"""test basemodel model
"""
from datetime import datetime
import unittest
from models.baseModel import BaseModel


class testUserModel(unittest.TestCase):
    """test usermodel class

    Args:
        unittest (_type_): unittest test case
    """
    @classmethod
    def setUpClass(cls):
        """set up for testing
        """
        cls.basemodel = BaseModel()

        cls.attributes = [
            "id",
            "created_at",
            "updated_at",
            ]
    
    @classmethod
    def tearDownClass(cls):
        """clear up test instance
        """
        del cls.basemodel

    def test_attr(self):
        """test basemodel attributes
        """
        for attribute in self.attributes:
            self.assertTrue(hasattr(self.basemodel, attribute))

        # Test default and not nullable attributes
        self.assertIsNotNone(self.basemodel.id)
        self.assertIsNotNone(self.basemodel.created_at)
        self.assertIsNotNone(self.basemodel.updated_at)
        
    def test_method(self):
        """test basemodel mode metthod
        """
        basemodel = self.basemodel.to_dict()
        self.assertIsInstance(basemodel, dict)
        attributes = [
            "id",
            "created_at",
            "updated_at",
            ]
        for attribute in attributes:
            self.assertTrue(attribute in basemodel)
        for key in basemodel:
            self.assertTrue(hasattr(self.basemodel, key))
    
    def test_attr_type(self):
        """test attributes type
        """
        self.assertEqual(BaseModel.id.expression.type.python_type, str)
        self.assertEqual(
            BaseModel.created_at.expression.type.python_type,
            datetime
            )
        self.assertEqual(
            BaseModel.updated_at.expression.type.python_type,
            datetime
            )
