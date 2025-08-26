from typing import List

from aimlpy.entity.note import Note
from aimlpy.repo.note_repo import NoteRepo


class NoteService:
    def __init__(self, note_repo: NoteRepo):
        self.note_repo = note_repo

    def create_note(self, text: str, user_id: int) -> Note:
        try:

            note = self.note_repo.create(text, user_id)
            return note

        except Exception as e:
            raise Exception(f"Failed to create note: {str(e)}")

    def get_notes_by_user(self, user_id: int) -> List[Note]:
        try:
            notes = self.note_repo.get_by_user_id(user_id)
            return notes

        except Exception as e:
            raise Exception(f"Failed to fetch notes: {str(e)}")

    def update_note(self, note_id: int, text: str) -> Note:
        try:
            note = self.note_repo.update(note_id, text)
            return note

        except Exception as e:
            raise Exception(f"Failed to update note: {str(e)}")

    def delete_note(self, note_id: int) -> bool:
        try:
            return self.note_repo.delete(note_id)
        except Exception as e:
            raise Exception(f"Failed to delete note: {str(e)}")
