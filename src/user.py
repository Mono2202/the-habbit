from pydantic import BaseModel
from typing import List

class Habit(BaseModel):
    name: str
    frequency: str
    points: int

class User(BaseModel):
    id: int
    username: str
    join_date: str
    habits: List[Habit]
