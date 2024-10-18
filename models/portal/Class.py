#!/usr/bin/python3
"""class model
"""
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel
from models.portal.association import course_class_asso
from models.portal.course import Course


class Class(BaseModel, Base):
    """class model
    
    Usage: jss1 = Class(className="Jss 1")
            others parameters are optional

    Args:
        BaseModel (_type_): Basemodel class
        Base (_type_): declarative base
    """    
    __tablename__ = "classes"
    extend_existing = True
    code = Column(String(16), unique=True)
    session = Column(String(9))
    className = Column(String(6))
    courses = relationship(
        "Course",
        secondary=course_class_asso,
        back_populates="classes",
        uselist=True
        )
    admitted_students = relationship(
        "Admission",
        back_populates="class_admitted", 
        uselist=True
        )
    form_teacher = relationship(
        "Teacher",
        back_populates="formClass",
        uselist=True
        )
    students = relationship(
        "Student",
        foreign_keys="[Student.classroom_id]",
        back_populates="classroom",
        uselist=True
        )
    examinations = relationship(
        "Examination",
        foreign_keys="[Examination.class_id]",
        back_populates="Class",
        uselist=True
        )

    def __init__(self, *args, **kwargs):
        """initializing class
        """        
        if kwargs:
            className = kwargs.pop("className", None)

        if className:
            className = className.upper()
            code = className.replace(" ", "-")
            yr = datetime.now().strftime("%y")
            kwargs["code"] = code + "-" + f"20{yr}-20{int(yr) + 1}"
            kwargs["className"] = className
            super().__init__(*args, **kwargs)

    def save(self):
        """class save method
        """        
        if not self.session:
            yr = datetime.now().strftime("%y")
            self.session = f"20{yr}/20{int(yr) + 1}"
        super().save()
        
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
        
        form_teacher = self.form_teacher
        if form_teacher is not None:
            new_dict["form_teacher"] = [
                {
                    "id": teacher.id,
                    "email": teacher.email,
                    "fullName": teacher.fullName
                } for teacher in form_teacher
            ]
        
        students = self.students
        if students is not None:
            end = 5 if len(students) > 5 else len(students)
            new_dict["students"] = {
                "number_of_students": len(students),
                "student": [{
                    "id": students[i].id,
                    "fullName": students[i].fullName
                } for i in range(end)]
            }
        
        exams = self.examinations
        if exams is not None:
            end = 5 if len(exams) > 5 else len(exams)
            new_dict["examinations"] = {
                "number_of_examinations": len(exams),
                "examinations": [{
                    "id": exams[i].id,
                    "code": exams[i].name,
                    "term": exams[i].term,
                    "session": exams[i].session
                } for i in range(end)]
            }
        
        courses = self.courses
        if courses is not None:
            end = 5 if len(courses) > 5 else len(courses)
            new_dict["courses"] = {
                "number_of_courses": len(courses),
                "courses": [{
                    "id": courses[i].id,
                    "code": courses[i].code,
                    "term": courses[i].term
                } for i in range(end)]
            }
        return new_dict
