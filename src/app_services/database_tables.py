from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class TaskMode:
    ACTIVE = "active"
    COMPLETED = "completed"
    DELETED = "deleted"


class UserData(Base):
    __tablename__ = 'userdata'

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    login = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("TaskList", back_populates="user")


class TaskList(Base):
    __tablename__ = 'tasklist'

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(BigInteger, ForeignKey('userdata.id', ondelete='CASCADE'))
    name = Column(String, nullable=False)
    mode = Column(String, nullable=False)

    user = relationship("UserData", back_populates="tasks")
