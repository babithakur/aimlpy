from fastapi import APIRouter, HTTPException
from cacs456ml.service.note_service import NoteService, get_note_service
from cacs456ml.entity.note_schemas import NoteResponse, CreateNoteRequest, UpdateNoteRequest

router = APIRouter()
service: NoteService = get_note_service()


@router.post("/notes", response_model=NoteResponse)
def create_note(request: CreateNoteRequest):
    try:
        note = service.create_note(request.text, request.user_id)
        return NoteResponse(note=note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notes/{user_id}", response_model=NoteResponse)
def get_notes(user_id: int):
    try:
        notes = service.get_notes_by_user(user_id)
        return NoteResponse(notes=notes)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/note/{note_id}", response_model=NoteResponse)
def update_note( request: UpdateNoteRequest):
    try:
        updated_note = service.update_note(request.text)
        return NoteResponse(note=updated_note)
    
    except Exception as e:
        print(e)
        return NoteResponse(error=True, error_code=ErrorCode.EXCEPTION, message=str(e))



@router.delete("/note/{note_id}", status_code=204)
def delete_note(note_id: int):
    try:
        success = service.delete_note(note_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
