from PyQt6.QtCore import QThread, pyqtSignal
from google import genai


class ApiRequest(QThread):
    response_result = pyqtSignal(str)
    error_result = pyqtSignal(str)

    def __init__(self, api_key, prompt):
        super().__init__()
        self.api_key = api_key
        self.prompt = prompt

    def run(self):
        try:
            if not self.prompt:
                raise ValueError("Текст сообщения пуст")

            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=self.prompt,
            )  # тут добавить контекст

            self.response_result.emit(response.text)

        except Exception as e:
            self.error_result.emit(str(e))
