from pydantic import BaseModel

class RequestDTO(BaseModel):
    text: str
    targetType: str
