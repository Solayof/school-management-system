#!/usr/bin/python3
"""question model
"""
from datetime import datetime, timedelta
from sqlalchemy  import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from typing import List
from models.base import Base
from models.baseModel import BaseModel
from models.cbt.examination import Examination
from models.portal.course import Course
from models.portal.association import exam_questions_asso


class Question(BaseModel, Base):
    """question model

    Args:
        BaseModel (_type_): basemodel class
        Base (_type_): _description_

    Returns:
        Question: resturns Question class instance
    """    
    __tablename__ = "questions"
    extend_existing = True
    content = Column(String(2048))
    option_A = Column(String(1024))
    option_B = Column(String(1024))
    option_C = Column(String(1024))
    option_D = Column(String(1024))
    option_E = Column(String(1024))
    mode = Column(String(10), nullable=False)
    answer = Column(String(1024))
    examination_id = Column(String(36), ForeignKey("examinations.id"))
    examination = relationship(
        "Examination",
        secondary=exam_questions_asso,
        back_populates="items",
        uselist=False
    )
    course_id = Column(String(16), ForeignKey("courses.id"))
    course  = relationship(
        "Course",
        foreign_keys=[course_id],
        back_populates="questions",
        uselist=False
    )
    responses = relationship(
        "Response",
        foreign_keys="[Response.question_id]",
        back_populates="question",
        uselist=True
    )
    pub_date = Column(DateTime, default=datetime.now)

    def was_published(self):
        """check if the question is publish

        Returns:
            bool: True is published, False otherwise
        """        
        return self.pub_date <= datetime.now() + timedelta(days=1)
    
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
        
        courses = self.courses
        if courses is not None:
            length = 5  if len(courses) > 5 else len(courses)
            new_dict["courses"] ={
                "number_of_courses": len(courses),
                "courses": [
                {
                    "code": courses[i].code,
                    "term": courses[i].term
                } for i in range(length)
            ]
            }
        
        responses = self.responses
        if responses is not None:
            new_dict["responses"] = [
                {
                    "id": response.id
                } for response in responses
            ]
        
        exam = self.examination
        if exam is not None:
            new_dict["examination"] = [
                {
                    "id": exam.id,
                    "code": exam.name,
                    "term": exam.term,
                    "session": exam.session
                }
            ]
        return new_dict
