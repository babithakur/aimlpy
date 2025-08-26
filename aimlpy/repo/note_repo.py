from typing import List

from aimlpy.model.note_record import NoteRecord
from aimlpy.repo.datasource import DataSource
from aimlpy.util import loggerutil


class NoteRepo:
    def __init__(self, db: DataSource):
        self.db = db
        self.logger = loggerutil.get_logger(__name__)

    def create(self, text: str, user_id: int) -> NoteRecord:
        with self.db.get_session() as session:
            try:
                note = NoteRecord(text=text, user_id=user_id)
                session.add(note)
                session.commit()
                session.refresh(note)
                return note

            except Exception as e:
                session.rollback()
                self.logger.error(f"Error creating note: {e}")
                raise

    def get_by_user_id(self, user_id: int) -> List[NoteRecord]:
        with self.db.get_session() as session:

            try:
                notes = session.query(NoteRecord).filter(NoteRecord.user_id == user_id).all()
                return notes

            except Exception as e:
                self.logger.error(f"Error fetching notes for user_id={user_id}: {e}")
                raise

    def update(self, note_id: int, text: str) -> NoteRecord:
        with self.db.get_session() as session:

            try:
                note = session.query(NoteRecord).filter(NoteRecord.note_id == note_id).first()

                if not note:
                    raise Exception(f"Note with id {note_id} not found")

                note.text = text
                session.commit()
                session.refresh(note)
                return note

            except Exception as e:
                session.rollback()
                self.logger.error(f"Error updating note id={note_id}: {e}")
                raise

    def delete(self, note_id: int) -> bool:
        with self.db.get_session() as session:

            try:
                note = session.query(NoteRecord).filter(NoteRecord.note_id == note_id).first()

                if not note:
                    raise Exception(f"Note with id {note_id} not found")

                session.delete(note)
                session.commit()
                return True

            except Exception as e:
                session.rollback()
                self.logger.error(f"Error deleting note id={note_id}: {e}")
                raise
