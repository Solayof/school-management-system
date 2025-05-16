#!/usr/bin/python3
"""subject model
"""
from sqlalchemy import Column, ForeignKey, String
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
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"))
    department = relationship(
        "Department",
        foreign_keys=[department_id],
        back_populates="subjects",
        uselist=False
    )
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
    new_dict["number_of_courses"] = len(courses) if courses else 0
    
    return new_dict

