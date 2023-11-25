from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse

from database import get_db
from models import User, Space, Permission
from schemas import UserDto, SpaceDto, SpaceIdDto
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete

import json

from hashlib import sha256
import jwt

app = FastAPI()

@app.get("/")
async def init(session: Session = Depends(get_db)):
    session.execute(insert(User).values(username='Alex', password_hash=sha256('123'.encode('utf-8')).hexdigest()))
    session.commit()
    session.execute(insert(Space).values(name='space', private=True, description='Hell'))
    session.commit()
    session.execute(insert(Space).values(name='space2', private=True, description='Hello'))
    session.commit()
    session.execute(insert(Space).values(name='space3', private=False, description='Hello, all'))
    session.commit()
    session.execute(insert(Permission).values(user_id=1, space_id=1, user_role="user"))
    session.commit()
    session.execute(insert(Permission).values(user_id=1, space_id=2, user_role="user"))
    session.commit()




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


@app.put('/space/invite')
async def space_invite(username: str, space_id: int, session: Session = Depends(get_db)):
    user_id = session.execute(select(User.id).where(User.username==username)).scalar()
    query = insert(Permission).values(user_id=user_id, space_id=space_id, user_role="user")
    session.execute(query)
    session.commit()

@app.put('/space/connect')
async def space_connect(user_id: int, session: Session = Depends(get_db)):
    pass


@app.delete('/space/delete/')
async def delete_space(space_id: int, session: Session = Depends(get_db)):
    query = delete(Space).where(Space.id==space_id)
    session.execute(query)
    session.commit()


@app.delete('/space/leave/')
async def leave_space(space: SpaceIdDto, username: str, session: Session = Depends(get_db)):
    query = select(User.id).where(User.username==username)
    user_id = session.execute(query).first()

    query = delete(Permission).where(Permission.space_id==space.id).where(Permission.user_id==user_id)
    session.execute(query)
    session.commit()


@app.get('/spaces/')
async def get_all_spaces(session: Session = Depends(get_db)):
    query = select(Space)
    data = session.execute(query).scalars()
    return {'data': [i for i in data]}



@app.post("/auth/login/")
async def add_user(user: UserDto, session: Session = Depends(get_db)):
    user_id = session.execute(select(User.id).filter(User.username==user.username)).scalar()
    if user_id is None:
        print('check')
        password_hash = sha256(user.password.encode('utf-8')).hexdigest()
        query = insert(User).values(username=user.username, password_hash=password_hash)
        result = session.execute(query)
        session.commit()
        user_id = result.inserted_primary_key
    else:
        password_hash = session.execute(select(User.password_hash).filter(User.username==user.username)).scalar()
        print(password_hash, sha256(user.password.encode('utf-8')).hexdigest())
        if password_hash != sha256(user.password.encode('utf-8')).hexdigest():
            return {'Error': 'Password not correct'}

    json_list = {'spaces': []}
    token = {'username': user.username, 'spaces': []}

    for item in session.execute(select(Space).join(Permission, Space.id == Permission.space_id).where((Permission.user_id==user_id) | (Space.private==False))).scalars():                             
        print(item)
        json_list['spaces'].append({'name': item.name, 'id': item.id, 'description': item.description})
        token['spaces'].append({'id': item.id})

    json_list['token'] = jwt.encode(token, "secret", algorithm="HS256")


    return json_list