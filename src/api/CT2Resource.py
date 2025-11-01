from typing import List
from fastapi import APIRouter

from schemas.RequestDTO import RequestDTO
from schemas.ResponseDTO import ResponseDTO
from schemas.BatchRequestDTO import BatchRequestDTO
from tool.LanguageTool import convert_type, detect_lang
from tool.ModelTool import tokenizer, translator

# 导出接口
router = APIRouter()

# 文本翻译
@router.post("/translate", response_model=ResponseDTO)
def translate(req: RequestDTO) -> ResponseDTO:
    try:
        text = req.text
        src_lang = detect_lang(req.text)
        tgt_lang = convert_type(req.targetType)

        # 内容翻译
        tokens = [src_lang] + tokenizer.convert_ids_to_tokens(tokenizer.encode(text)) + ["</s>"]
        results = translator.translate_batch(
            [tokens],
            target_prefix = [[tgt_lang]]
        )
        output_tokens = results[0].hypotheses[0]

        # 解码
        if output_tokens and output_tokens[0] == tgt_lang:
            output_tokens = output_tokens[1:]
        output_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(output_tokens))
        return ResponseDTO.res_success(text, output_text)
    except Exception as e:
        print(f"Translate fail: {str(req)}, error: {e}")
        return ResponseDTO.res_fail(str(e), "")

# 批量翻译
@router.post("/translate/batch", response_model = List[ResponseDTO])
def batch_translate(req: BatchRequestDTO) -> List[ResponseDTO]:
    try:
        sentences = req.textList
        batch_tokens = [
            [detect_lang(s)] + tokenizer.convert_ids_to_tokens(tokenizer.encode(s)) + ["</s>"]
            for s in sentences
        ]

        # 翻译质量
        beam_size = req.quality
        if beam_size is None or beam_size < 1:
            beam_size = 2
        if beam_size > 8:
            beam_size = 8

        # 批量翻译
        tgt_lang = convert_type(req.targetType)
        results = translator.translate_batch(
            batch_tokens,
            target_prefix = [[tgt_lang]] * len(sentences),
            # 增大提升质量, 但效率会降低
            beam_size = beam_size,
            # 启用矢量化 batch 推理, 可提升 CPU 性能（仅支持部分模型）
            use_vmap = True,
            # 禁止生成 <unk>
            disable_unk = True
        )

        # 构建结果
        result_list = []
        for index, item in enumerate(results):
            res = item.hypotheses[0]
            # 解码
            if res and res[0] == tgt_lang:
                res = res[1:]
            output_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(res))
            result_list.append(ResponseDTO.res_success(sentences[index], output_text))
        return result_list
    except Exception as e:
        print(f"Translate fail: {str(req)}, error: {e}")
        return [ResponseDTO.res_fail(str(e), "")]
