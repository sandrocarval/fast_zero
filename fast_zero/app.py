from http import HTTPStatus
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    DBUserSchema,
    SubmitUserSchema,
    UserListSchema,
    UserSchema,
)

app = FastAPI()

database = {}


@app.get("/")
def get_root():
    return {"message": "Olá, mundo!"}


@app.post("/users", status_code=HTTPStatus.CREATED, response_model=UserSchema)
def create_user(payload: SubmitUserSchema):
    new_user = DBUserSchema(**payload.model_dump(exclude_unset=True))
    new_user_id = uuid4()
    database[new_user_id] = new_user

    return UserSchema(id=new_user_id, **new_user.model_dump())


@app.get("/users", status_code=HTTPStatus.OK, response_model=UserListSchema)
def read_users():
    return {
        "users": [
            UserSchema(id=k, **database[k].model_dump())
            for k in database.keys()
        ]
    }


@app.get("/users/{id}", status_code=HTTPStatus.OK)
def read_user(id: UUID):
    if id not in database.keys():
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found.")

    return UserSchema(id=id, **database[id].model_dump())


@app.put("/users/{id}", status_code=HTTPStatus.OK)
def update_user(id: UUID, payload: SubmitUserSchema):
    if id not in database.keys():
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found.")

    database[id] = payload
    return UserSchema(id=id, **payload.model_dump())
