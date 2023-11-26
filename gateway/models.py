from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, CheckConstraint

from database import engine
from sqlalchemy.orm import declarative_base, relationship, backref
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True)
    password_hash = Column(String(64))


class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    private = Column(Boolean)
    description = Column(String(1024))


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    space_id = Column(Integer, ForeignKey("spaces.id"))
    user_role = Column(String(5), nullable=False)


class PlayRequest(BaseModel):
    space_id: int
    song: str


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
