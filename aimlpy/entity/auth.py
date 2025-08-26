"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from aimlpy.entity.user import User


class Session(BaseModel):
    session_id: str = None
    user_id: str = None
    token: str = None
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    ttl: int = 0
    user: Optional[User] = None
