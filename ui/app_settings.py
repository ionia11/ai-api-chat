import sys
from pathlib import Path

from dotenv import dotenv_values, set_key

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

DEFAULT_MODEL = "gemini-3.5-flash-lite"
AVAILABLE_MODELS = (
    ("gemini-3.5-flash-lite", "Gemini 3.5 Flash Lite"),
    ("gemini-3.8-flash", "Gemini 3.8 Flash"),
)
MODEL_IDS = [model_id for model_id, _ in AVAILABLE_MODELS]


class AppSettings:
    def __init__(self, env_path=None):
        self.env_path = Path(env_path) if env_path else ENV_PATH

    def _values(self):
        return dotenv_values(self.env_path)

    def get_api_key(self):
        return (self._values().get("API_KEY") or "").strip()

    def get_model(self):
        model = (self._values().get("MODEL_NAME") or "").strip()
        return model if model in MODEL_IDS else DEFAULT_MODEL

    def set_api_key(self, api_key):
        self._set_value("API_KEY", api_key.strip())

    def set_model(self, model):
        if model not in MODEL_IDS:
            raise ValueError(f"Неизвестная модель: {model}")
        self._set_value("MODEL_NAME", model)

    def _set_value(self, key, value):
        set_key(str(self.env_path), key, value, quote_mode="always")
