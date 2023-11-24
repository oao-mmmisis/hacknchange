from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse

from database import get_db
from models import User, Space, Permission
from schemas import UserDto, SpaceDto
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update

import json

from hashlib import sha256
import jwt

app = FastAPI()

@app.get("/")
async def get(session: Session = Depends(get_db)):
    return {'Hello', 'world'}

@app.post("/users/add/")
async def add_user(username: str, password: str, session: Session = Depends(get_db)):
    password_hash = sha256(password.encode('utf-8')).hexdigest()
    query = insert(User).values(username=username, password_hash=password_hash)
    session.execute(query)
    session.commit()

@app.get('/users/')
async def get_all_users(session: Session = Depends(get_db)):
    query = select(User)
    data = session.execute(query).scalars()
    return {'data': [i for i in data]}


@app.put('/space/add/')
async def add_space(space: SpaceDto, session: Session = Depends(get_db)):
    query = insert(Space).values(name=space.name, private=space.private, description=space.description)
    session.execute(query)
    session.commit()


@app.put('/space/reconfigure')
async def update_space(space: SpaceDto, session: Session = Depends(get_db)):
    query = update(Space).where(Space.id==space.id).values(name=space.name, private=space.private, description=space.description)
    session.execute(query)
    session.commit()

@app.get('/spaces/')
async def get_all_spaces(session: Session = Depends(get_db)):
    query = select(Space)
    data = session.execute(query).scalars()
    return {'data': [i for i in data]}



# @app.post("/auth/login/")
# async def add_user(user: UserDto, session: Session = Depends(get_db)):
#     # user_id = session.execute(select(User).filter(User.username==user.username)).first()
#     # print(user_id)
#     if session.execute(select(User).filter(User.username==user.username)).exist() is None:
#         print(user.username, user.password)
#         password_hash = sha256(user.password.encode('utf-8')).hexdigest()
#         query = insert(User).values(username=user.username, password_hash=password_hash)
#         result = session.execute(query)
        
#         session.commit()
#         return {'Info': result.inserted_primary_key}
#     print('check')

    # json_list = {'spaces': []}

    # for item in session.execute(select(Permission).join(Space, Space.b_id == Permission.id).filter(user_id=user_id)).scalars():
    #     print(item)
        # json_list['spaces'].append({'name': item.space})

    # json = {'spaces': [
    #     {
    #         'name': '',
    #         'id': '',
    #         'description': '',
    #     },
    #     ]
    # }

    # encoded_jwt = jwt.encode({"": "payload"}, "secret", algorithm="HS256")