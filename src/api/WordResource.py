import torch
from fastapi import APIRouter, HTTPException
from schemas.RequestDTO import RequestDTO
from schemas.ResponseDTO import ResponseDTO
from tool.LanguageTool import detect_lang, convert_type, reverse_type
from tool.ModelTool import model, tokenizer

# 导出接口
router = APIRouter()

# 接口服务
@router.post("/translate")
def translate(req: RequestDTO) -> ResponseDTO:
    sourceText = req.text
    # 检测输入语言
    sourceType = detect_lang(sourceText)

    # 语言类型转化校验
    targetType = convert_type(req.targetType)
    if not targetType or targetType not in tokenizer.lang_code_to_id:
        raise HTTPException(status_code = 400, detail = f"Unsupported target language: {targetType}")

    # 翻译内容
    tokenizer.src_lang = sourceType
    inputs = tokenizer(sourceText, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            forced_bos_token_id = tokenizer.convert_tokens_to_ids(targetType),
            max_length=256
        )
    # 解码输出
    result = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    # 返回结果
    return ResponseDTO(
        # 反转类型
        sourceType = reverse_type(sourceType),
        sourceText = sourceText,
        targetType = req.targetType,
        targetText = result
    )