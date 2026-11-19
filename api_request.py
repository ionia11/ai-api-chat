from PyQt6.QtCore import QThread, pyqtSignal
from google import genai
from google.genai import errors


class ApiRequest(QThread):
    response_result = pyqtSignal(str)
    error_result = pyqtSignal(str)

    def __init__(self, api_key, contents, model):
        super().__init__()
        self.api_key = api_key
        self.contents = contents
        self.model = model

    def run(self):
        try:
            with genai.Client(api_key=self.api_key) as client:
                response = client.models.generate_content(
                    model=self.model,
                    contents=self.contents,
                )

            text = (response.text or "").strip()
            if not text:
                self.error_result.emit("Модель не вернула текст.")
                return

            self.response_result.emit(text)

        except errors.APIError as error:
            if error.code in (401, 403) or "API_KEY_INVALID" in str(error):
                self.error_result.emit(
                    "Неверный API-ключ. Проверьте его в настройках."
                )
            else:
                self.error_result.emit(f"Ошибка API: {error}")
        except Exception as error:
            self.error_result.emit(f"Не удалось выполнить запрос: {error}")
