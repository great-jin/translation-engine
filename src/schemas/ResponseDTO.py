from pydantic import BaseModel

class ResponseDTO(BaseModel):
    source_type: str
    source_text: str
    target_type: str
    target_text: str
