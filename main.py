"""ToDoアプリ エントリーポイント"""
import sys

from PySide6.QtWidgets import QApplication

from app.database.connection import initialize_db
from app.database.task_repository import get_due_today
from app.services.notification import notify_due_today
from app.views.main_window import MainWindow
from app.views.styles import APP_STYLESHEET


def main() -> None:
    # データベース初期化
    initialize_db()

    app = QApplication(sys.argv)
    app.setApplicationName("ToDoアプリ")
    app.setStyleSheet(APP_STYLESHEET)

    # メインウィンドウ生成・表示
    window = MainWindow()
    window.show()
    window.initial_refresh()

    # 起動時通知（今日期限のタスクがあれば）
    due_today = get_due_today()
    notify_due_today(due_today)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
