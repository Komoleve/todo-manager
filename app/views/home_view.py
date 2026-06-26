"""ホーム画面（今日やること）"""
from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.database import task_repository as repo
from app.models.task import Task
from app.views.styles import (
    COLOR_ACCENT,
    COLOR_BG_CARD,
    COLOR_BORDER,
    COLOR_DANGER,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_WARNING,
)


class TaskMiniCard(QWidget):
    """ホーム画面用の小さなタスクカード"""

    complete_requested = Signal(int)  # task_id

    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self._task = task
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("task_item")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)

        # タイトル
        title_label = QLabel(self._task.title)
        title_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 13px;")
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(title_label)

        # 優先度
        prio_label = QLabel(self._task.priority_label)
        prio_label.setStyleSheet(f"color: {COLOR_ACCENT}; font-size: 11px;")
        layout.addWidget(prio_label)

        # 期限
        if self._task.due_date:
            due_str = self._task.due_date.strftime("%m/%d")
            color = COLOR_DANGER if self._task.is_overdue else COLOR_WARNING
            due_label = QLabel(due_str)
            due_label.setStyleSheet(f"color: {color}; font-size: 11px;")
            layout.addWidget(due_label)

        # 完了ボタン
        btn = QPushButton("完了")
        btn.setFixedWidth(52)
        btn.setFixedHeight(26)
        btn.setStyleSheet(
            f"background-color: {COLOR_BG_CARD}; color: {COLOR_TEXT_SECONDARY};"
            f"border: 1px solid {COLOR_BORDER}; border-radius: 4px; font-size: 11px;"
        )
        btn.clicked.connect(lambda: self.complete_requested.emit(self._task.id))
        layout.addWidget(btn)


class SectionWidget(QWidget):
    """セクション（タイトル + タスクリスト）"""

    complete_requested = Signal(int)

    def __init__(self, title: str, label_color: str, tasks: List[Task], parent=None):
        super().__init__(parent)
        self._tasks = tasks
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # セクションヘッダー
        header = QLabel(f"{title}  ({len(tasks)})")
        header.setStyleSheet(
            f"color: {label_color}; font-size: 15px; font-weight: bold; padding: 4px 0;"
        )
        layout.addWidget(header)

        if not tasks:
            empty = QLabel("なし")
            empty.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; padding-left: 8px;")
            layout.addWidget(empty)
        else:
            for task in tasks:
                card = TaskMiniCard(task)
                card.complete_requested.connect(self.complete_requested)
                layout.addWidget(card)

        # セパレーター
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {COLOR_BORDER};")
        layout.addWidget(sep)


class HomeView(QWidget):
    """ホーム画面ウィジェット"""

    # タスク完了が要求されたとき（task_id）
    task_completed = Signal(int)
    # 画面更新要求
    refresh_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        # ページタイトル
        title = QLabel("🏠  今日やること")
        title.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 20px; font-weight: bold;"
        )
        root.addWidget(title)

        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(16)
        self._content_layout.addStretch()

        scroll.setWidget(self._content)
        root.addWidget(scroll)

    def refresh(self) -> None:
        """データを再取得して画面を更新する"""
        # 既存ウィジェットをクリア（stretchを除く）
        layout = self._content_layout
        while layout.count() > 1:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        overdue = repo.get_overdue()
        due_today = repo.get_due_today()
        important = repo.get_high_priority(threshold=4)

        sections = [
            ("⚠️  期限切れ", COLOR_DANGER, overdue),
            ("📅  今日期限", COLOR_WARNING, due_today),
            ("⭐  重要タスク", COLOR_ACCENT, important),
        ]

        for sec_title, color, tasks in sections:
            sec = SectionWidget(sec_title, color, tasks)
            sec.complete_requested.connect(self._on_complete)
            layout.insertWidget(layout.count() - 1, sec)

    def _on_complete(self, task_id: int) -> None:
        repo.complete_task(task_id)
        self.refresh()
        self.task_completed.emit(task_id)
