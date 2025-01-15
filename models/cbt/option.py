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
    A = Column(String(1024))
    B = Column(String(1024))
    C = Column(String(1024))
    D = Column(String(1024))
    E = Column(String(1024))
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