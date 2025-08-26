# core/tasks/models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, func, DateTime, ForeignKey
from core.db import Base
from sqlalchemy.orm import relationship

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title= Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    
    create_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # any task has one user
    users = relationship("UserModel", back_populates="tasks", uselist=False)