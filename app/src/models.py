from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class CoreLogin(Base):
    __tablename__ = 'core_login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class TaskStatus(Base):
    __tablename__ = 'task_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(15), nullable=False)

class TaskPriority(Base):
    __tablename__ = 'task_priority'
    id = Column(Integer, primary_key=True, autoincrement=True)
    priority = Column(String(15), unique=True, nullable=False)

class CoreTask(Base):
    __tablename__ = 'core_task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    limit_ts = Column(TIMESTAMP, nullable=False)
    status = Column(Integer, ForeignKey('task_status.id'), nullable=False)
    owner_user = Column(Integer, ForeignKey('core_login.id'), nullable=False)
    priority = Column(Integer, ForeignKey('task_priority.id'), nullable=False)

    login_user = relationship("CoreLogin")
    task_status = relationship("TaskStatus")
    task_priority = relationship("TaskPriority")
