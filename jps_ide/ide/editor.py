"""
JPS Code Editor
Scintilla-based or PySide6 Syntax-highlighted Monospaced Code Editor for JPS Script.
"""

from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QTextEdit
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QPainter, QTextFormat
from PySide6.QtCore import QRegularExpression, Qt, QRect, QSize

from jps_ide.ide import theme

try:
    from PyQt5.Qsci import QsciScintilla, QsciLexerCustom
    from PyQt5.QtGui import QColor as QColor5, QFont as QFont5
    HAS_QSCI = True
except ImportError:
    HAS_QSCI = False


class JPSSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for PySide6 QPlainTextEdit."""
    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        # Keywords (import.box, import.game)
        kw_fmt = QTextCharFormat()
        kw_fmt.setForeground(QColor(theme.KEYWORD_COLOR))
        kw_fmt.setFontWeight(QFont.Bold)
        self.rules.append((QRegularExpression(r'\b(import\.box|import\.game)\b'), kw_fmt))

        # Built-in methods and functions
        fn_fmt = QTextCharFormat()
        fn_fmt.setForeground(QColor(theme.FUNCTION_COLOR))
        fn_fmt.setFontWeight(QFont.Bold)
        self.rules.append((QRegularExpression(r'\b(body_2D\.box|size\.box|run\.box|switch\.box|size\.game|run\.game|print)\b'), fn_fmt))

        # Strings
        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor(theme.STRING_COLOR))
        self.rules.append((QRegularExpression(r'\".*?\"|\'.*?\''), str_fmt))

        # Numbers
        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor(theme.NUMBER_COLOR))
        self.rules.append((QRegularExpression(r'\b\d+(\.\d+)?\b'), num_fmt))

        # Comments
        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor(theme.COMMENT_COLOR))
        self.rules.append((QRegularExpression(r'#.*'), comment_fmt))

        # Identifiers
        ident_fmt = QTextCharFormat()
        ident_fmt.setForeground(QColor(theme.TEXT_PRIMARY))
        self.rules.append((QRegularExpression(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'), ident_fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            match_iter = pattern.globalMatch(text)
            while match_iter.hasNext():
                match = match_iter.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class LineNumberArea(QWidget):
    """Line number margin component for PySide6 QPlainTextEdit."""
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class PySideEditor(QPlainTextEdit):
    """PySide6 QPlainTextEdit with line numbers & syntax highlighting."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CodeEditor")
        self.setFont(QFont("Consolas", 12))

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlighter = JPSSyntaxHighlighter(self.document())
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 10 + self.fontMetrics().horizontalAdvance('9') * max(3, digits)
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(theme.BG_PANEL)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(theme.BG_PANEL))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(theme.TEXT_MUTED))
                painter.setFont(self.font())
                painter.drawText(0, top, self.line_number_area.width() - 5, self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def get_code(self):
        return self.toPlainText()

    def set_code(self, text):
        self.setPlainText(text)


class CodeEditor(QWidget):
    """Container for the code editor widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.editor = PySideEditor(self)
        layout.addWidget(self.editor)

    def get_code(self):
        return self.editor.get_code()

    def set_code(self, text):
        self.editor.set_code(text)
