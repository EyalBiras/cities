from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    group: str | None = None
    disabled: bool = False

    def __hash__(self):
        return hash(self.username)


class UserInDB(User):
    hashed_password: str


class Group(BaseModel):
    name: str
    members: list[str]
    owner: str
    join_requests: list[str]

    def __hash__(self):
        return hash(self.name)
