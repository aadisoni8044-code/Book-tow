"""
Theme and QSS Stylesheet configuration for Book/Tow 1.1.
Primary Brand Color: Orange (#F28C28)
Secondary Colors: Warm Gray (#F5F6F8), Charcoal (#2C3038), Dark Charcoal (#1E2128), Off-White (#FAFAFC)
"""

PRIMARY_ORANGE = "#F28C28"
HOVER_ORANGE = "#FA9D3E"
PRESSED_ORANGE = "#D97512"
LIGHT_ORANGE = "#FFF3E8"
BORDER_ORANGE = "#E07B18"

DARK_CHARCOAL = "#1E2128"
CHARCOAL = "#2C3038"
LIGHT_CHARCOAL = "#3F4552"

WARM_GRAY_BG = "#F5F6F8"
GRID_LINE_COLOR = "#D1D5DB"
HEADER_BG = "#EAECEF"
HEADER_SELECTED_BG = "#FCD3A1"

TEXT_DARK = "#1F2937"
TEXT_LIGHT = "#FFFFFF"
TEXT_MUTED = "#6B7280"

APP_STYLESHEET = f"""
QMainWindow {{
    background-color: {WARM_GRAY_BG};
    color: {TEXT_DARK};
}}

/* Menu Bar */
QMenuBar {{
    background-color: {DARK_CHARCOAL};
    color: {TEXT_LIGHT};
    padding: 2px;
    font-size: 13px;
}}

QMenuBar::item {{
    background-color: transparent;
    padding: 6px 12px;
    border-radius: 4px;
}}

QMenuBar::item:selected {{
    background-color: {CHARCOAL};
    color: {PRIMARY_ORANGE};
}}

QMenu {{
    background-color: {DARK_CHARCOAL};
    color: {TEXT_LIGHT};
    border: 1px solid {LIGHT_CHARCOAL};
    border-radius: 6px;
    padding: 4px;
}}

QMenu::item {{
    padding: 6px 24px 6px 12px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {PRIMARY_ORANGE};
    color: {TEXT_LIGHT};
}}

QMenu::separator {{
    height: 1px;
    background-color: {LIGHT_CHARCOAL};
    margin: 4px 0px;
}}

/* Toolbars & Header Bars */
QToolBar {{
    background-color: #FFFFFF;
    border-bottom: 1px solid #E5E7EB;
    spacing: 4px;
    padding: 4px 8px;
}}

QToolButton {{
    background-color: transparent;
    color: {TEXT_DARK};
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 4px 8px;
    font-weight: 500;
}}

QToolButton:hover {{
    background-color: {LIGHT_ORANGE};
    border: 1px solid {BORDER_ORANGE};
    color: {PRESSED_ORANGE};
}}

QToolButton:pressed {{
    background-color: {PRIMARY_ORANGE};
    color: #FFFFFF;
}}

QToolButton:checked {{
    background-color: {LIGHT_ORANGE};
    border: 1px solid {PRIMARY_ORANGE};
    color: {PRESSED_ORANGE};
    font-weight: bold;
}}

/* Form Controls in Toolbar */
QComboBox {{
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 4px;
    padding: 3px 8px;
    min-width: 60px;
    color: {TEXT_DARK};
}}

QComboBox:hover {{
    border-color: {PRIMARY_ORANGE};
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: none;
}}

QLineEdit {{
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 4px;
    padding: 4px 8px;
    color: {TEXT_DARK};
    selection-background-color: {PRIMARY_ORANGE};
    selection-color: #FFFFFF;
}}

QLineEdit:focus {{
    border: 2px solid {PRIMARY_ORANGE};
}}

/* Formula Bar */
#FormulaBarContainer {{
    background-color: #FFFFFF;
    border-bottom: 1px solid #E5E7EB;
    padding: 4px 8px;
}}

#CellAddressLabel {{
    background-color: {WARM_GRAY_BG};
    border: 1px solid #D1D5DB;
    border-radius: 4px;
    padding: 4px 10px;
    font-weight: bold;
    color: {CHARCOAL};
    min-width: 60px;
    alignment: center;
}}

/* Spreadsheet Table & Headers */
QTableView {{
    background-color: #FFFFFF;
    gridline-color: {GRID_LINE_COLOR};
    selection-background-color: rgba(242, 140, 40, 0.25);
    selection-color: {TEXT_DARK};
    border: none;
    outline: none;
}}

QHeaderView::section {{
    background-color: {HEADER_BG};
    color: {TEXT_DARK};
    padding: 4px;
    font-weight: 600;
    border: 1px solid {GRID_LINE_COLOR};
    text-align: center;
}}

QHeaderView::section:checked {{
    background-color: {HEADER_SELECTED_BG};
    color: {PRESSED_ORANGE};
    font-weight: bold;
}}

/* Tabs (Worksheets) */
QTabWidget::pane {{
    border: none;
    background-color: {WARM_GRAY_BG};
}}

QTabBar::tab {{
    background-color: #E5E7EB;
    color: {TEXT_DARK};
    padding: 6px 16px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: #FFFFFF;
    color: {PRIMARY_ORANGE};
    border-bottom: 3px solid {PRIMARY_ORANGE};
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: #D1D5DB;
}}

/* Status Bar */
QStatusBar {{
    background-color: {DARK_CHARCOAL};
    color: #9CA3AF;
    font-size: 12px;
    padding: 2px 8px;
}}

QStatusBar QLabel {{
    color: #E5E7EB;
}}
"""
