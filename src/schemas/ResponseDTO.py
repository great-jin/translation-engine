from pydantic import BaseModel
from tool.LanguageTool import reverse_type

class ResponseDTO(BaseModel):
    success: bool
    errorMsg: str
    sourceType: str
    sourceText: str
    targetType: str
    targetText: str


    @staticmethod
    def res_origin(lan_text, lan_type):
        return ResponseDTO(
            success = True,
            errorMsg = "",
            sourceType = lan_type,
            sourceText = lan_text,
            targetType = lan_type,
            targetText = lan_text
        )

    @staticmethod
    def res_success(source_type, source_text, target_type, target_text):
        return ResponseDTO(
            success = True,
            errorMsg = "",
            sourceType = reverse_type(source_type),
            sourceText = source_text,
            targetType = target_type,
            targetText = target_text
        )

    @staticmethod
    def res_fail(message, source_text, target_type):
        return ResponseDTO(
            success = False,
            errorMsg = message,
            sourceType = "",
            sourceText = source_text,
            targetType = target_type,
            targetText = ""
        )