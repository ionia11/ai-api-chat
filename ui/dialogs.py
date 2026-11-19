from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from ui.app_settings import AVAILABLE_MODELS, AppSettings


class SettingsDialog(QDialog):
    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Настройки")
        self.setModal(True)
        self.setMinimumWidth(420)

        self.key_input = QLineEdit(settings.get_api_key())
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setPlaceholderText("Введите API-ключ")
        self.key_input.setClearButtonEnabled(True)

        show_key = QCheckBox("Показать ключ")
        show_key.toggled.connect(self._toggle_key_visibility)

        self.model_combo = QComboBox()
        for model_id, label in AVAILABLE_MODELS:
            self.model_combo.addItem(label, model_id)
        index = self.model_combo.findData(settings.get_model())
        if index >= 0:
            self.model_combo.setCurrentIndex(index)

        hint = QLabel(
            "Ключ хранится локально в файле .env и используется "
            "для запросов к нейросети."
        )
        hint.setWordWrap(True)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Save).setText("Сохранить")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Отмена")
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)

        form = QFormLayout()
        form.addRow("API-ключ:", self.key_input)
        form.addRow("Модель:", self.model_combo)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(show_key)
        layout.addWidget(hint)
        layout.addWidget(buttons)

    def _toggle_key_visibility(self, visible):
        mode = QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password
        self.key_input.setEchoMode(mode)

    def _save(self):
        api_key = self.key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Настройки", "Введите API-ключ.")
            return

        try:
            self.settings.set_api_key(api_key)
            self.settings.set_model(self.model_combo.currentData())
        except (OSError, ValueError) as error:
            QMessageBox.warning(
                self,
                "Настройки",
                f"Не удалось сохранить настройки:\n{error}",
            )
            return

        self.accept()
