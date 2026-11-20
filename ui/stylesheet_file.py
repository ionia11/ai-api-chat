STYLESHEET = """
            QWidget { color: #f2eef5; font-family: "Segoe UI"; font-size: 14px; }
            
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #2c0a38, stop:0.35 #6d2440, stop:1 #1d0a33);
            }
            QDialog { background: #1b1220; }
            
            #sidebar_widget, #chat_view {
                background: rgba(255, 255, 255, 16);
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 14px;
            }
            #chat_view { padding: 10px 14px; }
            #chats_list { background: transparent; border: none; outline: none; }
            #chats_list::item { padding: 8px 10px; margin: 2px; border-radius: 8px; }
            #chats_list::item:hover { background: rgba(255, 255, 255, 22); }
            #chats_list::item:selected { background: rgba(124, 92, 220, 120); color: #fff; }
            
            QMenuBar, QStatusBar { background: transparent; color: #d9cfe4; }
            QMenuBar::item { padding: 5px 10px; border-radius: 6px; }
            QMenuBar::item:selected { background: rgba(255, 255, 255, 26); }
            QMenu {
                background: #241428;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item { padding: 6px 20px; border-radius: 5px; }
            QMenu::item:selected { background: rgba(124, 92, 220, 150); color: #fff; }
            
            QPushButton, QLineEdit, QComboBox {
                background: rgba(255, 255, 255, 16);
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 9px;
                padding: 7px 12px;
            }
            QPushButton:hover, QLineEdit:hover, QComboBox:hover {
                background: rgba(255, 255, 255, 26);
                border-color: rgba(255, 255, 255, 70);
            }
            QLineEdit:focus, QComboBox:focus { border-color: rgba(150, 120, 255, 170); }
            QPushButton:disabled, QLineEdit:disabled {
                color: rgba(242, 238, 245, 110);
                background: rgba(255, 255, 255, 8);
                border-color: rgba(255, 255, 255, 18);
            }
            QPushButton:pressed { background: rgba(124, 92, 220, 130); }
            
            #new_chat_button { padding: 9px; font-weight: 600; }
            #send_button {
                background: #7c5cdc;
                border: none;
                padding: 9px 20px;
                color: #fff;
                font-weight: 600;
            }
            #send_button:hover { background: #8d6ff0; }
            #send_button:pressed { background: #6a4bc4; }
            
            QComboBox::drop-down { border: none; width: 22px; }
            QComboBox QAbstractItemView {
                background: #241428;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 6px;
                padding: 4px;
                selection-background-color: rgba(124, 92, 220, 150);
            }
            QCheckBox { spacing: 8px; background: transparent; }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                background: rgba(255, 255, 255, 14);
                border: 1px solid rgba(255, 255, 255, 60);
                border-radius: 4px;
            }
            QCheckBox::indicator:checked { background: #7c5cdc; border-color: #b29cff; }
            
            QToolTip {
                background: #241428;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 6px;
                padding: 5px 8px;
            }
            
            QScrollBar:vertical { background: transparent; width: 8px; margin: 4px 2px; }
            QScrollBar:horizontal { background: transparent; height: 0; }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 55);
                min-height: 24px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover { background: rgba(255, 255, 255, 95); }
            QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }
            QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }
            """