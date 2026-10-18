# Book/Tow 1.1 — Cross-Platform Desktop Spreadsheet Software

**Book/Tow 1.1** is a cross-platform desktop spreadsheet application inspired by Microsoft Excel, featuring its own original orange visual identity (`#F28C28`).

---

## Key Features

- **Spreadsheet Grid**: 100 rows by 26 columns (A-Z) grid, dynamically expandable.
- **Dedicated Formula Engine**: Safely evaluates math expressions without `eval()` or `exec()`. Supports operators (`+`, `-`, `*`, `/`, `^`), parenthesized grouping, cell references (`A1`, `B2`), cell ranges (`A1:C10`), and functions (`SUM`, `AVERAGE`, `COUNT`, `MIN`, `MAX`, `ABS`, `ROUND`, `IF`).
- **Cell Formatting**: Custom font choices, sizes, bold, italic, underline, text colors, cell fill background colors, alignments, and number formats (General, Number, Currency, Percentage, Plain Text).
- **Undo / Redo & Selection**: Full command history for edits and styling, cut/copy/paste, and status bar live range aggregations (`SUM`, `AVERAGE`, `COUNT`).
- **File Format (.btow)**: Native JSON document format with versioning (`1.1`), safe atomic writes, schema validation, and CSV import/export.
- **Multi-Worksheet**: Tabbed interface to manage multiple worksheets within a single workbook.

---

## File Format (.btow) Structure

The `.btow` document format uses JSON encoding with atomic write guarantees:

```json
{
  "app": "Book/Tow",
  "version": "1.1",
  "sheets": [
    {
      "name": "Sheet1",
      "rows": 100,
      "cols": 26,
      "cells": {
        "A1": {
          "raw": "=SUM(B1:B10)",
          "style": {
            "font_family": "Segoe UI",
            "font_size": 10,
            "bold": true,
            "italic": false,
            "underline": false,
            "align": 1,
            "text_color": "#1F2937",
            "bg_color": "#FFF3E8",
            "num_format": "Currency"
          }
        }
      }
    }
  ]
}
```

---

## Installation & Running

### Requirements
- Python 3.10+
- PySide6

### Development Setup
```bash
pip install -r requirements.txt
python3 main.py
```

### Running Tests
```bash
PYTHONPATH=. QT_QPA_PLATFORM=offscreen pytest -v
```

---

## Packaging

To package Book/Tow 1.1 into a standalone desktop bundle using PyInstaller:

```bash
pyinstaller --noconfirm book_tow.spec
```
