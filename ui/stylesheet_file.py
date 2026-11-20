STYLESHEET = """
                    QMainWindow {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #390c3b, stop:0.3 #7d2941, stop:1 #240c3b);
                        font-family: 'Segoe UI', sans-serif;
                        font-size: 14px;
                        
                    }

                    QTextBrowser {
                        background-color: transparent;

                        font-size: 14px;
                        /* font-family: "Courier New", monospace; */
                    }

                    /* Стиль для всего меню-бара */
                    QMenuBar {
                        background-color: transparent;
                        color: #a9b7c6;
                    }
                    
                    QListWidget {
                        background-color: transparent;
                        color: transparent;
                        font-size: 14px;
                        font-family: "Courier New", monospace;
                    }

                    /* Стиль для отдельного пункта меню (Файл, Правка...) */
                    QMenuBar::item {
                        background-color: transparent; /* Прозрачный фон */
                    }

                    /* Стиль для пункта меню при его выборе */
                    QMenuBar::item:selected {
                        background-color: transparent;
                    }

                    /* Стиль для выпадающего меню */
                    QMenu {
                        background-color: transparent;
                        color: #a9b7c6;
                        border: 1px solid #555;
                    }

                    /* Стиль для пунктов в выпадающем меню при наведении */
                    QMenu::item:selected {
                        background-color: #555;
                    }


                    QPushButton {
                        background-color: transparent;
                        color: #a9b7c6;

                        padding: 5px 10px;
                    }

                    /* Стиль для кнопок при наведении мышки */
                    QPushButton:hover {
                        border: 1px solid #858585;
                        border-radius: 5px;
                    }

                    /* Стиль для кнопок при клике мышки */
                    QPushButton:pressed {
                        border: 2px solid #2980b9;
                        border-radius: 10px;
                    }
                    
                    QLineEdit {
                        background-color: #252526;
                        border: 1px solid #3f3f3f;
                        border-radius: 4px;
                        padding: 4px;
                        color: #ffffff;
                    }
                    
                    QLineEdit:focus {
                        border: 1px solid #0078d7;
                """