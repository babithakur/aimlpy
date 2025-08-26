from typing import Optional

from pydantic import BaseModel


class Note(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    text: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
