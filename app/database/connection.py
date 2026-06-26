"""SQLite データベース接続管理"""
import sqlite3
from pathlib import Path

# データベースファイルのパス（プロジェクトルート/data/todo.db）
DB_DIR = Path(__file__).parent.parent.parent / "data"
DB_PATH = DB_DIR / "todo.db"


def get_connection() -> sqlite3.Connection:
    """データベース接続を返す"""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize_db() -> None:
    """テーブルを初期化する（存在しない場合のみ作成）"""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id           INTEGER  PRIMARY KEY AUTOINCREMENT,
                title        TEXT     NOT NULL,
                due_date     DATE,
                tag          TEXT,
                priority     INTEGER  NOT NULL DEFAULT 3,
                is_completed BOOLEAN  NOT NULL DEFAULT 0,
                created_at   DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                completed_at DATETIME
            )
        """)
        conn.commit()
