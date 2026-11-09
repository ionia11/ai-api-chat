import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication
from ui_chat import ChatWindow
from api_request import ApiRequest

load_dotenv()


class MainApp(ChatWindow):
    def __init__(self):
        super().__init__()

        self.send_button.clicked.connect(self.send_request)

    def send_request(self):
        api_key = self.key_input.text().strip() or os.getenv("API_KEY", "").strip()
        user_text = self.message_input.text().strip()

        if not api_key or not user_text:
            return

        self.chat_history.append(f"Вы: {user_text}")
        self.message_input.clear()

        self.request = ApiRequest(api_key, user_text)
        self.request.response_result.connect(self.show_response)
        self.request.error_result.connect(self.show_error)
        self.request.start()

    def show_response(self, text):
        self.chat_history.append(f"AI: {text}\n")

    def show_error(self, err):
        self.chat_history.append(f"[Ошибка]: {err}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
