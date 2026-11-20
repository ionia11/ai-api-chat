import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextBlockFormat
from PyQt6.QtWidgets import (
    QApplication,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
)

from api_request import ApiRequest
from database.db import ChatStorage
from ui.app_settings import AppSettings
from ui.dialogs import SettingsDialog
from ui.theme import apply_dark_theme, enable_dark_title_bar

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
    UI_PATH = Path(getattr(sys, "_MEIPASS", BASE_DIR)) / "ui" / "main_window.ui"
else:
    BASE_DIR = Path(__file__).resolve().parent
    UI_PATH = BASE_DIR / "ui" / "main_window.ui"

DB_PATH = BASE_DIR / "database" / "chat.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_CHAT_TITLE = "Новый чат"
MAX_TITLE_LENGTH = 40
MESSAGE_SPACING_LINES = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI_PATH), self)

        self.main_layout.setContentsMargins(14, 12, 14, 12)
        self.main_layout.setSpacing(12)
        self.sidebar_layout.setContentsMargins(12, 12, 12, 12)
        self.sidebar_layout.setSpacing(10)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_layout.setSpacing(12)
        self.input_layout.setSpacing(10)

        self.settings = AppSettings()
        self.storage = ChatStorage(DB_PATH)
        self.current_chat_id = None
        self.request = None

        self.new_chat_button.clicked.connect(self.new_chat)
        self.send_button.clicked.connect(self.send_request)
        self.message_input.returnPressed.connect(self.send_request)
        self.chats_list.itemSelectionChanged.connect(self.on_chat_selected)
        self.chats_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.chats_list.customContextMenuRequested.connect(self.show_chat_menu)
        self.chats_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.chats_list.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.action_settings.triggered.connect(self.open_settings)
        self.chat_view.setPlaceholderText(
            "Выберите чат или начните новый. API-ключ задаётся в меню «Настройки»."
        )
        self.chat_view.setOpenExternalLinks(True)
        self.reload_chats()
        self.message_input.setFocus()
        self.statusBar().showMessage("Готово")

    def showEvent(self, event):
        super().showEvent(event)
        enable_dark_title_bar(self)

    def open_settings(self):
        SettingsDialog(self.settings, self).exec()

    def reload_chats(self, select_chat_id=None):
        self.chats_list.blockSignals(True)
        self.chats_list.clear()
        for chat in self.storage.get_chats():
            item = QListWidgetItem(chat["title"])
            item.setData(Qt.ItemDataRole.UserRole, chat["id"])
            self.chats_list.addItem(item)

        if select_chat_id is not None:
            for row in range(self.chats_list.count()):
                item = self.chats_list.item(row)
                if item.data(Qt.ItemDataRole.UserRole) == select_chat_id:
                    self.chats_list.setCurrentRow(row)
                    break

        self.chats_list.blockSignals(False)

    def on_chat_selected(self):
        item = self.chats_list.currentItem()
        if item is None:
            return

        self.current_chat_id = item.data(Qt.ItemDataRole.UserRole)
        self.render_chat()

    def new_chat(self):
        self.chats_list.blockSignals(True)
        self.chats_list.setCurrentRow(-1)
        self.chats_list.blockSignals(False)

        self.current_chat_id = None
        self.chat_view.clear()
        self.message_input.setFocus()

    def show_chat_menu(self, pos):
        item = self.chats_list.itemAt(pos)
        if item is None:
            return

        menu = QMenu(self)
        delete_action = menu.addAction("Удалить")
        chosen = menu.exec(self.chats_list.mapToGlobal(pos))

        if chosen == delete_action:
            self.delete_chat(item)

    def delete_chat(self, item):
        chat_id = item.data(Qt.ItemDataRole.UserRole)
        title = item.text()

        answer = QMessageBox.question(
            self,
            "Удаление чата",
            f"Удалить чат «{title}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        self.storage.delete_chat(chat_id)

        if self.current_chat_id == chat_id:
            self.current_chat_id = None
            self.chat_view.clear()

        self.reload_chats(self.current_chat_id)

    def render_chat(self):
        if self.current_chat_id is None:
            self.chat_view.clear()
            return

        blocks = []
        for message in self.storage.get_messages(self.current_chat_id):
            prefix = "**Вы:**" if message["role"] == "user" else "**AI:**"
            blocks.append(f"{prefix} {message['content']}")

        self.chat_view.clear()
        cursor = self.chat_view.textCursor()
        spacing = int(
            self.chat_view.fontMetrics().lineSpacing() * MESSAGE_SPACING_LINES
        )
        first = True
        for block in blocks:
            if not first:
                block_format = QTextBlockFormat()
                block_format.setTopMargin(spacing)
                cursor.insertBlock(block_format)
            first = False
            cursor.insertMarkdown(block)

        scrollbar = self.chat_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_request(self):
        if self.request is not None:
            return

        user_text = self.message_input.text().strip()
        if not user_text:
            return

        api_key = self.settings.get_api_key()
        if not api_key:
            QMessageBox.information(
                self,
                "API-ключ",
                "Сначала задайте API-ключ в настройках.",
            )
            self.open_settings()
            return

        is_new_chat = self.current_chat_id is None
        if is_new_chat:
            self.current_chat_id = self.storage.create_chat(self.make_title(user_text))

        self.storage.add_message(self.current_chat_id, "user", user_text)
        self.message_input.clear()

        if is_new_chat:
            self.reload_chats(self.current_chat_id)
        else:
            self.render_chat()

        self.request = ApiRequest(
            api_key,
            self.storage.get_history(self.current_chat_id),
            self.settings.get_model(),
        )
        self.request.response_result.connect(self.show_response)
        self.request.error_result.connect(self.show_error)
        self.request.finished.connect(self.on_request_finished)

        self.set_busy(True)
        self.statusBar().showMessage("Ожидание ответа…")
        self.request.start()

    def show_response(self, text):
        self.storage.add_message(self.current_chat_id, "model", text)
        self.render_chat()
        self.statusBar().showMessage("Готово")

    def show_error(self, error):
        self.statusBar().showMessage(f"Ошибка: {error}")
        self.chat_view.append(f"[Ошибка]: {error}")

    def on_request_finished(self):
        request = self.request
        self.request = None
        if request is not None:
            request.deleteLater()

        self.set_busy(False)

    def set_busy(self, busy):
        for widget in (
            self.send_button,
            self.message_input,
            self.new_chat_button,
            self.chats_list,
        ):
            widget.setEnabled(not busy)

        if not busy:
            self.message_input.setFocus()

    def make_title(self, user_text):
        text = " ".join(user_text.split()) or DEFAULT_CHAT_TITLE
        if len(text) <= MAX_TITLE_LENGTH:
            return text
        return text[:MAX_TITLE_LENGTH].rstrip() + "…"

    def closeEvent(self, event):
        if self.request is not None:
            answer = QMessageBox.question(
                self,
                "Выход",
                "Точно выйти?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                event.ignore()
                return

            self.stop_request()

        self.storage.close()
        super().closeEvent(event)

    def stop_request(self):
        request = self.request
        self.request = None
        if request is not None:
            request.stop()
            request.deleteLater()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AI B2B SaaS API Chat")

    apply_dark_theme(app)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
