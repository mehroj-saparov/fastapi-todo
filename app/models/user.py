from enum import Enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum as SQLEnum,
    DateTime,
)
from sqlalchemy.orm import relationship

from ..core.database import Base


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    user_id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=64), unique=True, nullable=False)
    password = Column(String(length=128), nullable=False)
    role = Column(SQLEnum(Role), default=Role.USER, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    tasks = relationship("Task", back_populates="user")

    def __str__(self):
        return self.username
