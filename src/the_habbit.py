from pydantic import BaseModel
from typing import List

class Habit(BaseModel):
    name: str
    icon: str
    steps: int # Minus to break a habit
    unit: str
    frequency: str
    points: int

class User(BaseModel):
    id: int
    username: str
    join_date: str
    habits: List[Habit]
