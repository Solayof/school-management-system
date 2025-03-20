#!/usr/bin/python3
"""student model
"""
from sqlalchemy import Column, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from models.portal.association import student_courses_asso
from models.portal.admission import Admission


class Student(Admission):
    """student model
    
    Usage: student = Student(
            username="jesa",
            email="asd@gdha",
            admission_no="231",
            arm="A"
        )
        other parameters are optional

    Args:
        Admission (_type_): admission class
    """    
    __tablename__ = "students"
    extend_existing = True
    _id = Column(
        String(36),
        ForeignKey('admission_register._id'),
        primary_key=True
        )
    arm = Column(String(2), nullable=False)
    classroom_id = Column(String(36), ForeignKey("classes.id"))
    _attendance = Column(JSON())
    classroom = relationship(
        "Class",
        foreign_keys=[classroom_id],
        back_populates="students",
        uselist=False
        )
    courses = relationship(
        "Course",
        secondary=student_courses_asso,
        back_populates="students"
        )
    responses = relationship(
        "Response",
        foreign_keys="[Response.student_id]",
        back_populates="student",
        uselist=True
        )
    scores = relationship(
        "Score",
        foreign_keys="[Score.student_id]",
        back_populates="student",
        uselist=True
        )
    
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"))
    department = relationship(
        "Department",
        foreign_keys=[department_id],
        back_populates="students",
        uselist=False
    )
    

    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        new_dict.pop("responses", None)
        new_dict.pop("scores", None)
        new_dict.pop("_password", None)
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["dob"] = self.dob.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        new_dict['userType'] = "students"
        
        classroom = self.classroom
        new_dict["classroom_id"] = classroom.id if classroom else None
        
        courses = self.courses
        new_dict["number_of_courses"] = len(courses) if courses else 0
        
        class_admitted = self.class_admitted
        new_dict["class_admitted_id"] = class_admitted.id if class_admitted else None
        
        return new_dict
