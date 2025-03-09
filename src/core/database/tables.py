from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, declared_attr
from sqlalchemy import MetaData
from utils.camel_case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_case_to_snake_case(cls.__name__)


class TaskMode:
    ACTIVE = "active"
    COMPLETED = "completed"
    DELETED = "deleted"


class UserData(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    login = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("TaskList", back_populates="user")


class TaskList(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(BigInteger, ForeignKey('user_data.id', ondelete='CASCADE'))
    name = Column(String, nullable=False)
    mode = Column(String, nullable=False)

    user = relationship("UserData", back_populates="tasks")
