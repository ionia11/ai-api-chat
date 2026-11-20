import sys
import ctypes
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import QApplication
from ctypes import wintypes
from ui.stylesheet_file import STYLESHEET

DARK_BACKGROUND = QColor(30, 30, 30)
DARK_SURFACE = QColor(45, 45, 45)
DARK_ALTERNATE = QColor(53, 53, 53)
LIGHT_TEXT = QColor(240, 240, 240)
ACCENT = QColor(42, 130, 218)


def build_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, DARK_BACKGROUND)
    palette.setColor(QPalette.ColorRole.WindowText, LIGHT_TEXT)
    palette.setColor(QPalette.ColorRole.Base, DARK_SURFACE)
    palette.setColor(QPalette.ColorRole.AlternateBase, DARK_ALTERNATE)
    palette.setColor(QPalette.ColorRole.ToolTipBase, DARK_SURFACE)
    palette.setColor(QPalette.ColorRole.ToolTipText, LIGHT_TEXT)
    palette.setColor(QPalette.ColorRole.Text, LIGHT_TEXT)
    palette.setColor(QPalette.ColorRole.Button, DARK_ALTERNATE)
    palette.setColor(QPalette.ColorRole.ButtonText, LIGHT_TEXT)
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 80, 80))
    palette.setColor(QPalette.ColorRole.Link, ACCENT)
    palette.setColor(QPalette.ColorRole.Highlight, ACCENT)
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(150, 150, 150))

    for role in (
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
    ):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(120, 120, 120))

    return palette


def apply_dark_theme(app: QApplication):
    app.setStyle("Fusion")

    font = QFont("Segoe UI", 10)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)

    app.setPalette(build_dark_palette())
    app.setStyleSheet(STYLESHEET)


def enable_dark_title_bar(window):
    try:
        hwnd = wintypes.HWND(int(window.winId()))
        value = ctypes.c_int(1)
        for attribute in (20, 19):
            result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, attribute, ctypes.byref(value), ctypes.sizeof(value)
            )
            if result == 0:
                break
    except Exception:
        pass
