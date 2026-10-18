"""
Book/Tow 1.1 Theme & Styling Definitions
Primary Brand Color: Orange (#F28C28)
Secondary Colors: White (#FFFFFF), Warm Gray (#F4F4F6), Charcoal (#22252A), Subtle Orange (#FFF3E6 / #FFE8D1)
"""

PRIMARY_ORANGE = "#F28C28"
HOVER_ORANGE = "#E07B17"
DARK_ORANGE = "#D06A06"
LIGHT_ORANGE_BG = "#FFF8F2"
SELECTION_BG = "#FFE8D1"

CHARCOAL = "#22252A"
DARK_GRAY = "#33373E"
LIGHT_GRAY = "#F4F4F6"
BORDER_GRAY = "#D1D5DB"
GRID_LINE_COLOR = "#E2E8F0"
TEXT_DARK = "#1E293B"
TEXT_LIGHT = "#FFFFFF"

APP_QSS = f"""
QMainWindow {{
    background-color: #FAFAFA;
    font-family: "Segoe UI", "SF Pro Text", "Helvetica Neue", sans-serif;
}}

/* Menu Bar */
QMenuBar {{
    background-color: #FFFFFF;
    color: {TEXT_DARK};
    border-bottom: 1px solid {BORDER_GRAY};
    font-size: 13px;
    padding: 2px 5px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 4px 10px;
    border-radius: 4px;
}}

QMenuBar::item:selected {{
    background-color: {LIGHT_ORANGE_BG};
    color: {DARK_ORANGE};
}}

QMenu {{
    background-color: #FFFFFF;
    border: 1px solid {BORDER_GRAY};
    padding: 4px 0px;
    border-radius: 6px;
}}

QMenu::item {{
    padding: 6px 24px 6px 12px;
    font-size: 13px;
    color: {TEXT_DARK};
}}

QMenu::item:selected {{
    background-color: {PRIMARY_ORANGE};
    color: #FFFFFF;
}}

QMenu::separator {{
    height: 1px;
    background: {BORDER_GRAY};
    margin: 4px 0px;
}}

/* Toolbars */
QToolBar {{
    background-color: #FFFFFF;
    border-bottom: 1px solid {BORDER_GRAY};
    spacing: 4px;
    padding: 3px 6px;
}}

QToolButton {{
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 4px;
    font-size: 12px;
    color: {TEXT_DARK};
}}

QToolButton:hover {{
    background-color: {LIGHT_ORANGE_BG};
    border: 1px solid {PRIMARY_ORANGE};
}}

QToolButton:checked {{
    background-color: {SELECTION_BG};
    border: 1px solid {PRIMARY_ORANGE};
    font-weight: bold;
}}

/* ComboBox & Inputs */
QComboBox {{
    background-color: #FFFFFF;
    border: 1px solid {BORDER_GRAY};
    border-radius: 4px;
    padding: 3px 8px;
    min-height: 22px;
    font-size: 12px;
}}

QComboBox:hover {{
    border-color: {PRIMARY_ORANGE};
}}

QLineEdit {{
    background-color: #FFFFFF;
    border: 1px solid {BORDER_GRAY};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 13px;
    color: {TEXT_DARK};
}}

QLineEdit:focus {{
    border: 2px solid {PRIMARY_ORANGE};
}}

/* Formula Bar */
#formulaLabel {{
    font-weight: bold;
    color: {DARK_ORANGE};
    padding: 2px 6px;
    background-color: {LIGHT_ORANGE_BG};
    border: 1px solid {PRIMARY_ORANGE};
    border-radius: 4px;
    font-family: monospace;
}}

/* Table View & Grid */
QTableView {{
    background-color: #FFFFFF;
    gridline-color: {GRID_LINE_COLOR};
    selection-background-color: {SELECTION_BG};
    selection-color: {TEXT_DARK};
    border: 1px solid {BORDER_GRAY};
    font-size: 13px;
}}

QHeaderView::section {{
    background-color: #F8FAFC;
    color: #475569;
    padding: 4px;
    border: 1px solid {GRID_LINE_COLOR};
    font-weight: 600;
    font-size: 12px;
    text-align: center;
}}

QHeaderView::section:checked {{
    background-color: {PRIMARY_ORANGE};
    color: #FFFFFF;
}}

/* Tab Bar */
QTabBar::tab {{
    background-color: #F1F5F9;
    color: #475569;
    border: 1px solid {BORDER_GRAY};
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 6px 16px;
    margin-right: 2px;
    font-weight: 500;
    font-size: 12px;
}}

QTabBar::tab:selected {{
    background-color: #FFFFFF;
    color: {DARK_ORANGE};
    border-top: 3px solid {PRIMARY_ORANGE};
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: {LIGHT_ORANGE_BG};
}}

/* Status Bar */
QStatusBar {{
    background-color: #FFFFFF;
    border-top: 1px solid {BORDER_GRAY};
    color: #64748B;
    font-size: 12px;
    padding: 2px 8px;
}}

/* Dialogs & Buttons */
QPushButton {{
    background-color: {PRIMARY_ORANGE};
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: 600;
    font-size: 13px;
}}

QPushButton:hover {{
    background-color: {HOVER_ORANGE};
}}

QPushButton:pressed {{
    background-color: {DARK_ORANGE};
}}

QPushButton:disabled {{
    background-color: #CBD5E1;
    color: #94A3B8;
}}
"""
