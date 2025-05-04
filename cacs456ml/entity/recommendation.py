"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from pydantic import BaseModel


class Recommendation(BaseModel):
    user_id: str = None
    item_id: str = None
    score: float = None
    reason: str = None
