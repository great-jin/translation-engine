from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pathlib import Path
# 导入工具
from tool.ConfigTool import get_model_config

# 配置加载
model_config = get_model_config()

# 模型加载
model_path = Path(model_config.path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
