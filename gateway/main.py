import subprocess
from hashlib import sha256
from typing import Annotated

from fastapi import FastAPI, Depends, Header
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

from database import get_db
from models import User, Space, Permission
from schemas import UserDto, SpaceDto, SpaceIdDto, PlayRequestDto

#
# def decode_jwt(token):
#     return jwt.decode(token, private_key, algorithms=["RS256"])


secret = []

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


@app.post("/users/add")
async def add_user(username: str, password: str, session: Session = Depends(get_db)):
    password_hash = sha256(password.encode('utf-8')).hexdigest()
    query = insert(User).values(username=username, password_hash=password_hash)
    session.execute(query)
    session.commit()


@app.get('/users')
async def get_all_users(session: Session = Depends(get_db)):
    query = select(User)
    data = session.execute(query).scalars()
    return {'data': [i for i in data]}


@app.post('/space/add')
async def add_space(space: SpaceDto, token: Annotated[list[str] | None, Header()] = None,
                    session: Session = Depends(get_db)):
    # decode_token = decode_jwt(token)
    # print(decode_token)
    query = insert(Space).values(name=space.name, private=space.private, description=space.description)
    session.execute(query)
    session.commit()


@app.post('/space/reconfigure')
async def update_space(space: SpaceDto, token: Annotated[list[str] | None, Header()] = None,
                       session: Session = Depends(get_db)):
    query = update(Space).where(Space.id == space.id).values(name=space.name, private=space.private,
                                                             description=space.description)
    session.execute(query)
    session.commit()


@app.post('/space/invite')
async def space_invite(username: str, space_id: int, token: Annotated[list[str] | None, Header()] = None,
                       session: Session = Depends(get_db)):
    user_id = session.execute(select(User.id).where(User.username == username)).scalar()
    query = insert(Permission).values(user_id=user_id, space_id=space_id, user_role="user")
    session.execute(query)
    session.commit()


@app.post('/space/connect')
async def space_connect(user_id: int, token: Annotated[list[str] | None, Header()] = None,
                        session: Session = Depends(get_db)):
    pass


@app.post('/space/delete')
async def delete_space(space_id: int, token: Annotated[list[str] | None, Header()] = None,
                       session: Session = Depends(get_db)):
    query = delete(Space).where(Space.id == space_id)
    session.execute(query)
    session.commit()


@app.post('/space/leave')
async def leave_space(space: SpaceIdDto, username: str, token: Annotated[list[str] | None, Header()] = None,
                      session: Session = Depends(get_db)):
    query = select(User.id).where(User.username == username)
    user_id = session.execute(query).first()

    query = delete(Permission).where(Permission.space_id == space.id).where(Permission.user_id == user_id)
    session.execute(query)
    session.commit()


@app.get('/spaces')
async def get_all_spaces(session: Session = Depends(get_db)):
    query = select(Space)
    data = session.execute(query).scalars()
    return {'data': [i for i in data]}


@app.post("/auth/login")
async def add_user(user: UserDto, session: Session = Depends(get_db)):
    user_id = session.execute(select(User.id).filter(User.username == user.username)).scalar()
    if user_id is None:
        print('check')
        password_hash = sha256(user.password.encode('utf-8')).hexdigest()
        query = insert(User).values(username=user.username, password_hash=password_hash)
        result = session.execute(query)
        session.commit()
        user_id = result.inserted_primary_key
    else:
        password_hash = session.execute(select(User.password_hash).filter(User.username == user.username)).scalar()
        if password_hash != sha256(user.password.encode('utf-8')).hexdigest():
            return {'Error': 'Password not correct'}

    json_list = {'spaces': []}
    token = {'username': user.username, 'spaces': []}

    for item in session.execute(select(Space).join(Permission, Space.id == Permission.space_id).where(
            Permission.user_id == user_id)).scalars():
        json_list['spaces'].append({'name': item.name, 'id': item.id, 'description': item.description})
        result = session.execute(
            select(Permission).where(Permission.space_id == item.id).where(Permission.user_id == user_id)).scalar()
        token['spaces'].append({'id': item.id, 'role': result.user_role})

    # json_list['token'] = jwt.encode(token, private_key, algorithm="RS256")
    json_list['token'] = "mock"

    return json_list


@app.post("/play")
async def play(play_request: PlayRequestDto, session: Session = Depends(get_db)):
    process = subprocess.Popen([f"liquidsoap 'settings.init.allow_root.set(true)\noutput.icecast(%vorbis, host=\"icecast2\", port=8000, password=\"chael7Ai\", mount=\"/audio/{play_request.space_id}\", single(\"/music/{play_request.song}.ogg\"))'"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
