"""メインウィンドウ（サイドバーナビゲーション + ページ切り替え）"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.views.archive_view import ArchiveView
from app.views.home_view import HomeView
from app.views.styles import (
    COLOR_ACCENT,
    COLOR_BG_DARK,
    COLOR_BG_PANEL,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)
from app.views.task_list_view import TaskListView


class NavButton(QPushButton):
    """サイドバーナビゲーションボタン"""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setObjectName("nav_button")
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class MainWindow(QMainWindow):
    """アプリのメインウィンドウ"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDoアプリ")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)
        self._setup_ui()
        # 起動時にホーム画面を表示
        self._switch_page(0)

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ──────────────────────────────────────────────
        # サイドバー
        # ──────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(4)

        # アプリ名
        from PySide6.QtWidgets import QLabel
        app_name = QLabel("✅ ToDoアプリ")
        app_name.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 16px; font-weight: bold;"
            f"padding: 8px 4px 16px 4px;"
        )
        sidebar_layout.addWidget(app_name)

        # ナビボタン
        self._nav_buttons: list[NavButton] = []
        nav_items = [
            ("🏠  今日やること", 0),
            ("📋  タスク一覧", 1),
            ("🗂  アーカイブ", 2),
        ]
        for label, idx in nav_items:
            btn = NavButton(label)
            btn.clicked.connect(lambda checked, i=idx: self._switch_page(i))
            sidebar_layout.addWidget(btn)
            self._nav_buttons.append(btn)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # ──────────────────────────────────────────────
        # コンテンツエリア（StackedWidget）
        # ──────────────────────────────────────────────
        self._stack = QStackedWidget()

        self._home_view = HomeView()
        self._task_list_view = TaskListView()
        self._archive_view = ArchiveView()

        self._stack.addWidget(self._home_view)       # index 0
        self._stack.addWidget(self._task_list_view)  # index 1
        self._stack.addWidget(self._archive_view)    # index 2

        main_layout.addWidget(self._stack)

        # ──────────────────────────────────────────────
        # シグナル接続（画面間の連携）
        # ──────────────────────────────────────────────
        # タスク一覧でタスクが変更されたらホームも更新
        self._task_list_view.tasks_changed.connect(self._home_view.refresh)
        # アーカイブでタスクが変更されたらホーム・一覧も更新
        self._archive_view.tasks_changed.connect(self._home_view.refresh)
        self._archive_view.tasks_changed.connect(self._task_list_view.refresh)
        # ホームで完了したらタスク一覧も更新
        self._home_view.task_completed.connect(lambda _: self._task_list_view.refresh())
        self._home_view.task_completed.connect(lambda _: self._archive_view.refresh())

    def _switch_page(self, index: int) -> None:
        """ページを切り替えてナビボタンの状態を更新する"""
        self._stack.setCurrentIndex(index)

        for i, btn in enumerate(self._nav_buttons):
            btn.setChecked(i == index)
            if i == index:
                btn.setStyleSheet(
                    f"background-color: {COLOR_ACCENT}; color: white;"
                    f"border: none; border-radius: 8px; padding: 10px 16px;"
                    f"text-align: left; font-size: 14px;"
                )
            else:
                btn.setStyleSheet(
                    f"background-color: transparent; color: {COLOR_TEXT_SECONDARY};"
                    f"border: none; border-radius: 8px; padding: 10px 16px;"
                    f"text-align: left; font-size: 14px;"
                )

        # ページ切り替え時にデータを更新
        current = self._stack.currentWidget()
        if hasattr(current, "refresh"):
            current.refresh()

    def initial_refresh(self) -> None:
        """起動時の初期データ読み込み"""
        self._home_view.refresh()
        self._task_list_view.refresh()
        self._archive_view.refresh()
