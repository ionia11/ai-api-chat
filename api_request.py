from PyQt6.QtCore import QThread, pyqtSignal
from google import genai
from google.genai import errors, types

REQUEST_TIMEOUT_MS = 20_000


class ApiRequest(QThread):
    response_result = pyqtSignal(str)
    error_result = pyqtSignal(str)

    def __init__(self, api_key, contents, model, timeout_ms=REQUEST_TIMEOUT_MS):
        super().__init__()
        self.api_key = api_key
        self.contents = contents
        self.model = model
        self.timeout_ms = timeout_ms

    def stop(self):
        self.requestInterruption()
        self.terminate()
        self.wait(2000)

    def _timeout_message(self):
        seconds = self.timeout_ms / 1000
        return (
            f"Превышено время ожидания ответа ({seconds:g} с). "
            "Проверьте подключение к интернету и попробуйте ещё раз."
        )

    @staticmethod
    def is_timeout_error(error):
        if isinstance(error, TimeoutError):
            return True
        for klass in type(error).__mro__:
            if "Timeout" in klass.__name__:
                return True
        return getattr(error, "code", None) in (408, 504)

    def run(self):
        try:
            http_options = types.HttpOptions(timeout=self.timeout_ms)
            with genai.Client(
                api_key=self.api_key, http_options=http_options
            ) as client:
                response = client.models.generate_content(
                    model=self.model,
                    contents=self.contents,
                )

        except Exception as error:
            if self.isInterruptionRequested():
                return

            if self.is_timeout_error(error):
                self.error_result.emit(self._timeout_message())
            elif isinstance(error, errors.APIError):
                if error.code in (401, 403) or "API_KEY_INVALID" in str(error):
                    self.error_result.emit(
                        "Неверный API-ключ. Проверьте его в настройках."
                    )
                else:
                    self.error_result.emit(f"Ошибка API: {error}")
            else:
                self.error_result.emit(f"Не удалось выполнить запрос: {error}")
            return

        if self.isInterruptionRequested():
            return

        text = (response.text or "").strip()
        if not text:
            self.error_result.emit("Модель не вернула текст.")
            return

        self.response_result.emit(text)
