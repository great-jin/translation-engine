from pydantic import BaseModel

class RequestDTO(BaseModel):
    text: str
    target_lang: str
