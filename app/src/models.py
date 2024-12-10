from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class CoreLogin(Base):
    """
    Represents the user model

    Columns:
        - id: Numeric identifier code for the user. Constraints: Primary key, autoincrement
        - username: String identifier for the user. Constraints: 25 characters max, unique, not null
        - password: String password used for username login, used only in non-OAUTH users. Constraints: 255 characters max, not null
        - github_id: String Github ID associated with OAUTH users. Constraints: 50 characters max, unique, not null

    Methods:
        - set_password: Generates password hash to store in DB table
        - check_password: Checks user's input password hash against stored password hash
    """
    __tablename__ = 'core_login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    github_id = Column(String(50), unique=True, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class TaskStatus(Base):
    """
    Represents the user model

    Columns:
        - id: Numeric identifier code for the task status. Constraints: Primary key, autoincrement
        - status: String identifier for the task status. Constraints: 15 characters max, unique, not null
    """
    __tablename__ = 'task_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(15), unique=True, nullable=False)

class TaskPriority(Base):
    """
    Represents the priority model

    Columns:
        - id: Numeric identifier code for the task priority. Constraints: Primary key, autoincrement
        - priority: String identifier for the task priority. Constraints: 15 characters max, unique, not null
    """
    __tablename__ = 'task_priority'
    id = Column(Integer, primary_key=True, autoincrement=True)
    priority = Column(String(15), unique=True, nullable=False)

class CoreTask(Base):
    """
    Represents the task model

    Columns:
        - id: Numeric identifier code for the task. Constraints: Primary key, autoincrement
        - name: String identifier for the task. Constraints: 50 characters max, not null
        - description: Longer string description for the task. Constraints: 200 characters max
        - limit_ts: Deadline timestamp for the task's completion. Constraints: not null
        - status: Current status of the task. Constraints: Foreign key referencing task_status.id, not null
        - owner_user: User who created task. Constraints: Foreign key referencing core_login.id, not null
        - priority: Priority assigned by user for task. Constraints: Foreign key referencing task_priority.id, not null
    """
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