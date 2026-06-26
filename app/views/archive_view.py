"""アーカイブ画面"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
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
    COLOR_BORDER,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)


class ArchivedTaskCard(QWidget):
    """アーカイブ済みタスクの1行カード"""

    restore_requested = Signal(int)   # task_id
    delete_requested = Signal(int)    # task_id

    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self._task = task
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("task_item")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        # タイトル（打ち消し線）
        title_label = QLabel(self._task.title)
        title_label.setStyleSheet(
            f"color: {COLOR_TEXT_MUTED}; font-size: 13px; text-decoration: line-through;"
        )
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(title_label)

        # タグ
        if self._task.tag:
            tag_label = QLabel(self._task.tag)
            tag_label.setStyleSheet(
                f"color: {COLOR_TEXT_SECONDARY}; font-size: 11px;"
                f"border: 1px solid {COLOR_BORDER}; border-radius: 4px; padding: 1px 6px;"
            )
            layout.addWidget(tag_label)

        # 完了日時
        if self._task.completed_at:
            completed_str = self._task.completed_at.strftime("%Y/%m/%d %H:%M")
            comp_label = QLabel(f"完了: {completed_str}")
            comp_label.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 11px;")
            layout.addWidget(comp_label)

        # 復元ボタン
        btn_restore = QPushButton("復元")
        btn_restore.setObjectName("btn_secondary")
        btn_restore.setFixedWidth(52)
        btn_restore.setFixedHeight(28)
        btn_restore.clicked.connect(lambda: self.restore_requested.emit(self._task.id))
        layout.addWidget(btn_restore)

        # 削除ボタン
        btn_del = QPushButton("削除")
        btn_del.setObjectName("btn_danger")
        btn_del.setFixedWidth(52)
        btn_del.setFixedHeight(28)
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self._task.id))
        layout.addWidget(btn_del)


class ArchiveView(QWidget):
    """アーカイブ画面ウィジェット"""

    # タスクが復元されたとき（他画面の更新用）
    tasks_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(12)

        # ページタイトル
        title = QLabel("🗂  アーカイブ")
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
        self._content_layout.setSpacing(6)
        self._content_layout.addStretch()

        scroll.setWidget(self._content)
        root.addWidget(scroll)

    def refresh(self) -> None:
        """データを再取得して画面を更新する"""
        layout = self._content_layout
        while layout.count() > 1:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        tasks = repo.get_all_archived()

        if not tasks:
            empty = QLabel("完了済みタスクはありません。")
            empty.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; padding: 20px;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.insertWidget(0, empty)
        else:
            for task in tasks:
                card = ArchivedTaskCard(task)
                card.restore_requested.connect(self._on_restore)
                card.delete_requested.connect(self._on_delete)
                layout.insertWidget(layout.count() - 1, card)

    def _on_restore(self, task_id: int) -> None:
        repo.restore_task(task_id)
        self.refresh()
        self.tasks_changed.emit()

    def _on_delete(self, task_id: int) -> None:
        reply = QMessageBox.question(
            self,
            "削除確認",
            "このタスクを完全に削除しますか？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            repo.delete_task(task_id)
            self.refresh()
