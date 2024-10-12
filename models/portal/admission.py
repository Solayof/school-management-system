#!/usr/bin/python3
"""admission model
"""
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.portal.user import User


class Admission(User):
    """admission model

    Args:
        User (User): User class
    """    
    __tablename__ = "admission_register"
    extend_existing = True
    _id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    admission_no = Column(String(5), unique=True, nullable=False)
    previous_school = Column(String(128))
    class_at_previous_school = Column(String(8))
    Class_id = Column(String(36), ForeignKey("classes.id"))
    class_admitted = relationship(
        "Class",
        foreign_keys=[Class_id],
        back_populates="admitted_students"
        )
    parent_id = Column(String(36), ForeignKey("parents._id"))
    parent = relationship(
        "Parent",
        foreign_keys=[parent_id],
        back_populates="children"
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
        
        class_admitted = self.class_admitted
        if class_admitted is not None:
            new_dict["class_admitted"] = [
                {
                    "id": class_admitted.id,
                    "code": class_admitted.code
                }
            ]
        
        parent = self.parent
        if parent is not None:
            new_dict["parent"] = [
                {
                    "id": parent.id,
                    "fullName": parent.fullName,
                    "phoneNumber": parent.phone_number,
                    "email": parent.email
                }
            ]
        return new_dict
