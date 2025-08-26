"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""

from sqlalchemy import Column, String, DateTime, func, Integer

from aimlpy.repo.datasource import Base


class UserRecord(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String)
    name = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
