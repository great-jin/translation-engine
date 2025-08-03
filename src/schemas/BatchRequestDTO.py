from pydantic import BaseModel, conlist
from schemas.RequestDTO import RequestDTO

class BatchRequestDTO(BaseModel):
    requests: conlist(RequestDTO)
