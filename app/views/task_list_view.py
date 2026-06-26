"""タスク一覧画面"""
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
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
    COLOR_BG_CARD,
    COLOR_BORDER,
    COLOR_DANGER,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_WARNING,
)
from app.views.task_dialog import TaskDialog


class TaskCard(QWidget):
    """タスク一覧の1行カード"""

    edit_requested = Signal(object)    # Task
    delete_requested = Signal(int)     # task_id
    complete_requested = Signal(int)   # task_id

    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self._task = task
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("task_item")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        # 完了チェックボックス
        self._check = QCheckBox()
        self._check.setChecked(self._task.is_completed)
        self._check.toggled.connect(self._on_check)
        layout.addWidget(self._check)

        # タイトル
        title_label = QLabel(self._task.title)
        title_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 13px;")
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(title_label)

        # タグ
        if self._task.tag:
            tag_label = QLabel(self._task.tag)
            tag_label.setStyleSheet(
                f"color: {COLOR_TEXT_SECONDARY}; font-size: 11px;"
                f"background-color: {COLOR_BG_CARD}; border: 1px solid {COLOR_BORDER};"
                f"border-radius: 4px; padding: 1px 6px;"
            )
            layout.addWidget(tag_label)

        # 優先度
        prio_label = QLabel(self._task.priority_label)
        prio_label.setStyleSheet(f"color: {COLOR_ACCENT}; font-size: 11px; min-width: 70px;")
        layout.addWidget(prio_label)

        # 期限
        if self._task.due_date:
            due_str = self._task.due_date.strftime("%Y/%m/%d")
            if self._task.is_overdue:
                color = COLOR_DANGER
                due_str = f"⚠ {due_str}"
            elif self._task.is_due_today:
                color = COLOR_WARNING
                due_str = f"📅 {due_str}"
            else:
                color = COLOR_TEXT_SECONDARY
            due_label = QLabel(due_str)
            due_label.setStyleSheet(f"color: {color}; font-size: 11px; min-width: 90px;")
            layout.addWidget(due_label)
        else:
            spacer_label = QLabel("")
            spacer_label.setFixedWidth(90)
            layout.addWidget(spacer_label)

        # 編集ボタン
        btn_edit = QPushButton("編集")
        btn_edit.setObjectName("btn_secondary")
        btn_edit.setFixedWidth(52)
        btn_edit.setFixedHeight(28)
        btn_edit.clicked.connect(lambda: self.edit_requested.emit(self._task))
        layout.addWidget(btn_edit)

        # 削除ボタン
        btn_del = QPushButton("削除")
        btn_del.setObjectName("btn_danger")
        btn_del.setFixedWidth(52)
        btn_del.setFixedHeight(28)
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self._task.id))
        layout.addWidget(btn_del)

    def _on_check(self, checked: bool) -> None:
        if checked:
            self.complete_requested.emit(self._task.id)


class TaskListView(QWidget):
    """タスク一覧画面ウィジェット"""

    # 他の画面への更新通知
    tasks_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(12)

        # ヘッダー行
        header = QHBoxLayout()
        title = QLabel("📋  タスク一覧")
        title.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 20px; font-weight: bold;"
        )
        header.addWidget(title)
        header.addStretch()

        btn_add = QPushButton("＋ タスクを追加")
        btn_add.setFixedHeight(34)
        btn_add.clicked.connect(self._on_add)
        header.addWidget(btn_add)
        root.addLayout(header)

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

        tasks = repo.get_all_active()

        if not tasks:
            empty = QLabel("タスクがありません。「＋ タスクを追加」から追加してください。")
            empty.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; padding: 20px;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.insertWidget(0, empty)
        else:
            for task in tasks:
                card = TaskCard(task)
                card.edit_requested.connect(self._on_edit)
                card.delete_requested.connect(self._on_delete)
                card.complete_requested.connect(self._on_complete)
                layout.insertWidget(layout.count() - 1, card)

    def _on_add(self) -> None:
        dlg = TaskDialog(self)
        if dlg.exec() == TaskDialog.DialogCode.Accepted:
            repo.add_task(
                title=dlg.task_title,
                due_date=dlg.task_due_date,
                tag=dlg.task_tag,
                priority=dlg.task_priority,
            )
            self.refresh()
            self.tasks_changed.emit()

    def _on_edit(self, task: Task) -> None:
        dlg = TaskDialog(self, task=task)
        if dlg.exec() == TaskDialog.DialogCode.Accepted:
            repo.update_task(
                task_id=task.id,
                title=dlg.task_title,
                due_date=dlg.task_due_date,
                tag=dlg.task_tag,
                priority=dlg.task_priority,
            )
            self.refresh()
            self.tasks_changed.emit()

    def _on_delete(self, task_id: int) -> None:
        reply = QMessageBox.question(
            self,
            "削除確認",
            "このタスクを削除しますか？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            repo.delete_task(task_id)
            self.refresh()
            self.tasks_changed.emit()

    def _on_complete(self, task_id: int) -> None:
        repo.complete_task(task_id)
        self.refresh()
        self.tasks_changed.emit()
