from pydantic import BaseModel
from typing import List

# TODO: change module name

class Habit(BaseModel):
    name: str
    icon: str
    frequency: str
    points: int

class User(BaseModel):
    id: int
    username: str
    join_date: str
    habits: List[Habit]
