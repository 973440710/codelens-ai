
"""
CodeLens AI - 配置管理模块
处理 API 密钥、模型设置等配置
"""

import os
import yaml
from typing import Optional

CONFIG_FILE = os.path.expanduser("~/.codelens-ai/config.yaml")

class Config:
    def __init__(self):
        self.openai_api_key: Optional[str] = None
        self.gemini_api_key: Optional[str] = None
        self.model: str = "openai"
        self.temperature: float = 0.1
        self.max_tokens: int = 2048
        
        # 确保配置目录存在
        self._ensure_config_dir()
        # 加载配置文件
        self._load_config()
    
    def _ensure_config_dir(self):
        config_dir = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, mode=0o700)
    
    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if config:
                        self.openai_api_key = config.get("openai_api_key")
                        self.gemini_api_key = config.get("gemini_api_key")
                        self.model = config.get("model", "openai")
                        self.temperature = config.get("temperature", 0.1)
                        self.max_tokens = config.get("max_tokens", 2048)
            except Exception as e:
                print(f"⚠️  加载配置文件失败: {e}")
    
    def _save_config(self):
        config = {
            "openai_api_key": self.openai_api_key,
            "gemini_api_key": self.gemini_api_key,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            # 设置权限为仅用户可读写
            os.chmod(CONFIG_FILE, 0o600)
        except Exception as e:
            print(f"⚠️  保存配置文件失败: {e}")
    
    def set_api_keys(self, openai_key: Optional[str] = None, gemini_key: Optional[str] = None):
        """设置 API 密钥"""
        if openai_key:
            self.openai_api_key = openai_key
        if gemini_key:
            self.gemini_api_key = gemini_key
        self._save_config()
    
    def set_model(self, model: str):
        """设置使用的 AI 模型"""
        if model in ["openai", "gemini"]:
            self.model = model
            self._save_config()
        else:
            raise ValueError("无效的模型类型，只支持 'openai' 或 'gemini'")
    
    def set_temperature(self, temperature: float):
        """设置生成温度（0-2）"""
        if 0 <= temperature <= 2:
            self.temperature = temperature
            self._save_config()
        else:
            raise ValueError("温度值必须在 0 到 2 之间")
    
    def validate_config(self, require_api_key: bool = True):
        """验证配置是否完整"""
        if require_api_key:
            if self.model == "openai" and not self.openai_api_key:
                raise ValueError("OpenAI API 密钥未配置，请运行 'codelens config' 命令")
            if self.model == "gemini" and not self.gemini_api_key:
                raise ValueError("Google Gemini API 密钥未配置，请运行 'codelens config' 命令")
    
    def get_api_key(self, require_api_key: bool = True):
        """获取当前模型的 API 密钥"""
        self.validate_config(require_api_key)
        return self.openai_api_key if self.model == "openai" else self.gemini_api_key
