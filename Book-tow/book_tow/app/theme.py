"""Book/Tow's original orange visual identity."""

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap


ORANGE = "#F28C28"
THEME_SETTING_KEY = "appearance/theme"
THEMES = ("light", "dark")


def application_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(ORANGE))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QPen(QColor("#FFFFFF"), 3))
    painter.setBrush(QColor("#FFFFFF"))
    painter.drawRoundedRect(13, 10, 38, 44, 5, 5)
    painter.setPen(QPen(QColor(ORANGE), 2))
    for y in (23, 32, 41):
        painter.drawLine(21, y, 43, y)
    painter.drawLine(28, 18, 28, 47)
    painter.end()
    return QIcon(pixmap)


def load_saved_theme(settings=None):
    settings = settings or QSettings("Book/Tow", "Book/Tow")
    theme = settings.value(THEME_SETTING_KEY, "light")
    return theme if theme in THEMES else "light"


def save_theme_preference(theme, settings=None):
    if theme not in THEMES:
        raise ValueError("Unsupported application theme.")
    settings = settings or QSettings("Book/Tow", "Book/Tow")
    settings.setValue(THEME_SETTING_KEY, theme)
    settings.sync()
    if settings.status() != QSettings.Status.NoError:
        raise OSError("Could not save the appearance setting.")


def apply_theme(application, mode="light"):
    if mode not in THEMES:
        raise ValueError("Unsupported application theme.")

    application.setStyle("Fusion")
    if mode == "dark":
        application.setStyleSheet("""
            QWidget { color: #E8E4DE; font-family: "Segoe UI", "Noto Sans", sans-serif; }
            QMainWindow, QDialog { background: #252628; }
            QMenuBar { background: #2D2F32; border-bottom: 1px solid #414347; }
            QMenuBar::item { padding: 7px 10px; }
            QMenuBar::item:selected, QMenu::item:selected { background: #594127; color: #FFD0A0; }
            QMenu { background: #303236; border: 1px solid #505258; padding: 4px; }
            QToolBar { background: #2D2F32; border: none; border-bottom: 1px solid #414347; spacing: 6px; padding: 7px; }
            QToolButton { background: transparent; border: 1px solid transparent; border-radius: 4px; padding: 5px 7px; }
            QToolButton:hover { background: #494038; border-color: #8A633E; }
            QToolButton:checked { background: #594127; border-color: #F28C28; }
            QComboBox, QLineEdit, QSpinBox { background: #202124; color: #E8E4DE; border: 1px solid #505258; border-radius: 4px; padding: 5px 7px; }
            QComboBox:focus, QLineEdit:focus, QSpinBox:focus { border: 1px solid #F28C28; }
            QComboBox QAbstractItemView { background: #303236; color: #E8E4DE; selection-background-color: #594127; }
            QTableView { background: #202124; alternate-background-color: #26282B; color: #E8E4DE; gridline-color: #484B50; selection-background-color: #65451F; selection-color: #FFFFFF; border: none; }
            QTableView::item:selected { border: 1px solid #F28C28; }
            QHeaderView::section { background: #303236; color: #D5D0C9; border: none; border-right: 1px solid #484B50; border-bottom: 1px solid #484B50; padding: 5px; }
            QStatusBar { background: #2D2F32; border-top: 1px solid #414347; }
            QTabBar::tab { background: #34363A; color: #D5D0C9; padding: 8px 18px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #202124; color: #FFFFFF; border-top: 2px solid #F28C28; }
            QToolTip { background: #3A3C40; color: #FFFFFF; border: 1px solid #606268; padding: 5px; }
        """)
        application.setProperty("bookTowTheme", "dark")
        return

    application.setStyleSheet("""
        QWidget { color: #302D2A; font-family: "Segoe UI", "Noto Sans", sans-serif; }
        QMainWindow, QDialog { background: #F7F6F4; }
        QMenuBar { background: #FFFFFF; border-bottom: 1px solid #E8E3DD; }
        QMenuBar::item { padding: 7px 10px; }
        QMenuBar::item:selected, QMenu::item:selected { background: #FFF0E0; color: #A64B00; }
        QMenu { background: #FFFFFF; border: 1px solid #E2DDD6; padding: 4px; }
        QToolBar { background: #FFFFFF; border: none; border-bottom: 1px solid #E8E3DD; spacing: 6px; padding: 7px; }
        QToolButton { background: transparent; border: 1px solid transparent; border-radius: 4px; padding: 5px 7px; }
        QToolButton:hover { background: #FFF0E0; border-color: #F5C899; }
        QToolButton:checked { background: #FFE3C2; border-color: #F28C28; }
        QComboBox, QLineEdit, QSpinBox { background: #FFFFFF; border: 1px solid #DDD7CF; border-radius: 4px; padding: 5px 7px; }
        QComboBox:focus, QLineEdit:focus, QSpinBox:focus { border: 1px solid #F28C28; }
        QTableView { background: #FFFFFF; alternate-background-color: #FCFBFA; gridline-color: #E9E5DF; selection-background-color: #FCE6D0; selection-color: #302D2A; border: none; }
        QTableView::item:selected { border: 1px solid #F28C28; }
        QHeaderView::section { background: #F4F2EF; color: #615B54; border: none; border-right: 1px solid #E3DFD9; border-bottom: 1px solid #E3DFD9; padding: 5px; }
        QStatusBar { background: #FFFFFF; border-top: 1px solid #E8E3DD; }
        QTabBar::tab { background: #EEEAE5; padding: 8px 18px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
        QTabBar::tab:selected { background: #FFFFFF; border-top: 2px solid #F28C28; }
        QToolTip { background: #302D2A; color: white; border: none; padding: 5px; }
    """)
    application.setProperty("bookTowTheme", "light")
