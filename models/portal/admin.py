#!/usr/bin/python3
"""admin model
"""
from sqlalchemy import Column, ForeignKey, JSON, String
from models.base import Base
from models.baseModel import BaseModel
from models.customExcept import InvalidAdmin
from models.portal.teacher import Teacher


class Admin(BaseModel, Base):
    """admin model

    Args:
        Teacher (_type_): Teacher model class
    """
    __tablename__ = "admins"
    extend_existing = True
    teacher_id = Column(
        String(36),
        ForeignKey("teachers._id", ondelete="CASCADE"),
        nullable=False
        )
    privileges = Column(JSON())
    
    def __init__(self, *args, **kwargs):
        """initialize admin model

        Raises:
            InvalidUser: customize User exception
        """
        self.prvileges = {
            "create": False,
            "delete": False,
            "update": False,
            "superadmin": False
        }
        if Teacher.get(kwargs["teacher_id"]) is None:
            raise InvalidAdmin("User not valid")
        super().__init__(*args, **kwargs)
 
    def save(self):
        """admin save method

        Raises:
            InvalidUser: customize User exception
        """        
        if Teacher.get(self.teacher_id) is None:
            raise InvalidAdmin("User not valid")
        super().save()
