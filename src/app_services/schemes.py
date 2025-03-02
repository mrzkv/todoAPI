from pydantic import BaseModel, Field


class SignScheme(BaseModel):
    login: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8, max_length=71)
