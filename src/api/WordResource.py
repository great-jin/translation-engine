import torch
from fastapi import APIRouter, HTTPException
from schemas.RequestDTO import RequestDTO
from schemas.ResponseDTO import ResponseDTO
from tool.LanguageTool import detect_lang, convert_type, reverse_type
from tool.ModelTool import model, tokenizer

# 导出接口
router = APIRouter()

# 接口服务
@router.post("/nllb/translate")
def translate(req: RequestDTO) -> ResponseDTO:
    source_text = req.text
    # 检测输入语言
    source_type = detect_lang(source_text)

    # 语言类型校验
    target_type = convert_type(req.targetType)
    if not target_type or target_type not in tokenizer.lang_code_to_id:
        raise HTTPException(status_code = 400, detail = f"Unsupported target language: {target_type}")

    # 语言类型一致直接返回
    if source_type == target_type:
         return ResponseDTO(
            sourceType = req.targetType,
            sourceText = source_text,
            targetType = req.targetType,
            targetText = source_text
        )

    # 翻译内容
    tokenizer.src_lang = source_type
    inputs = tokenizer(source_text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_type),
            max_length=256
        )
    # 解码输出
    result = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    # 返回结果
    return ResponseDTO(
        # 反转类型
        sourceType = reverse_type(source_type),
        sourceText = source_text,
        targetType = req.targetType,
        targetText = result
    )