"""アプリ共通スタイル定義（ダークモード・ブルーアクセント）"""

# カラーパレット
COLOR_BG_DARK = "#1e1e2e"
COLOR_BG_PANEL = "#2a2a3e"
COLOR_BG_CARD = "#313145"
COLOR_ACCENT = "#4a9eff"
COLOR_ACCENT_HOVER = "#6ab4ff"
COLOR_TEXT_PRIMARY = "#e0e0f0"
COLOR_TEXT_SECONDARY = "#9090b0"
COLOR_TEXT_MUTED = "#606080"
COLOR_DANGER = "#ff5555"
COLOR_WARNING = "#ffaa33"
COLOR_SUCCESS = "#50fa7b"
COLOR_BORDER = "#404060"

APP_STYLESHEET = f"""
QMainWindow, QDialog {{
    background-color: {COLOR_BG_DARK};
    color: {COLOR_TEXT_PRIMARY};
}}

QWidget {{
    background-color: {COLOR_BG_DARK};
    color: {COLOR_TEXT_PRIMARY};
    font-family: "Yu Gothic UI", "Meiryo UI", sans-serif;
    font-size: 13px;
}}

/* ナビゲーションサイドバー */
#sidebar {{
    background-color: {COLOR_BG_PANEL};
    border-right: 1px solid {COLOR_BORDER};
}}

#nav_button {{
    background-color: transparent;
    color: {COLOR_TEXT_SECONDARY};
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    text-align: left;
    font-size: 14px;
}}

#nav_button:hover {{
    background-color: {COLOR_BG_CARD};
    color: {COLOR_TEXT_PRIMARY};
}}

#nav_button[active="true"] {{
    background-color: {COLOR_ACCENT};
    color: white;
}}

/* カード */
#card {{
    background-color: {COLOR_BG_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 8px;
}}

/* セクションタイトル */
#section_title {{
    color: {COLOR_TEXT_PRIMARY};
    font-size: 16px;
    font-weight: bold;
}}

/* タスクアイテム */
#task_item {{
    background-color: {COLOR_BG_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    padding: 6px 10px;
}}

#task_item:hover {{
    border-color: {COLOR_ACCENT};
}}

/* ボタン */
QPushButton {{
    background-color: {COLOR_ACCENT};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 16px;
    font-size: 13px;
}}

QPushButton:hover {{
    background-color: {COLOR_ACCENT_HOVER};
}}

QPushButton:pressed {{
    background-color: {COLOR_ACCENT};
}}

QPushButton#btn_danger {{
    background-color: {COLOR_DANGER};
}}

QPushButton#btn_danger:hover {{
    background-color: #ff7777;
}}

QPushButton#btn_secondary {{
    background-color: {COLOR_BG_CARD};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
}}

QPushButton#btn_secondary:hover {{
    background-color: {COLOR_BORDER};
}}

/* 入力フィールド */
QLineEdit, QComboBox, QDateEdit, QSpinBox {{
    background-color: {COLOR_BG_CARD};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 13px;
}}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus {{
    border-color: {COLOR_ACCENT};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLOR_BG_CARD};
    color: {COLOR_TEXT_PRIMARY};
    selection-background-color: {COLOR_ACCENT};
    border: 1px solid {COLOR_BORDER};
}}

QDateEdit::drop-down {{
    border: none;
    width: 24px;
}}

/* スクロールバー */
QScrollBar:vertical {{
    background: {COLOR_BG_PANEL};
    width: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background: {COLOR_BORDER};
    border-radius: 4px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLOR_ACCENT};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* チェックボックス */
QCheckBox {{
    color: {COLOR_TEXT_PRIMARY};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLOR_BORDER};
    border-radius: 4px;
    background-color: {COLOR_BG_CARD};
}}

QCheckBox::indicator:checked {{
    background-color: {COLOR_ACCENT};
    border-color: {COLOR_ACCENT};
    image: none;
}}

/* ラベル */
QLabel#label_overdue {{
    color: {COLOR_DANGER};
    font-weight: bold;
}}

QLabel#label_today {{
    color: {COLOR_WARNING};
    font-weight: bold;
}}

QLabel#label_important {{
    color: {COLOR_ACCENT};
    font-weight: bold;
}}

/* ダイアログ */
QDialog {{
    background-color: {COLOR_BG_PANEL};
}}

/* セパレーター */
QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    color: {COLOR_BORDER};
}}
"""
