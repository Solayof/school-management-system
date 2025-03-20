#!/usr/bin/python3
"""parent class
"""
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.portal.course import Course
from models.portal.user import User
from models.portal.usermodel import UserModel


class Parent(User):
    """parent model
    Usage: parent = Parent()
           all the parameters are optional

    Args:
        User (_type_): user model class
    """        
    __tablename__ = "parents"
    extend_existing = True
    _id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    occupation = Column(String(24))
    children = relationship(
        "Admission",
        foreign_keys="[Admission.parent_id]",
        back_populates="parent",
        uselist=True
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
        new_dict['userType'] = "parents"
        
        children = self.children
        if children is not None:
            length = 2  if len(children) > 2 else len(children)
            new_dict["children"] = {
                "number_of_children": len(children),
                "children": [{
                    "id": children[i].id,
                    "fullName": children[i].fullName,
                    "username": children[i].username,
                    "email": children[i].email
                } for i in range(length)]
            }
    
        return new_dict

