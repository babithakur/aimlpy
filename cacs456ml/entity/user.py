"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    name: str = None
    email: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
