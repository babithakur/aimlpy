from typing import Optional, List

from pydantic import BaseModel

from aimlpy.entity.common import BaseResponse
from aimlpy.entity.note import Note


class CreateNoteRequest(BaseModel):
    user_id: int
    text: str


class UpdateNoteRequest(BaseModel):
    note_id: int
    text: str


class NoteResponse(BaseResponse):
    note: Optional[Note] = None
    notes: Optional[List[Note]] = None
