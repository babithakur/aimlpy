from typing import Optional, List
from pydantic import BaseModel
from cacs456ml.entity.common import BaseResponse


class NoteBase(BaseModel):
    id: int
    user_id: int
    text: str

    model_config = {
        "from_attributes": True  
    }


class CreateNoteRequest(BaseModel):
    text: str
    user_id: int


class UpdateNoteRequest(BaseModel):
    id: int
    text: str


class NoteResponse(BaseResponse):
    note: Optional[NoteBase] = None
    notes: Optional[List[NoteBase]] = None
