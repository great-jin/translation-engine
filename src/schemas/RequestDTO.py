from typing import Optional
from pydantic import BaseModel
from tool.LanguageTool import LANG_CODE_MAP

class RequestDTO(BaseModel):
    quality: Optional[int] = None
    text: str
    targetType: str


    @staticmethod
    def validate_req(req):
        input_text = req.text
        if input_text is None or input_text.strip() == "":
            return "Text is blank"

        # 类型校验
        input_type = req.targetType
        if input_type is None or input_type.strip() == "":
            return "Type is blank"
        lan_type = LANG_CODE_MAP.get(req.targetType, None)
        if lan_type is None:
            return "Type not supported"

        # 合法返回空
        return None
