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
        
        classes = self.classes
        if classes is not None:
            new_dict["classes"] = [
                {
                    "id": Class.id,
                    "code": Class.code
                } for Class in classes
            ]
        
        students = self.students
        if students is not None:
            new_dict["students"] = [
                {
                    "id": student.id,
                    "fullName": student.fullName,
                    "phoneNumber": student.phone_number,
                    "email": student.email
                } for student in students
            ]
        
        exams = self.examinations
        if exams is not None:
            new_dict["examinations"] = [
                {
                    "id": exam.id,
                    "code": exam.name,
                    "term": exam.term,
                    "session": exam.session
                } for exam in exams
            ]
        
        questions = self.questions
        if questions is not None:
            new_dict["questions"] = [
                {
                    "id": question.id,
                    "mode": question.mode,
                } for question in questions
            ]
        return new_dict
