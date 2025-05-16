#!/usr/bin/python3
"""course model
"""
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel
from models.portal.association import course_teacher_asso, student_courses_asso
from models.portal.association import course_class_asso


class Course(BaseModel, Base):
    """course model
    
    Usage: Phy = Course(term="First", code="PHY12")
           other parameters are optional

    Args:
        BaseModel (_type_): basemodel class
        Base (_type_): declarative base
    """    
    __tablename__ = "courses"
    extend_existing = True
    term = Column(String(8), nullable=False)
    code = Column(String(6), nullable=False)
    teachers = relationship(
        "Teacher",
        secondary=course_teacher_asso,
        back_populates="course_teach"
        )
    classes = relationship(
        "Class",
        secondary=course_class_asso,
        back_populates="courses"
        )
    students = relationship(
        "Student",
        secondary=student_courses_asso,
        back_populates="courses"
        )
    examinations = relationship(
        "Examination",
        foreign_keys="[Examination.course_id]",
        back_populates="course",
        uselist=True
        )
    questions = relationship(
        "Question",
        foreign_keys="[Question.course_id]",
        back_populates="course",
        uselist=True
        )
    subject_id = Column(String(36), ForeignKey("subjects.id"))
    subject = relationship(
        "Subject",
        foreign_keys=[subject_id],
        back_populates="courses",
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
        
        
        
        students = self.students
        new_dict["number_of_students"] = len(students) if students else 0
        
        exams = self.examinations
        new_dict["number_of_examinations"] = len(exams) if exams else 0
        
        questions = self.questions
        new_dict["number_of_questions"] = len(questions) if questions else 0
        
        return new_dict
