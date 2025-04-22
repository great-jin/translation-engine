import yaml
import os
from config.AppConfig import AppConfig
from config.ModelConfig import ModelConfig

# 配置文件
def load_config():
    # 读取相对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, '../../resource/config.yml')

    # 文件存在判断
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Not found config file of: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# 加载配置文件
_config_data = load_config()

# 获取系统配置
def get_app_config() -> AppConfig:
    app_data = _config_data.get('app', {})
    return AppConfig(**app_data)

# 获取模型配置
def get_model_config() -> ModelConfig:
    model_data = _config_data.get('model', {})
    return ModelConfig(**model_data)
