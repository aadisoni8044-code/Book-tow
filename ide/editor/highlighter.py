import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression


class JPSSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for JPS Script in PySide6."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # 1. Imports (import.box, import.game, import)
        import_format = QTextCharFormat()
        import_format.setForeground(QColor("#C586C0"))  # Magenta / Purple
        import_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegularExpression(r"\bimport\.(box|game)\b"), import_format))
        self.highlighting_rules.append((QRegularExpression(r"\bimport\b"), import_format))

        # 2. Dotted JPS Functions
        # body_2D.box, size.box, run.box, switch.box, size.game, run.game, print
        jps_func_format = QTextCharFormat()
        jps_func_format.setForeground(QColor("#DCDCAA"))  # Soft Yellow / Gold
        jps_func_format.setFontWeight(QFont.Bold)

        jps_funcs = [
            r"\bbody_2D\.box\b",
            r"\bsize\.box\b",
            r"\brun\.box\b",
            r"\bswitch\.box\b",
            r"\bsize\.game\b",
            r"\brun\.game\b",
            r"\bprint\b",
        ]
        for pattern in jps_funcs:
            self.highlighting_rules.append((QRegularExpression(pattern), jps_func_format))

        # 3. Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))  # Light Green
        self.highlighting_rules.append((QRegularExpression(r"\b\d+(\.\d+)?\b"), number_format))

        # 4. Strings (double and single quotes)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))  # Soft Coral
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # 5. Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))  # Muted Green
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))

        # 6. Identifiers / Variables
        ident_format = QTextCharFormat()
        ident_format.setForeground(QColor("#9CDCFE"))  # Light Cyan/Blue
        self.highlighting_rules.append((QRegularExpression(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"), ident_format))

    def highlightBlock(self, text: str):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
