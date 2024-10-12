
from sqlalchemy import Column, ForeignKey, String
from models.base import Base
from models.baseModel import BaseModel


class Session(BaseModel, Base):
    __tablename__ = "sessions"
    user_id = Column(
        String(36),
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
