from sqlalchemy import Column, Integer, String, DateTime, Float, func
from sqlalchemy.dialects.postgresql import ARRAY

from aimlpy.repo.datasource import Base  


class PDFDocument(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String)
    keywords = Column(ARRAY(String))
    summary = Column(String)
    filename = Column(String)
    embedding = Column(ARRAY(Float), nullable=True)

    created_at = Column(DateTime, default=func.now())
