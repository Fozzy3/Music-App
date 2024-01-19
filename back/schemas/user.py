from typing import Optional, Union
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None  # Proporciona un valor por defecto
    name: str
    email: str
    password: str
