from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse

from database import get_db
from models import User
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

import json

from hashlib import sha256

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