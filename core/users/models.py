# core/users/models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, func, DateTime
from core.db import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    password = Column(String, nullable=False)
    
    is_active = Column(Boolean, default=True)
    
    create_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    
    # any user can has many tasks on-to-many
    tasks = relationship("TaskModel", back_populates="users")
    
    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)
    
    def set_password(self, plain_text:str) -> None:
        self.password = self.hash_password(plain_text) 