from sqlalchemy import Column, Integer, String, ForeignKey
from cacs456ml.repo.datasource import Base

class UserNotes(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    text = Column(String)




