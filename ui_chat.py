from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Chat App")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Введите API-ключ...")
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.key_input)

        # История чата
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        # Поле ввода сообщения
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Напишите сообщение...")
        layout.addWidget(self.message_input)

        # Кнопка отправки
        self.send_button = QPushButton("Отправить")
        layout.addWidget(self.send_button)

        self.setLayout(layout)
