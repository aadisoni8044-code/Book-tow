from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtGui import (
    QColor, QPainter, QTextFormat, QFont, QKeySequence, QTextCursor,
    QTextDocument, QPen, QSyntaxHighlighter
)
from PySide6.QtCore import QRect, QSize, Qt

from .highlighter import JPSSyntaxHighlighter
from .search_bar import SearchBar


class LineNumberArea(QWidget):
    """Line number area gutter widget displayed on left side of code editor."""

    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class JPSCodeEditor(QPlainTextEdit):
    """Professional JPS Script code editor widget with line numbers, active line highlight, auto-indent, and syntax highlighting."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CodeEditor")

        # Configure Monospace Font
        font = QFont("Consolas", 13)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)

        # Line Number Area Gutter
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Syntax Highlighter
        self.highlighter = JPSSyntaxHighlighter(self.document())

        # Search Bar
        self.search_bar = SearchBar(self)
        self.search_bar.search_requested.connect(self._find_text)

        # Formatting
        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self) -> int:
        digits = 1
        max_val = max(1, self.blockCount())
        while max_val >= 10:
            max_val //= 10
            digits += 1
        space = 20 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, new_block_count):
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
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )
        self.search_bar.setGeometry(
            cr.right() - 320, cr.top() + 10, 310, 40
        )

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#252526"))  # Gutter background

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        current_block_num = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                if block_number == current_block_num:
                    painter.setPen(QColor("#C6C6C6"))  # Active line number
                    painter.setFont(QFont("Consolas", 12, QFont.Bold))
                else:
                    painter.setPen(QColor("#858585"))  # Normal line number
                    painter.setFont(QFont("Consolas", 12))

                painter.drawText(
                    0, top, self.line_number_area.width() - 8,
                    self.fontMetrics().height(), Qt.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self, error_line: int = -1):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#2A2D2E")  # Active line subtle dark highlight
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        if error_line > 0:
            doc = self.document()
            block = doc.findBlockByLineNumber(error_line - 1)
            if block.isValid():
                error_sel = QTextEdit.ExtraSelection()
                error_sel.format.setBackground(QColor("#5A1D1D"))  # Red error line highlight
                error_sel.format.setProperty(QTextFormat.FullWidthSelection, True)
                cursor = QTextCursor(block)
                error_sel.cursor = cursor
                extra_selections.append(error_sel)

        self.setExtraSelections(extra_selections)

    def keyPressEvent(self, event):
        # Shortcut Ctrl+F -> Search Bar
        if event.matches(QKeySequence.Find):
            self.search_bar.show_search()
            return

        # Auto Indentation on Enter key
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            cursor = self.textCursor()
            block_text = cursor.block().text()
            indent = len(block_text) - len(block_text.lstrip())
            super().keyPressEvent(event)
            self.insertPlainText(' ' * indent)
            return

        # Tab inserts 4 spaces
        if event.key() == Qt.Key_Tab:
            self.insertPlainText('    ')
            return

        super().keyPressEvent(event)

    def _find_text(self, text: str, forward: bool):
        flags = QTextDocument.FindFlags()
        if not forward:
            flags |= QTextDocument.FindBackward

        found = self.find(text, flags)
        if not found:
            # Wrap around search
            cursor = self.textCursor()
            if forward:
                cursor.movePosition(QTextCursor.Start)
            else:
                cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            self.find(text, flags)


# Alias QsciScintilla to JPSCodeEditor so QScintilla requirements are met seamlessly
QsciScintilla = JPSCodeEditor
