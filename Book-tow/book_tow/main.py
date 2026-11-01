"""Application entry point."""

import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from book_tow import __version__
from book_tow.app.error_logging import (
    configure_error_logging, log_file_operation_error,
)
from book_tow.app.main_window import MainWindow
from book_tow.app.splash_screen import SplashScreen
from book_tow.app.theme import apply_theme, application_icon, load_saved_theme
from book_tow.app.windows_association import register_file_association


def main():
    arguments = sys.argv[1:]
    if "--register-file-association" in arguments:
        application = QApplication.instance() or QApplication([sys.argv[0]])
        try:
            register_file_association()
        except OSError as error:
            QMessageBox.critical(
                None, "File Association Not Registered",
                "Book/Tow could not register .booktow files: {}".format(error))
            return 1
        QMessageBox.information(
            None, "File Association Registered",
            "Book/Tow is registered to open .booktow projects for this Windows "
            "account. If needed, choose Book/Tow under Windows Settings > "
            "Default apps.")
        return 0
    smoke_test = "--smoke-test" in arguments
    project_path = next(
        (argument for argument in arguments if not argument.startswith("--")), None)
    application = QApplication.instance() or QApplication([sys.argv[0]])
    application.setApplicationName("Book/Tow")
    application.setApplicationDisplayName("Book/Tow")
    application.setApplicationVersion(__version__)
    application.setOrganizationName("Book/Tow")
    application.setWindowIcon(application_icon())
    configure_error_logging()
    apply_theme(application, load_saved_theme())
    if smoke_test:
        window = MainWindow()
        window.show()
        QTimer.singleShot(500, application.quit)
        return application.exec()

    splash = SplashScreen()
    splash.show()
    application.processEvents()
    try:
        window = MainWindow()
    except Exception as error:
        splash.close()
        log_file_operation_error("startup", error)
        QMessageBox.critical(
            None, "Unable to Start Book/Tow",
            "Book/Tow could not initialize its main window. Check the "
            "application log for diagnostic details.")
        return 1

    def show_main_window():
        splash.close()
        window.show()
        if project_path:
            QTimer.singleShot(
                0, lambda: window.open_project_path(project_path))
        else:
            QTimer.singleShot(0, window.check_for_recovery)

    QTimer.singleShot(4000, show_main_window)
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
