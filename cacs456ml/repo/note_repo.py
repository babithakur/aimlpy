from typing import List
from cacs456ml.model.user_notes import UserNotes
from cacs456ml.repo.datasource import DataSource
from cacs456ml.util import loggerutil

class NoteRepo:
    def __init__(self, db: DataSource):
        self.db = db
        self.logger = loggerutil.get_logger(__name__)


    def create(self, text: str, user_id: int) -> UserNotes:
        with self.db.get_session() as session:
            try:
                note = UserNotes(text=text, user_id=user_id)
                session.add(note)
                session.commit()
                session.refresh(note)
                return note
            
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error creating note: {e}")
                raise
     
    
    def get_by_user_id(self, user_id: int) -> List[UserNotes]:
        with self.db.get_session() as session:

            try:
                notes = session.query(UserNotes).filter(UserNotes.user_id == user_id).all()
                return notes
            
            except Exception as e:
                self.logger.error(f"Error fetching notes for user_id={user_id}: {e}")
                raise


    def update(self, note_id: int, text: str) -> UserNotes:
        with self.db.get_session() as session:

            try:
                note = session.query(UserNotes).filter(UserNotes.id == note_id).first()

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
                note = session.query(UserNotes).filter(UserNotes.id == note_id).first()

                if not note:
                    raise Exception(f"Note with id {note_id} not found")
                
                session.delete(note)
                session.commit()
                return True
            
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error deleting note id={note_id}: {e}")
                raise
