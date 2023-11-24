from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

from database import engine
from sqlalchemy.orm import declarative_base, relationship, backref

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
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
    # user = relationship(User, cascade="all,delete")
    user_role = Column(String(50))
    space_id = Column(Integer, ForeignKey("spaces.id"))
    # space = relationship(Space, cascade="all,delete")



Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)