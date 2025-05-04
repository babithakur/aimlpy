"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""

from sqlalchemy import Column, String, DateTime, func

from cacs456ml.repo.datasource import Base


class UserRecord(Base):
    __tablename__ = 'user'
    user_id = Column(String, primary_key=True)
    email = Column(String)
    name = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
