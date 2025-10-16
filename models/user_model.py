import datetime
from typing import List, Optional
from venv import logger

import pytest
from pydantic import BaseModel, Field, model_validator, field_validator

from conftest import creation_user_data, test_user
from constants.roles import Roles


class UserModel(BaseModel):
    email: str = Field(..., description="Почта")
    fullName: str
    password: str = Field(..., min_length=8, description="Пароль")
    passwordRepeat: str = Field(..., min_length=8, description="Повтор пароля")
    roles: list[Roles] = Roles.USER
    verified: Optional[bool] = False
    banned: Optional[bool] = False

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Почта должна содержать знак @")
        return value

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


def test_creation_user_data_model(creation_user_data):
    user = UserModel(**{**creation_user_data, "email": "@testemail", "password": "asdasdasd33", "passwordRepeat":
        "asdasdas"})
    json_data = user.model_dump_json()
    logger.info(json_data)
    assert isinstance(user.fullName, str)


def test_test_user_model(test_user):
    user = UserModel(**test_user)
    json_data = user.model_dump_json(exclude_unset=True)
    logger.info(f"{json_data=}")

    assert isinstance(user.fullName, str)


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value
