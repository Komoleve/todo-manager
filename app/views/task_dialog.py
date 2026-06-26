"""タスク追加・編集ダイアログ"""
from datetime import date
from typing import Optional

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from app.models.task import DEFAULT_PRIORITY, PRIORITY_LABELS, TAGS, Task


class TaskDialog(QDialog):
    """タスク追加・編集ダイアログ"""

    def __init__(self, parent: Optional[QWidget] = None, task: Optional[Task] = None):
        super().__init__(parent)
        self._task = task
        self._setup_ui()
        if task:
            self._populate(task)

    def _setup_ui(self) -> None:
        title = "タスクを編集" if self._task else "タスクを追加"
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        form = QFormLayout()
        form.setSpacing(10)

        # タイトル
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("タスク名を入力してください")
        form.addRow("タイトル *", self.title_edit)

        # 期限
        self.use_due_date = QCheckBox("期限を設定する")
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDate(QDate.currentDate())
        self.due_date_edit.setEnabled(False)
        self.use_due_date.toggled.connect(self.due_date_edit.setEnabled)
        form.addRow("期限", self.use_due_date)
        form.addRow("", self.due_date_edit)

        # タグ
        self.tag_combo = QComboBox()
        self.tag_combo.addItem("（なし）", None)
        for tag in TAGS:
            self.tag_combo.addItem(tag, tag)
        form.addRow("タグ", self.tag_combo)

        # 優先度
        self.priority_combo = QComboBox()
        for val in sorted(PRIORITY_LABELS.keys(), reverse=True):
            self.priority_combo.addItem(PRIORITY_LABELS[val], val)
        # デフォルト選択
        default_idx = self.priority_combo.findData(DEFAULT_PRIORITY)
        if default_idx >= 0:
            self.priority_combo.setCurrentIndex(default_idx)
        form.addRow("優先度", self.priority_combo)

        layout.addLayout(form)

        # ボタン
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("保存")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("キャンセル")
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate(self, task: Task) -> None:
        """既存タスクの値をフォームに反映"""
        self.title_edit.setText(task.title)

        if task.due_date:
            self.use_due_date.setChecked(True)
            self.due_date_edit.setDate(
                QDate(task.due_date.year, task.due_date.month, task.due_date.day)
            )

        if task.tag:
            idx = self.tag_combo.findData(task.tag)
            if idx >= 0:
                self.tag_combo.setCurrentIndex(idx)

        idx = self.priority_combo.findData(task.priority)
        if idx >= 0:
            self.priority_combo.setCurrentIndex(idx)

    def _on_accept(self) -> None:
        title = self.title_edit.text().strip()
        if not title:
            self.title_edit.setFocus()
            self.title_edit.setStyleSheet("border: 1px solid #ff5555;")
            return
        self.accept()

    # ──────────────────────────────────────────────
    # 取得プロパティ
    # ──────────────────────────────────────────────

    @property
    def task_title(self) -> str:
        return self.title_edit.text().strip()

    @property
    def task_due_date(self) -> Optional[date]:
        if not self.use_due_date.isChecked():
            return None
        qd = self.due_date_edit.date()
        return date(qd.year(), qd.month(), qd.day())

    @property
    def task_tag(self) -> Optional[str]:
        return self.tag_combo.currentData()

    @property
    def task_priority(self) -> int:
        return self.priority_combo.currentData()
