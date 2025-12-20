from enum import Enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum as SQLEnum,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from ..core.database import Base


class Priority(int, Enum):
    PRIORITY01 = 1
    PRIORITY02 = 2
    PRIORITY03 = 3
    PRIORITY04 = 4
    PRIORITY05 = 5


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=64), nullable=False, unique=True)
    icon = Column(String(length=255), nullable=False, default='media/category-icons/default-icon.svg')
    color = Column(String(length=20), nullable=False, default='#ede7d5')

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    tasks = relationship('Task', back_populates='category')

    def __str__(self):
        return self.name
    

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=64), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    description = Column(String(length=255), nullable=True)
    due_date = Column(DateTime, nullable=False)
    priority = Column(SQLEnum(Priority), default=Priority.PRIORITY05, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    category = relationship('Category', back_populates='tasks')
    user = relationship('User', back_populates='tasks')
    sub_tasks = relationship('SubTask', back_populates='task')

    def __str__(self):
        return self.name


class SubTask(Base):
    __tablename__ = 'sub_tasks'

    sub_task_id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=64), nullable=False)
    description = Column(String(length=255), nullable=True)
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'))

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    task = relationship('Task', back_populates='sub_tasks')

    def __str__(self):
        return self.name


class Attechment(Base):
    __tablename__ = 'attechments'

    attechment_id = Column('id', Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(length=255), nullable=False)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return self.attechment_id