#!/usr/bin/python3
"""question model
"""
from datetime import datetime, timedelta
from sqlalchemy  import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from typing import List
from models.base import Base
from models.baseModel import BaseModel
from models.cbt.examination import Examination
from models.portal.course import Course
from models.portal.association import exam_questions_asso


class Option(BaseModel, Base):
    __tablename__ = "options"
    extend_existing = True
    A = Column(Text)
    B = Column(Text)
    C = Column(Text)
    D = Column(Text)
    E = Column(Text)
    answer = Column(String(2))
    note = Column(Text)
    question_id = Column(String(36), ForeignKey("questions.id"))
    question = relationship(
        "Question",
        foreign_keys=[question_id],
        back_populates="options",
        uselist=False
    )

    response_id = Column(String(36), ForeignKey("responses.id"))
    response = relationship(
        "Response",
        foreign_keys=[response_id],
        back_populates="option",
        uselist=True
    )

    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """
        # if self.question is None or self.question.was_published() is False:
        #     return {}
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        new_dict.pop('question', None)
        new_dict.pop('response', None)
        if self.A:
            new_dict["A"] = self.A
        if self.B:
            new_dict["B"] = self.B
        if self.C:
            new_dict["C"] = self.C
        if self.D:
            new_dict['D'] = self.D 
        if self.E:
            new_dict['E'] = self.E
        new_dict["note"] =self.note
        # new_dict['answer'] = self.answer 
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        
        return new_dict
