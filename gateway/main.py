from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Header
from fastapi.responses import HTMLResponse

from database import get_db
from models import User, Space, Permission
from schemas import UserDto, SpaceDto, SpaceIdDto
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete

import json
from typing import Annotated

from hashlib import sha256
import jwt

private_key = '''-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDKmLsOBl1vxsCP
GY44rqSmduIkfEnIap8//r8dkGv3qXnPMxuGGJK7dByRKhEQ41K38nnVwgqFUs55
H8zm7OnO+GzIEf1W4qjdVL22J8g5IU2QPXlmKktpap6/01B9PBXAQKMU4fMtbCVH
SDRit/226zsDY80oBS5TyVBfgmHD1ryTxlNUtq5CuRp61M9VZ5c1klG3BiXSR/Hb
KER5CM6ob9ZQWA2nd2SNNe5h4bBPvYLTppcocsLDVWzkYBRlow8DL+yvU57C38ia
GGlkokS0nICwu+2no30x/bovw4gEiPIFClGCOK6wEa6kLTr9nwn20A4Ds2ZdesW5
ZhIcoEA5AgMBAAECggEAF3PPr4NwHIja8JXKP2iEGdsIOaYDmoYxMiTIteDqhqxh
M+mcJY1Bqx55UhqXCCfwgue4T9TbB+z6hs32F8NUG4fpe82NUJoDZz+wiF4ZkPd4
dZqQK5H40dasUtNg7WZftDYnSrsPPfJXbGWA3u6imaKoXa+XZ6sV3lAfFDdRHuzP
eCTwDms33DSnhe3QYnm2/x2foxJdrGs3JnrAoMD0mE+iJoxhay3NCR8F/bJJlhPW
mUZm+XsvOOw4S7fP9HkPPXtjehYE0gKyenA0OEVRqH6ckTJW0oB79eCokCqcnP0R
XS2m+ZbfYpRC1K0zQd7Ye8MD3FqLvn+tgK/Uv0HKowKBgQDtxW8xDeEI5ErQ1tms
IblReOh4DH/OjDz/mS1Kiz11Z5afUS+OnCCHNxIAzl6AWT90S8ytQGNDdMpRZnCQ
Lau+u80IihTQeXDhbqtPANkXluqMo8y2f/0KLKvu6nAiiEIcmz7xBjJ459bA71Zp
qfVA1o1anVCxc9hCO0k5+2usBwKBgQDaIPL9yYiDqTlnIU/xXm5lSyCSDe9YLNKf
//JERFy06QnbusH7juZ9RP8PCwIJ+LSH3u2PrbYnHOQMsn0M7GVC/8bgYkWTHZCy
ugXXNL7EwGrNO/5qow8f+yiT2hkLGS5Ofu9CNTNPXKHM9bYSOzZNHNXnzx0bJ+mL
hz7+3XIhvwKBgQDpPWN1m0fEkS1S729Xiz1ezlw8ZwZ4dtjfYkMrfKstIBCA+ALO
whimiz79y3KoNOQqELEWwrKc2VQdxX9l72cqEs9uMQV5+6bffNBPD2Xl3gT3MTb/
T03JTUjbdN3LAh7YMPHtPUcFk2b2m9EIldAfalf/K5KcgCcD0WRjnF5iwQKBgCbg
0o6beiKFaf7QuC/8Nc8GGfMOWserjYsJEoRKbv+rvZ8VZXfR25EeWBu1SZK/amYB
PPRr8Nh91MPSmGlSRSYw8qCRw3baQS0p7NqTwyDMbvzPoaQeFhcMLApWSDprLY6+
HyT82H1ftFMUxHPxa9dIuXOMvdJWRdEhtP+2Np5/AoGAeeNwdq4WiI0IP2PFpXEA
XfGoThr+/X7B9gM5SohtLSiixqmL4S2NM5UjWntCDno9yMZNrstcxsAp9xDISpzd
+GSmuKRMoZCoNnS9rEbvfGM2NofMsM1kBYq9JRljdyOBLHvVfM8itLWcGE2NYma4
Pq8p5y7mnO+rP4gj2zZzBf8=
-----END PRIVATE KEY-----
'''
public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAypi7DgZdb8bAjxmOOK6k
pnbiJHxJyGqfP/6/HZBr96l5zzMbhhiSu3QckSoREONSt/J51cIKhVLOeR/M5uzp
zvhsyBH9VuKo3VS9tifIOSFNkD15ZipLaWqev9NQfTwVwECjFOHzLWwlR0g0Yrf9
tus7A2PNKAUuU8lQX4Jhw9a8k8ZTVLauQrkaetTPVWeXNZJRtwYl0kfx2yhEeQjO
qG/WUFgNp3dkjTXuYeGwT72C06aXKHLCw1Vs5GAUZaMPAy/sr1Oewt/ImhhpZKJE
tJyAsLvtp6N9Mf26L8OIBIjyBQpRgjiusBGupC06/Z8J9tAOA7NmXXrFuWYSHKBA
OQIDAQAB
-----END PUBLIC KEY-----
'''

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
async def add_space(space: SpaceDto, token: Annotated[list[str] | None, Header()] = None, session: Session = Depends(get_db)):
    decode_token = decode_jwt(token)
    print(decode_token)
    query = insert(Space).values(name=space.name, private=space.private, description=space.description)
    session.execute(query)
    session.commit()


@app.put('/space/reconfigure')
async def update_space(space: SpaceDto, token: Annotated[list[str] | None, Header()] = None, session: Session = Depends(get_db)):
    query = update(Space).where(Space.id==space.id).values(name=space.name, private=space.private, description=space.description)
    session.execute(query)
    session.commit()


@app.put('/space/invite')
async def space_invite(username: str, space_id: int, token: Annotated[list[str] | None, Header()] = None, session: Session = Depends(get_db)):
    user_id = session.execute(select(User.id).where(User.username==username)).scalar()
    query = insert(Permission).values(user_id=user_id, space_id=space_id, user_role="user")
    session.execute(query)
    session.commit()


@app.put('/space/connect')
async def space_connect(user_id: int, token: Annotated[list[str] | None, Header()] = None, session: Session = Depends(get_db)):
    pass


@app.delete('/space/delete/')
async def delete_space(space_id: int, token: Annotated[list[str] | None, Header()] = None, session: Session = Depends(get_db)):
    query = delete(Space).where(Space.id==space_id)
    session.execute(query)
    session.commit()


@app.delete('/space/leave/')
async def leave_space(space: SpaceIdDto, username: str, token: Annotated[list[str] | None, Header()] = None, session: Session = Depends(get_db)):
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
        if password_hash != sha256(user.password.encode('utf-8')).hexdigest():
            return {'Error': 'Password not correct'}

    json_list = {'spaces': []}
    token = {'username': user.username, 'spaces': []}

    for item in session.execute(select(Space).join(Permission, Space.id == Permission.space_id).where(Permission.user_id==user_id)).scalars():

        json_list['spaces'].append({'name': item.name, 'id': item.id, 'description': item.description})
        result = session.execute(select(Permission).where(Permission.space_id==item.id).where(Permission.user_id==user_id)).scalar()
        token['spaces'].append({'id': item.id, 'role': result.user_role})

    json_list['token'] = jwt.encode(token, private_key, algorithm="RS256")


    return json_list