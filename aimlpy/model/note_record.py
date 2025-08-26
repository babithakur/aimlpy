from sqlalchemy import Column, Integer, String, DateTime, func

from aimlpy.repo.datasource import Base


class NoteRecord(Base):
    __tablename__ = 'note'
    note_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    text = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
