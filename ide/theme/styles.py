"""Dark developer theme QSS stylesheet for JPS Script IDE."""

DARK_THEME_QSS = """
QMainWindow {
    background-color: #1E1E1E;
    color: #D4D4D4;
}

QWidget {
    font-family: 'Segoe UI', 'Consolas', sans-serif;
    font-size: 13px;
    color: #D4D4D4;
}

/* Header Bar */
#HeaderBar {
    background-color: #252526;
    border-bottom: 1px solid #333333;
    min-height: 52px;
    max-height: 52px;
    padding: 4px 12px;
}

#AppTitle {
    font-weight: bold;
    font-size: 15px;
    color: #00F0FF;
}

#AppSubtitle {
    font-size: 11px;
    color: #858585;
}

/* Run Button */
QPushButton#RunButton {
    background-color: #0E639C;
    color: #FFFFFF;
    font-weight: bold;
    font-size: 13px;
    padding: 6px 18px;
    border-radius: 4px;
    border: none;
}

QPushButton#RunButton:hover {
    background-color: #1177BB;
}

QPushButton#RunButton:pressed {
    background-color: #094771;
}

/* Code Editor */
QPlainTextEdit#CodeEditor {
    background-color: #1E1E1E;
    color: #D4D4D4;
    border: none;
    font-family: 'Consolas', 'DejaVu Sans Mono', 'Courier New', monospace;
    font-size: 14px;
    selection-background-color: #264F78;
    selection-color: #FFFFFF;
}

/* Terminal Console */
QTextEdit#TerminalView {
    background-color: #181818;
    color: #CCCCCC;
    font-family: 'Consolas', 'DejaVu Sans Mono', 'Courier New', monospace;
    font-size: 13px;
    border: 1px solid #2D2D2D;
    selection-background-color: #264F78;
}

/* Splitter handle */
QSplitter::handle {
    background-color: #2D2D2D;
    height: 3px;
}

QSplitter::handle:hover {
    background-color: #007ACC;
}

/* Search Overlay */
#SearchBar {
    background-color: #252526;
    border: 1px solid #454545;
    border-radius: 4px;
    padding: 4px;
}

QLineEdit {
    background-color: #3C3C3C;
    color: #CCCCCC;
    border: 1px solid #555555;
    border-radius: 2px;
    padding: 3px 6px;
    font-family: 'Consolas', monospace;
}

QLineEdit:focus {
    border: 1px solid #007ACC;
}
"""
