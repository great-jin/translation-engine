from typing import Optional
from pydantic import BaseModel

class BatchRequestDTO(BaseModel):
    quality: Optional[int] = None
    sourceType: Optional[str] = None
    targetType: str
    textList: list[str]
