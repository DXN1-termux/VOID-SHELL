import json
from dataclasses import dataclass, field
from typing import Dict, Any
from void_shell.utils.paths import CONFIG_PATH

@dataclass
class AIConfig:
    provider: str = "ollama"
    endpoint: str = "http://localhost:11434/api/generate"
    model: str = "qwen2.5-coder:0.5b"
    temperature: float = 0.2
    max_tokens: int = 1024

@dataclass
class FeatureConfig:
    shadow_execution: bool = True
    neural_overlay: bool = True
    auto_correct: bool = True
    stealth_mode: bool = False

@dataclass
class Config:
    ai: AIConfig = field(default_factory=AIConfig)
    features: FeatureConfig = field(default_factory=FeatureConfig)
    system: Dict[str, Any] = field(default_factory=lambda: {
        "log_level": "INFO",
        "max_parallel_workers": 8
    })

def load_config(path: str = None) -> Config:
    target_path = path or str(CONFIG_PATH)
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            return Config(
                ai=AIConfig(**data.get("ai", {})),
                features=FeatureConfig(**data.get("features", {})),
                system=data.get("system", {})
            )
    return Config()
