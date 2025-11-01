from typing import Optional
from pydantic import BaseModel

class ResponseDTO(BaseModel):
    success: bool
    errorMsg: Optional[str] = None
    sourceText: Optional[str] = None
    targetText: Optional[str] = None


    @staticmethod
    def res_origin(lan_text):
        return ResponseDTO(
            success = True,
            errorMsg = "",
            sourceText = lan_text,
            targetText = lan_text
        )

    @staticmethod
    def res_success(source_text, target_text):
        return ResponseDTO(
            success = True,
            errorMsg = "",
            sourceText = source_text,
            targetText = target_text
        )

    @staticmethod
    def res_fail(message, source_text):
        return ResponseDTO(
            success = False,
            errorMsg = message,
            sourceText = source_text,
            targetText = ""
        )
