from pydantic import BaseModel


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
    

class PlayRequestDto(BaseModel):
    space_id: int
    song: str
