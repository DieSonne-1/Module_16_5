from fastapi import FastAPI, Path, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


users.append(User(id=1, username="UrbanUser", age=24))
users.append(User(id=2, username="UrbanTest", age=22))
users.append(User(id=3, username="Capybara", age=60))


@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get(path='/user/{user_id}')
def get_users(request: Request, user_id: int) -> HTMLResponse:
    for user in users:
        if int(user.id) == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
        raise HTTPException(status_code=404, detail="User not found")


@app.post('/user/{username}/{age}')
def post_users(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=100, description='Enter User ID', example=28)]) -> User:
    user_id = 1 if not users else users[-1].id + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example=1)],
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanProfi')],
        age: Annotated[int, Path(ge=18, le=100, description='Enter User ID', example=28)]) -> User:
    try:
        user = next(user for user in users if user.id == user_id)
        user.username = username
        user.age = age
        return user
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
def delete_user(user_id: int = Path(ge=1, le=100, description='Enter User ID', example=2)) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail='User was not found')
