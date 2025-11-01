from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import ctranslate2
from pathlib import Path
# 导入工具
from tool.ConfigTool import get_model_config

# 配置加载
model_config = get_model_config()

# 加载 NLLB 模型
model_path = Path(model_config.nllbPath)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=True)
model.eval()

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)

# 加载 CT2 模型
translator = ctranslate2.Translator(
    model_config.ct2Path,
    device = "cpu",
    # 精度
    compute_type = "int8",
    # 任务并发数
    inter_threads = 4,
    # 单个任务内部并行数，默认 4
    intra_threads = 4
)
