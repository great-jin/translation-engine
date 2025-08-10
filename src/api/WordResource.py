import torch
from typing import List
from fastapi import APIRouter, HTTPException

from schemas.RequestDTO import RequestDTO
from schemas.ResponseDTO import ResponseDTO
from schemas.BatchRequestDTO import BatchRequestDTO
from tool.LanguageTool import detect_lang, convert_type, reverse_type
from tool.ModelTool import model, tokenizer

# 导出接口
router = APIRouter()


# 文本翻译
@router.post("/translate")
def translate(req: RequestDTO) -> ResponseDTO:
    # 格式校验
    msg = RequestDTO.validate_req(req)
    if msg is not None:
        raise HTTPException(status_code = 500, detail = f"{msg}")

    # 语言类型一致直接返回
    source_text = req.text
    source_type = detect_lang(source_text)
    target_type = convert_type(req.targetType)
    if source_type == target_type:
         return ResponseDTO.res_origin(source_text, req.targetType)

    try:
        # 翻译内容
        tokenizer.src_lang = source_type
        inputs = tokenizer(source_text, return_tensors = "pt", padding = True, truncation = True)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_type),
                # 限制生成时的最大 token 数量
                max_length = 512
            )
        # 解码输出
        result = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

        # 返回结果
        return ResponseDTO.res_success(source_type, source_text, req.targetType, result)
    except Exception as e:
        print(f"Translate fail: {str(req)}, error: {e}")
        return ResponseDTO.res_fail(str(e), req.text, req.targetType)


# 批量翻译
@router.post("/translate/batch", response_model = List[ResponseDTO])
def batch_translate(batch_req: BatchRequestDTO) -> List[ResponseDTO]:
    # 数量校验
    req_list = batch_req.requests
    if len(req_list) > 20:
        raise HTTPException(status_code = 500, detail = "Exceeds the maximum allowed limit of 20" )

    # 翻译
    result_list = []
    for req in req_list:
        try:
            result_list.append(translate(req))
        except Exception as e:
            print(f"Translate fail: {str(req)}, error: {e}")
            result_list.append(ResponseDTO.res_fail(str(e), req.text, req.targetType))
            continue

    return result_list
