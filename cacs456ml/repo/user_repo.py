"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from cacs456ml.entity.user import User
from cacs456ml.model.user_record import UserRecord
from cacs456ml.repo.datasource import DataSource
from cacs456ml.util import loggerutil, uuidutil


class UserRepo:
    def __init__(self, db: DataSource):
        self.db = db
        self.logger = loggerutil.get_logger(__name__)

    def create_user(self, user: User):
        self.logger.debug(f"Creating user: {user}")
        with self.db.get_session() as session:
            try:
                u = UserRecord(
                    user_id=uuidutil.generate_uuid(),
                    email=user.email,
                    name=user.name,
                    address=user.address,
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error creating user: {e}")
                raise e
