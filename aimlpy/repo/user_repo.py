"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from aimlpy.entity.user import User
from aimlpy.model.user_record import UserRecord
from aimlpy.repo.datasource import DataSource
from aimlpy.util import loggerutil


class UserRepo:
    def __init__(self, db: DataSource):
        self.db = db
        self.logger = loggerutil.get_logger(__name__)

    def create_user(self, user: User):
        self.logger.debug(f"Creating user: {user}")
        with self.db.get_session() as session:
            try:
                u = UserRecord(
                    email=user.email,
                    name=user.name,
                    address=user.address,
                )
                session.add(u)
                session.commit()
                session.refresh(u)
                return u
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error creating user: {e}")
                raise e
