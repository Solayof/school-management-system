#!/usr/bin/python3
"""examination model
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel
from models.portal.association import exam_questions_asso


class Examination(BaseModel, Base):
    """examination model

    Args:
        BaseModel (_type_): Basemodel class
        Base (_type_): Declarative base
    """    
    __tablename__ = "examinations"
    extend_existing = True
    name   = Column(String(36), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"))
    mode = Column(String(10), nullable=False)
    session = Column(String(10), nullable=False)
    course = relationship(
        "Course",
        foreign_keys=[course_id],
        back_populates="examinations",
        uselist=False
    )
    class_id = Column(String(36), ForeignKey("classes.id"))
    Class = relationship(
        "Class",
        foreign_keys=[class_id],
        back_populates="examinations",
        uselist=False
    )
    term   = Column(String(10), nullable=False)
    items = relationship(
        "Question",
        secondary=exam_questions_asso,
        back_populates="examination",
    )
    pub_date = Column(DateTime, default=datetime.now)

    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        new_dict.pop("_password", None)
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["pub_date"] = self.pub_date.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        Class = self.Class
        if Class is not None:
            new_dict["Class"] = {
                    "id": Class.id,
                    "code": Class.code
                }

        course = self.course
        if course is not None:

            new_dict["course"] ={
                    "code": course.code,
                    "term": course.term
               
            }
        

        items = self.items
        if items is not None:
            length = 5  if len(items) > 5 else len(items)
            new_dict["items"] = {
                "number_of_items": len(items),
                "items": [
                {
                    "id": item.id,
                    "mode": item.mode,
                } for item in items
            ]
            }
        return new_dict