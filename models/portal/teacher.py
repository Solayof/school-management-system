#!/usr/bin/python3
"""teacher class
"""
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.portal.association import course_teacher_asso
from models.portal.user import User
from models.portal.Class import Class
from models.portal.course import Course


class Teacher(User):
    """teacher model

    Args:
        User (_type_): user class
    """    
    __tablename__ = "teachers"
    extend_existing = True
    _id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    staff_id = Column(String(16))
    file_no = Column(String(16))
    grade_level = Column(String(4))
    previous_school = Column(String(64))
    date_transfer = Column(DateTime)
    last_promote_date = Column(DateTime)
    course_teach = relationship(
        'Course',
        secondary=course_teacher_asso,
        back_populates="teachers"
        )
    form_class_id = Column(String(36), ForeignKey("classes.id"))
    formClass = relationship(
        "Class",
        foreign_keys=[form_class_id],
        back_populates="form_teacher"
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
        new_dict["dob"] = self.dob.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        
        formclass = self.formClass
        if formclass is not None:
            new_dict["formclass"] = [
                {
                    "id": formclass.id,
                    "code": formclass.code
                }
            ]
        
        courses = self.course_teach
        if courses is not None:
            new_dict["course_teach"] = [
                {
                    "id": course.id,
                    "code": course.code,
                    "term": course.term
                } for course in courses
            ]
        return new_dict

    def course_teach_paginate(self, page=1, per_page=10):
        if per_page == 0  or page == 0:
            return None
        offset = (page - 1) * per_page
        length = len(self.course_teach)
        if offset >= length:
            return None
        remain = length - offset
        end = offset + per_page if remain >= per_page else offset + remain
        nxt_page = page + 1 if page * per_page < length else 1
        courses = {
            
              "page": page,
              "total": len(self.course_teach),
              "next_page": nxt_page
            ,

            "courses": [{
            self.course_teach[i].to_dict()
            } for i in  range(offset, end)]
        }
        return courses
