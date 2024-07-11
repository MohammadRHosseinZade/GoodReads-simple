from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=False)
    email: str = Field(index=True, nullable=False, unique=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now())
    is_admin: bool = Field(default=False,)
    