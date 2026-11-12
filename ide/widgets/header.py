import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Signal, Qt


class HeaderBar(QWidget):
    """Header bar featuring the official JPS Script logo, branding, and Run button."""

    run_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HeaderBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 6, 16, 6)
        layout.setSpacing(12)

        # Official Logo Image
        logo_label = QLabel(self)
        logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(38, 38, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)

        layout.addWidget(logo_label)

        # Title and Subtitle Container
        title_container = QWidget(self)
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)

        app_title = QLabel("JPS Script", title_container)
        app_title.setObjectName("AppTitle")

        app_badge = QLabel("PROFESSIONAL IDE", title_container)
        app_badge.setStyleSheet("""
            background-color: #007ACC;
            color: #FFFFFF;
            font-size: 10px;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 3px;
        """)

        title_layout.addWidget(app_title)
        title_layout.addWidget(app_badge)
        title_layout.addStretch()

        layout.addWidget(title_container)

        layout.addStretch()

        # Run Button
        self.btn_run = QPushButton("▶  Run", self)
        self.btn_run.setObjectName("RunButton")
        self.btn_run.setCursor(Qt.PointingHandCursor)
        self.btn_run.clicked.connect(self.run_requested.emit)

        layout.addWidget(self.btn_run)
