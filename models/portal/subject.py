#!/usr/bin/python3
"""subject model
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel
from models.portal.course import Course


class Subject(BaseModel, Base):
    """subject model
    
    Usage: mathematics = Subject(
        name="Mathematics"
        code="MTH"
        )
        ohter parameters are optional

    Args:
        BaseModel (_type_): basemodel class
        Base (_type_): declarative base
    """
    __tablename__ = "subjects"
    extend_existing = True
    name = Column(String(20), nullable=False, unique=True)
    code = Column(String(6), nullable=False, unique=True)
    courses = relationship(
        "Course",
        foreign_keys="[Course.subject_id]",
        back_populates="subject",
        uselist=True
        )
    
def to_dict(self):
    """dictionary representation of class instance

    Returns:
        _type_: dict
    """        
    new_dict = self.__dict__.copy()
    new_dict.pop("_sa_instance_state", None)
    new_dict.pop("_password", None)
    new_dict["created_at"] = self.created_at.isoformat()
    new_dict["updated_at"] = self.updated_at.isoformat()
    
    courses = self.courses
    if courses is not None:
        new_dict["courses"] = [
            {
                "id": course.id,
                "code": course.code,
                "term": course.term
            } for course in courses
        ]
    
    return new_dict

