from pydantic import BaseModel, EmailStr, Field, ConfigDict
# from decimal import Decimal
from datetime import datetime
# from typing import Literal, List
from datetime import datetime
# from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
