from sqlalchemy import Column, ForeignKey, Integer, String

from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    password_hash = Column(String(64))


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1024))


class RoomPermissions(Base):
    __tablename__ = "roompermissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_role = Column(String(50))
    room_id = Column(Integer, ForeignKey("rooms.id"))

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)