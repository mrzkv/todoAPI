from sqlalchemy import String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()

class UserData(Base):
    __tablename__ = 'userdata'
    id = mapped_column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    login = mapped_column(String, nullable=False, unique=True)
    hashed_password = mapped_column(String, nullable=False)

