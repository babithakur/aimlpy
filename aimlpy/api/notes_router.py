from fastapi import APIRouter, HTTPException

from aimlpy.entity.common import ErrorCode
from aimlpy.entity.note_reqres import NoteResponse, CreateNoteRequest, UpdateNoteRequest
from aimlpy.repo.datasource import DataSource
from aimlpy.repo.note_repo import NoteRepo
from aimlpy.service.note_service import NoteService

router = APIRouter()
db = DataSource()
note_repo = NoteRepo(db=db)
service: NoteService = NoteService(note_repo=note_repo)


@router.post("/note", response_model=NoteResponse)
def create_note(request: CreateNoteRequest):
    try:
        note = service.create_note(request.text, request.user_id)
        return NoteResponse(note=note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/note/{user_id}", response_model=NoteResponse)
def get_notes(user_id: int):
    try:
        notes = service.get_notes_by_user(user_id)
        return NoteResponse(notes=notes)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/note/{note_id}", response_model=NoteResponse)
def update_note(request: UpdateNoteRequest):
    try:
        updated_note = service.update_note(request.note_id, request.text)
        return NoteResponse(note=updated_note)

    except Exception as e:
        print(e)
        return NoteResponse(error=True, error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))


@router.delete("/note/{note_id}", status_code=204)
def delete_note(note_id: int):
    try:
        success = service.delete_note(note_id)
        if not success:
            return NoteResponse(error=True, error_code=ErrorCode.NOT_FOUND, message="Note not found")
    except Exception as e:
        return NoteResponse(error=True, error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))
