"""Windows トースト通知サービス"""
from typing import List

from app.models.task import Task


def notify_due_today(tasks: List[Task]) -> None:
    """今日期限のタスクをWindows通知で表示する"""
    if not tasks:
        return

    try:
        from winotify import Notification, audio

        task_lines = "\n".join(f"・{t.title}" for t in tasks[:10])
        body = f"今日期限のタスクがあります\n\n{task_lines}"

        toast = Notification(
            app_id="ToDoアプリ",
            title="📋 今日のタスク",
            msg=body,
            duration="short",
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    except Exception:
        # 通知に失敗してもアプリは継続する
        pass
