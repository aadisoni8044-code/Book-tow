"""Branded, non-interactive Book/Tow launch splash screen."""

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from book_tow.app.theme import application_icon


def _asset_path(filename):
    bundle_directory = getattr(sys, "_MEIPASS", os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    return os.path.join(bundle_directory, "assets", filename)


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__(
            None,
            Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Book/Tow")
        self.setFixedSize(440, 330)
        self.setObjectName("SplashCard")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        screen = QApplication.primaryScreen()
        if screen:
            self.move(screen.availableGeometry().center() - self.rect().center())
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "QWidget#SplashCard { background: #202124; color: #F4F0EB; "
            "border: 1px solid #484B50; border-radius: 14px; }"
            "QLabel { background: transparent; border: none; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 28)
        layout.setSpacing(8)
        layout.addStretch(1)

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(self._logo_pixmap(104))
        layout.addWidget(logo)

        title = QLabel("Book/Tow")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 25, QFont.Weight.DemiBold))
        title.setStyleSheet("color: #F28C28; border: none;")
        layout.addWidget(title)

        subtitle = QLabel("Your Workspace, Your Way")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #C4BDB5; border: none;")
        layout.addWidget(subtitle)
        layout.addStretch(1)

        accent = QWidget()
        accent.setFixedHeight(3)
        accent.setStyleSheet("background: #F28C28; border: none;")
        layout.addWidget(accent)

    @staticmethod
    def _logo_pixmap(size):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        renderer = QSvgRenderer(_asset_path("book_tow.svg"))
        if renderer.isValid():
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
        else:
            pixmap = application_icon().pixmap(size, size)
        return pixmap
