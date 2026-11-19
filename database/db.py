import sqlite3


class ChatStorage:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(str(db_path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        with self.connection:
            self.connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                );
                """
            )

    def get_chats(self):
        cursor = self.connection.execute(
            "SELECT id, title FROM chats ORDER BY id DESC"
        )
        return cursor.fetchall()

    def create_chat(self, title):
        with self.connection:
            cursor = self.connection.execute(
                "INSERT INTO chats (title) VALUES (?)", (title,)
            )
        return cursor.lastrowid

    def delete_chat(self, chat_id):
        with self.connection:
            self.connection.execute("DELETE FROM chats WHERE id = ?", (chat_id,))

    def add_message(self, chat_id, role, content):
        with self.connection:
            self.connection.execute(
                "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
                (chat_id, role, content),
            )

    def get_messages(self, chat_id):
        cursor = self.connection.execute(
            "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY id",
            (chat_id,),
        )
        return cursor.fetchall()

    def get_history(self, chat_id):
        return [
            {"role": row["role"], "parts": [{"text": row["content"]}]}
            for row in self.get_messages(chat_id)
        ]

    def close(self):
        self.connection.close()
