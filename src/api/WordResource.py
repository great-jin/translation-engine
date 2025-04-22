import torch
from fastapi import APIRouter, HTTPException
from schemas.RequestDTO import RequestDTO
from schemas.ResponseDTO import ResponseDTO
from tool.LanguageTool import detectLang
from tool.ModelTool import model, tokenizer

# 导出接口
router = APIRouter()

# 接口服务
@router.post("/translate")
def translate(req: RequestDTO) -> ResponseDTO:
    src_text = req.text
    tgt_lang = req.target_lang

    # 检测输入语言类型
    src_lang = detectLang(src_text)

    # 类型合法校验
    if not tgt_lang or tgt_lang not in tokenizer.lang_code_to_id:
        raise HTTPException(status_code = 400, detail = f"Unsupported target language: {tgt_lang}")

    tokenizer.src_lang = src_lang
    inputs = tokenizer(src_text, return_tensors="pt", padding=True, truncation=True)

    # 翻译内容
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
            max_length=256
        )
    # 解码输出
    result = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    # 返回结果
    return ResponseDTO(
        source_type = src_lang,
        source_text = src_text,
        target_type = tgt_lang,
        target_text = result
    )