"""
JPS IDE Dark Developer Theme
Defines styles and colors for the IDE user interface.
"""

# Palette Colors
BG_DARK = "#1E1E1E"
BG_PANEL = "#252526"
BG_EDITOR = "#1E1E1E"
BG_TERMINAL = "#181818"
BORDER_COLOR = "#3C3C3C"

TEXT_PRIMARY = "#D4D4D4"
TEXT_MUTED = "#858585"
ACCENT_BLUE = "#007ACC"
ACCENT_HOVER = "#0098FF"
ACCENT_PRESSED = "#005A9E"

KEYWORD_COLOR = "#569CD6"
FUNCTION_COLOR = "#DCDCAA"
STRING_COLOR = "#CE9178"
NUMBER_COLOR = "#B5CEA8"
COMMENT_COLOR = "#6A9955"
ERROR_COLOR = "#F48771"
SUCCESS_COLOR = "#89D185"

MAIN_STYLESHEET = f"""
QMainWindow {{
    background-color: {BG_DARK};
}}

QWidget {{
    color: {TEXT_PRIMARY};
    font-family: 'Consolas', 'Segoe UI', 'Monaco', 'Courier New', monospace;
}}

/* Header Panel */
QFrame#HeaderPanel {{
    background-color: {BG_PANEL};
    border-bottom: 1px solid {BORDER_COLOR};
    padding: 6px;
}}

/* Run Button */
QPushButton#RunButton {{
    background-color: {ACCENT_BLUE};
    color: #FFFFFF;
    font-weight: bold;
    font-size: 14px;
    border: none;
    border-radius: 4px;
    padding: 8px 24px;
}}

QPushButton#RunButton:hover {{
    background-color: {ACCENT_HOVER};
}}

QPushButton#RunButton:pressed {{
    background-color: {ACCENT_PRESSED};
}}

/* Clear Button */
QPushButton#ClearButton {{
    background-color: transparent;
    color: {TEXT_MUTED};
    font-size: 12px;
    border: 1px solid {BORDER_COLOR};
    border-radius: 3px;
    padding: 4px 10px;
}}

QPushButton#ClearButton:hover {{
    color: {TEXT_PRIMARY};
    background-color: #2A2D2E;
}}

/* Code Editor */
QPlainTextEdit#CodeEditor {{
    background-color: {BG_EDITOR};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    font-size: 14px;
    line-height: 1.4;
    selection-background-color: #264F78;
    selection-color: #FFFFFF;
}}

/* Terminal Output */
QTextEdit#Terminal {{
    background-color: {BG_TERMINAL};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    font-size: 13px;
    selection-background-color: #264F78;
    selection-color: #FFFFFF;
}}

QSplitter::handle {{
    background-color: {BORDER_COLOR};
    height: 2px;
}}
"""
