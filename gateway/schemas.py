from pydantic import BaseModel, ConfigDict, Field

class UserDto(BaseModel):
    username: str
    password: str

class SpaceDto(BaseModel):
    id: int = None
    name: str
    private: bool
    description: str

class SpaceIdDto(BaseModel):
    id: int