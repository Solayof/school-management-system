#!/usr/bin/python3
"""response model
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel
from models.cbt.question import Question
from models.cbt.score import Score
from models.portal.student import Student


class Response(BaseModel, Base):
    """response model

    Args:
        BaseModel (_type_): basemodel class
        Base (_type_): declarative base
    """    
    __tablename__ = "responses"
    extend_existing = True
    note = Column(Text)
    answer = Column(String(2))
    student_id = Column(String(36), ForeignKey("students._id"))
    student = relationship(
        "Student",
        foreign_keys=[student_id],
        back_populates="responses",
        uselist=False
    )
    option = relationship(
        "Option",
        foreign_keys="[Option.response_id]",
        back_populates="response",
        uselist=False
    )
    remark = Column(Boolean, default=None)
    score_id = Column(String(36), ForeignKey("scores.id"))
    grade = Column(Integer(), default=0)
    score = relationship(
        "Score",
        foreign_keys=[score_id],
        uselist=False
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
        question = self.question
        if question is not None:
            new_dict["question"] = [
                {
                    "id": question.id,
                    "code": question.mode
                }
            ]

        student = self.student
        if student is not None:
            new_dict["student"] = [
                {
                    "id": student.id,
                    "fullName": student.fullName()
                }
            ]
        score = self.score
        if score is not None:
            new_dict["score"] = [
                {
                    "id": score.id,
                    "term": score.scores,
                }
            ]
        return new_dict
