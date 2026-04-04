from fastapi import FastAPI

from pydantic import BaseModel, Field, EmailStr, ConfigDict

app = FastAPI()

data = {
    'email': 'abc@mail.ru',
    'bio': 'УДАААА',
    'age': 10,
}

# data_without_age = {
#     'email': 'abc@mail.ru',
#     'bio': 'test',
#     # 'gender': 'male',
#     # 'birthday': '2002-12-12'
# }

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)
    model_config = ConfigDict(extra='forbid')


users = []


@app.post('/users')
def add_user(user: UserSchema):
    users.append(user)
    return {'ok': True, 'msg': 'Юзер добавлен'}


@app.get('/users')
def get_users() -> list[UserSchema]:
    return users


#
# class UserAgeSchema(UserSchema):
#     age: int = Field(ge=0, le=130)
#
# print(repr(UserAgeSchema(**data)))
# print(repr(UserSchema(**data_without_age)))
