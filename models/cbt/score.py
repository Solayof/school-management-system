#!/usr/bin/python3
"""score model
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel


class Score(BaseModel, Base):
    """score model

    Args:
        BaseModel (_type_): Basemodel class
        Base (_type_): Declarative base

    Returns:
        Score: Score instance
    """    
    __tablename__ = "scores"
    extend_existing = True
    student_id = Column(String(36), ForeignKey("students._id"))
    mode = Column(String(10), nullable=False)
    student = relationship(
        "Student",
        foreign_keys=[student_id],
        back_populates="scores",
        uselist=False
    )
    responses = relationship(
        "Response",
        foreign_keys="[Response.score_id]",
        back_populates="score",
        uselist=True
    )
    scores = Column(Integer(), default=0)

    @property
    def scores(self):
        """instance score

        Returns:
            int: instance score
        """        
        return self.scores

    @scores.setter
    def scores(self, point: int):
        """_summary_

        Args:
            point (int): value to update intance score with
        """        
        self.scores = self.scores + point
        
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
        student = self.student
        if student is not None:
            new_dict["student"] = [
                {
                    "id": student.id,
                    "fullName": student.fullName()
                }
            ]
        responses = self.responses
        if responses is not None:
            new_dict["responses"] = [
                {
                    "id": response.id,
                    "term": response.remark
                } for response in responses
            ]
        return new_dict

