from pydantic import BaseModel, Field
from services.database_tables import TaskMode


class SignScheme(BaseModel):
    login: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8, max_length=71)


class CreateTaskScheme(BaseModel):
    name: str = Field(max_length=71)


class UpdateTaskScheme(BaseModel):
    taskid: int
    mode: str
