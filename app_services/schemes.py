from pydantic import BaseModel


class UserSign(BaseModel):
    login: str
    password: str

