#!/usr/bin/python3
"""user model
"""
from datetime import datetime, timezone
from flask_login import UserMixin
from hashlib import sha256
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.portal.usermodel import UserModel
import models


class User(UserModel, Base, UserMixin):
    """user model definition

    Args:
        UserModel (_type_): user basemodel
        Base (_type_): Declarative base
        UserMixin (_type_): flask usermixin
    """
    __tablename__ = "users"
    username = Column(String(64), unique=True, nullable=False)
    firstName = Column(String(36))
    middleName = Column(String(36))
    lastName = Column(String(36))
    email = Column(String(36), unique=True, nullable=False)
    gender = Column(String(6))
    address = Column(String(128))
    phone_number = Column(String(16))
    dob = Column(DateTime, default=datetime.now(timezone.utc))
    password = Column(String(64))
    
    @property
    def password(self):
        """get the hash password

        Returns:
            str: the password string
        """        
        return self._password
    
    @password.setter
    def password(self, pwd):
        """set the password into encryoted version

        Args:
            pwd (str): the raw password
        """        
        self._password = sha256(pwd.encode()).hexdigest().lower()
        
    def is_valid_password(self, pwd):
        """check if the provided passowrd is valid

        Args:
            pwd (str): password to check its validity

        Returns:
            Bool: True if valid, False otherwise
        """        
        if self.password is None:
            return False
        e_pwd = pwd.encode()
        return sha256(e_pwd).hexdigest().lower() == self.password

    def isAdmin(self) -> bool:
        """check is a user is an admin

        Returns:
            bool: return True if admin otherwise False
        """        
        teac = models.portal.Admin.query.filter_by(teacher_id=self.id).count()
        if teac == 1:
            return True
        else:
            return False

    @classmethod
    def all(cls):
        """get all the instances of the class in dict

        Returns:
            bool: dict of all the class instances
        """        
        objs = {}
        for obj in cls.query.all():
            objs[obj.username] = obj.to_dict()
        return objs

