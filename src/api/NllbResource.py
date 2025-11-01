import torch
from typing import List
from fastapi import APIRouter, HTTPException

from schemas.RequestDTO import RequestDTO
from schemas.ResponseDTO import ResponseDTO
from schemas.BatchRequestDTO import BatchRequestDTO
from tool.LanguageTool import detect_lang, convert_type
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
         return ResponseDTO.res_origin(source_text)

    try:
        # 内容翻译
        tokenizer.src_lang = source_type
        inputs = tokenizer(
            source_text,
            # 指定返回的张量类型。
            # pt: PyTorch 张量
            # tf: TensorFlow
            # np: NumPy 数组
            return_tensors="pt",
            # 是否补到当前 batch 的最长序列长度
            padding=True,
            # 是否截断过长序列
            # True: 自动截断超过模型最大长度的输入
            # False: 不过滤（可能导致报错）
            # longest_first: 优先保留重要部分
            truncation=True,
            # 用于屏蔽 padding 部分，默认 True
            return_attention_mask=True
        )
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                # shape[0]: 输入的记录数量
                # shape[0]: 序列长度（每条句子被分成多少个 token），取句子最长的值，其余通过 padding 填充
                max_new_tokens = min(256, int(inputs["input_ids"].shape[1] * 1.5)),
                forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_type)
            )
        result = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

        # 返回结果
        return ResponseDTO.res_success(source_text, result)
    except Exception as e:
        print(f"Translate fail: {str(req)}, error: {e}")
        return ResponseDTO.res_fail(str(e), req.text)


# 批量翻译
@router.post("/translate/batch", response_model = List[ResponseDTO])
def batch_translate(batch_req: BatchRequestDTO) -> List[ResponseDTO]:
    req_list = batch_req.textList
    target_type = convert_type(batch_req.targetType)

    # 内容翻译
    inputs = tokenizer(
        req_list,
        return_tensors="pt",
        padding=True,
        truncation=True,
        return_attention_mask=True
    )
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens = 256,
            forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_type)
        )
    results = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    # 结果构建
    result_list = []
    for i, res in enumerate(results):
        result_list.append(ResponseDTO.res_success(req_list[i], res))
    return result_list
