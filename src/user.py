from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    join_date: str
