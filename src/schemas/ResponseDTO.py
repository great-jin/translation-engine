from pydantic import BaseModel

class ResponseDTO(BaseModel):
    sourceType: str
    sourceText: str
    targetType: str
    targetText: str
