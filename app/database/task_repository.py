"""タスクのCRUD操作を担うリポジトリ"""
import sqlite3
from datetime import date, datetime
from typing import List, Optional

from app.database.connection import get_connection
from app.models.task import Task


def _row_to_task(row: sqlite3.Row) -> Task:
    """DB行をTaskオブジェクトへ変換"""
    due_date = None
    if row["due_date"]:
        due_date = date.fromisoformat(row["due_date"])

    completed_at = None
    if row["completed_at"]:
        completed_at = datetime.fromisoformat(row["completed_at"])

    created_at = datetime.fromisoformat(row["created_at"])

    return Task(
        id=row["id"],
        title=row["title"],
        due_date=due_date,
        tag=row["tag"],
        priority=row["priority"],
        is_completed=bool(row["is_completed"]),
        created_at=created_at,
        completed_at=completed_at,
    )


# ──────────────────────────────────────────────
# 取得系
# ──────────────────────────────────────────────

def get_all_active() -> List[Task]:
    """未完了タスクを優先度降順→期限昇順→作成日昇順で取得"""
    sql = """
        SELECT * FROM tasks
        WHERE is_completed = 0
        ORDER BY priority DESC,
                 CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
                 due_date ASC,
                 created_at ASC
    """
    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()
    return [_row_to_task(r) for r in rows]


def get_all_archived() -> List[Task]:
    """完了済みタスクを完了日時降順で取得"""
    sql = """
        SELECT * FROM tasks
        WHERE is_completed = 1
        ORDER BY completed_at DESC
    """
    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()
    return [_row_to_task(r) for r in rows]


def get_overdue() -> List[Task]:
    """期限切れ未完了タスクを取得"""
    today = date.today().isoformat()
    sql = """
        SELECT * FROM tasks
        WHERE is_completed = 0
          AND due_date IS NOT NULL
          AND due_date < ?
        ORDER BY due_date ASC, priority DESC
    """
    with get_connection() as conn:
        rows = conn.execute(sql, (today,)).fetchall()
    return [_row_to_task(r) for r in rows]


def get_due_today() -> List[Task]:
    """今日期限の未完了タスクを取得"""
    today = date.today().isoformat()
    sql = """
        SELECT * FROM tasks
        WHERE is_completed = 0
          AND due_date = ?
        ORDER BY priority DESC
    """
    with get_connection() as conn:
        rows = conn.execute(sql, (today,)).fetchall()
    return [_row_to_task(r) for r in rows]


def get_high_priority(threshold: int = 4) -> List[Task]:
    """優先度が閾値以上の未完了タスクを取得（デフォルト: 4以上）"""
    sql = """
        SELECT * FROM tasks
        WHERE is_completed = 0
          AND priority >= ?
        ORDER BY priority DESC,
                 CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
                 due_date ASC
    """
    with get_connection() as conn:
        rows = conn.execute(sql, (threshold,)).fetchall()
    return [_row_to_task(r) for r in rows]


# ──────────────────────────────────────────────
# 更新系
# ──────────────────────────────────────────────

def add_task(title: str, due_date: Optional[date], tag: Optional[str], priority: int) -> Task:
    """タスクを追加して追加後のTaskを返す"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    due_str = due_date.isoformat() if due_date else None
    sql = """
        INSERT INTO tasks (title, due_date, tag, priority, is_completed, created_at)
        VALUES (?, ?, ?, ?, 0, ?)
    """
    with get_connection() as conn:
        cur = conn.execute(sql, (title, due_str, tag, priority, now))
        conn.commit()
        task_id = cur.lastrowid
    return Task(
        id=task_id,
        title=title,
        due_date=due_date,
        tag=tag,
        priority=priority,
        is_completed=False,
        created_at=datetime.fromisoformat(now),
        completed_at=None,
    )


def update_task(task_id: int, title: str, due_date: Optional[date], tag: Optional[str], priority: int) -> None:
    """タスクを更新する"""
    due_str = due_date.isoformat() if due_date else None
    sql = """
        UPDATE tasks
        SET title = ?, due_date = ?, tag = ?, priority = ?
        WHERE id = ?
    """
    with get_connection() as conn:
        conn.execute(sql, (title, due_str, tag, priority, task_id))
        conn.commit()


def complete_task(task_id: int) -> None:
    """タスクを完了状態にする"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "UPDATE tasks SET is_completed = 1, completed_at = ? WHERE id = ?"
    with get_connection() as conn:
        conn.execute(sql, (now, task_id))
        conn.commit()


def restore_task(task_id: int) -> None:
    """アーカイブ済みタスクを未完了に戻す"""
    sql = "UPDATE tasks SET is_completed = 0, completed_at = NULL WHERE id = ?"
    with get_connection() as conn:
        conn.execute(sql, (task_id,))
        conn.commit()


def delete_task(task_id: int) -> None:
    """タスクを削除する"""
    sql = "DELETE FROM tasks WHERE id = ?"
    with get_connection() as conn:
        conn.execute(sql, (task_id,))
        conn.commit()
