from pydantic import BaseModel, Field, field_validator
import re
from loguru import logger


class SignScheme(BaseModel):
    login: str = Field(max_length=30)
    password: str

    @field_validator("password", check_fields=False)
    def validate_password(cls, password):
        if not re.fullmatch(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#^()_+:><|\\/@$!%*?&])[A-Za-z\d#^()_+:><|\\/@$!%*?&]{8,}$",
                password):
            logger.info(f"incorrect password: {password}")
            raise ValueError('The password must contain 1 number,'
                             ' 1 lowercase and uppercase letter,'
                             ' 1 special character and be at least 8 characters long.')
        return password


class CreateTaskScheme(BaseModel):
    name: str = Field(max_length=71)


class UpdateTaskScheme(BaseModel):
    taskid: int
    mode: str = Field()

    @field_validator("mode", check_fields=False)
    def validate_mode(cls, mode):
        if not (mode == 'active' or mode == 'deleted' or mode == 'completed'):
            raise ValueError('Incorrect task status.'
                             ' Available statuses - completed, active, deleted')
        return mode
