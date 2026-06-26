"""タスクモデル定義"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


# 固定タグ一覧
TAGS = ["仕事", "個人", "開発", "勉強", "買い物", "その他"]

# 優先度ラベル（1=最低, 5=最高）
PRIORITY_LABELS = {
    5: "★★★★★",
    4: "★★★★☆",
    3: "★★★☆☆",
    2: "★★☆☆☆",
    1: "★☆☆☆☆",
}

DEFAULT_PRIORITY = 3


@dataclass
class Task:
    """タスクデータクラス"""
    id: Optional[int]
    title: str
    due_date: Optional[date]
    tag: Optional[str]
    priority: int
    is_completed: bool
    created_at: datetime
    completed_at: Optional[datetime]

    @property
    def priority_label(self) -> str:
        return PRIORITY_LABELS.get(self.priority, "★★★☆☆")

    @property
    def is_overdue(self) -> bool:
        """期限切れかどうか（未完了かつ期限が今日より前）"""
        if self.is_completed or self.due_date is None:
            return False
        return self.due_date < date.today()

    @property
    def is_due_today(self) -> bool:
        """今日期限かどうか"""
        if self.is_completed or self.due_date is None:
            return False
        return self.due_date == date.today()
