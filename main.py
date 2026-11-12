import sys
import os
import argparse
from PySide6.QtWidgets import QApplication
from ide.app import JPSMainWindow


def main():
    parser = argparse.ArgumentParser(description="JPS Script Professional IDE")
    parser.add_argument("--test-launch", action="store_true", help="Launch IDE window headlessly and exit immediately (for test verification)")
    args, unknown = parser.parse_known_args()

    app = QApplication(sys.argv)
    window = JPSMainWindow()

    if args.test_launch:
        window.show()
        print("[JPS IDE] Test launch successful.")
        sys.exit(0)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
