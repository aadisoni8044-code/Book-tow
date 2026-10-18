import os
import zipfile
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio

os.makedirs("assets", exist_ok=True)
os.makedirs("downloads", exist_ok=True)
os.makedirs("css", exist_ok=True)
os.makedirs("js", exist_ok=True)

# 1. Generate downloads/Booktow.zip
zip_path = os.path.join("downloads", "Booktow.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.writestr("BookTow/README.md", "# Book/Tow Spreadsheet Application v1.1.0\n\nOfficial desktop spreadsheet application with high-performance formula engine and native .btow format support.\n")
    zipf.writestr("BookTow/BookTow.exe", b"BookTow Binary Mock - Portable Desktop Application Executable Version 1.1.0\n" + b"\x00" * 2048)
    zipf.writestr("BookTow/main.py", "import sys\nprint('Starting Book/Tow Spreadsheet Studio...')\n")
    zipf.writestr("BookTow/requirements.txt", "PySide6>=6.5.0\nopenpyxl>=3.1.0\n")
    zipf.writestr("BookTow/LICENSE", "Book/Tow License Agreement - Copyright (c) 2025 Book/Tow Team.\n")

print(f"Created {zip_path} (size: {os.path.getsize(zip_path)} bytes)")

# Helper fonts
def get_font(size, bold=False):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

font_sm = get_font(14)
font_md = get_font(18, bold=True)
font_lg = get_font(28, bold=True)
font_title = get_font(42, bold=True)

# Colors
ORANGE = (242, 140, 40)
ORANGE_DARK = (210, 110, 20)
ORANGE_LIGHT = (254, 243, 230)
CHARCOAL = (30, 32, 37)
DARK_NAVY = (15, 23, 42)
BG_GRAY = (245, 247, 250)
WHITE = (255, 255, 255)
BORDER_GRAY = (220, 225, 230)

# 2. Generate a.png (Logo)
def create_logo():
    width, height = 800, 320
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Icon background (rounded square)
    icon_box = [40, 40, 280, 280]
    draw.rounded_rectangle(icon_box, radius=40, fill=ORANGE)

    # Grid lines inside icon representing spreadsheet & tow hook/book
    # Spreadsheet grid on icon
    grid_rects = [
        [70, 70, 150, 150], [170, 70, 250, 150],
        [70, 170, 150, 250], [170, 170, 250, 250]
    ]
    for i, r in enumerate(grid_rects):
        fill_c = WHITE if i in [0, 3] else (255, 220, 180)
        draw.rounded_rectangle(r, radius=12, fill=fill_c)

    # Draw B/T stylized icon elements
    draw.line([110, 100, 110, 220], fill=ORANGE, width=12)
    draw.line([110, 100, 210, 100], fill=ORANGE, width=12)
    draw.line([110, 160, 190, 160], fill=ORANGE, width=10)

    # Brand Text
    f_brand = get_font(76, bold=True)
    f_sub = get_font(24, bold=False)

    draw.text((320, 90), "Book/Tow", fill=CHARCOAL, font=f_brand)
    draw.text((324, 180), "PREMIUM SPREADSHEET STUDIO", fill=ORANGE_DARK, font=f_sub)

    img.save("assets/a.png")
    print("Created assets/a.png")

create_logo()

# Helper function to draw standard app UI base
def draw_app_frame(draw, width, height, title="Book/Tow Spreadsheet Studio"):
    # Window background
    draw.rectangle([0, 0, width, height], fill=BG_GRAY)

    # Title bar
    draw.rectangle([0, 0, width, 45], fill=CHARCOAL)
    # Window controls
    draw.ellipse([15, 16, 27, 28], fill=(239, 68, 68))
    draw.ellipse([35, 16, 47, 28], fill=(245, 158, 11))
    draw.ellipse([55, 16, 67, 28], fill=(16, 185, 129))
    draw.text((80, 12), title, fill=WHITE, font=font_md)

    # Menu & Toolbar
    draw.rectangle([0, 45, width, 90], fill=WHITE)
    draw.line([0, 90, width, 90], fill=BORDER_GRAY, width=2)

    menus = ["File", "Edit", "View", "Insert", "Format", "Formulas", "Data", "Tools", "Help"]
    x = 20
    for m in menus:
        draw.text((x, 58), m, fill=CHARCOAL, font=font_sm)
        x += 70

    # Quick action toolbar
    draw.rectangle([0, 90, width, 135], fill=ORANGE_LIGHT)
    draw.line([0, 135, width, 135], fill=BORDER_GRAY, width=2)

    tools = ["💾 Save", "↩ Undo", "↪ Redo", "➕ New Sheet", "📊 Insert Chart", "ƒx Function", "🔍 Search", "📤 Export .BTOW"]
    tx = 20
    for t in tools:
        draw.rounded_rectangle([tx, 98, tx + 120, 128], radius=6, fill=WHITE, outline=ORANGE, width=1)
        draw.text((tx + 10, 104), t, fill=CHARCOAL, font=font_sm)
        tx += 130

# 3. Generate b.png (Main Workspace Grid)
def create_b_png():
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw_app_frame(draw, w, h, "Book/Tow — Q4_Financial_Analysis.btow")

    # Formula bar
    draw.rectangle([0, 135, w, 175], fill=WHITE)
    draw.rectangle([10, 142, 70, 168], fill=BG_GRAY, outline=BORDER_GRAY)
    draw.text((22, 146), "C12", fill=ORANGE_DARK, font=font_md)
    draw.rectangle([80, 142, w - 20, 168], fill=WHITE, outline=BORDER_GRAY)
    draw.text((95, 146), "=SUM(C4:C11) * (1 + $B$2)", fill=CHARCOAL, font=font_sm)
    draw.line([0, 175, w, 175], fill=BORDER_GRAY, width=2)

    # Spreadsheet Grid Header
    col_widths = [60, 200, 160, 160, 160, 160, 180]
    cols = ["", "A (Category)", "B (Q1 Revenue)", "C (Q2 Revenue)", "D (Q3 Revenue)", "E (Q4 Target)", "F (Growth %)"]

    x = 0
    for idx, cw in enumerate(col_widths):
        draw.rectangle([x, 175, x + cw, 205], fill=(235, 240, 245), outline=BORDER_GRAY)
        draw.text((x + 10, 182), cols[idx], fill=CHARCOAL, font=font_md)
        x += cw

    # Grid Rows
    rows_data = [
        ("1", "Enterprise Subscriptions", "$124,500", "$148,200", "$162,000", "$185,000", "+22.4%"),
        ("2", "Professional Tier", "$82,100", "$89,400", "$94,300", "$108,000", "+14.5%"),
        ("3", "Custom Integrations", "$45,000", "$52,000", "$61,500", "$70,000", "+13.8%"),
        ("4", "Consulting & Services", "$28,400", "$31,000", "$34,200", "$40,000", "+17.0%"),
        ("5", "API Volume Usage", "$19,800", "$24,100", "$29,600", "$35,500", "+19.9%"),
        ("6", "Support Agreements", "$14,200", "$15,000", "$16,200", "$18,000", "+11.1%"),
        ("7", "Hardware Bundles", "$62,000", "$58,000", "$64,000", "$72,000", "+12.5%"),
        ("8", "Partner Licensing", "$33,500", "$39,000", "$44,100", "$51,000", "+15.6%"),
        ("9", "Training & Certification", "$11,200", "$13,500", "$15,800", "$19,000", "+20.3%"),
        ("10", "Maintenance Renewal", "$48,900", "$51,200", "$53,900", "$58,500", "+8.5%"),
        ("TOTAL", "Combined Gross Revenue", "$469,600", "$521,400", "$575,600", "$657,000", "+14.1%"),
    ]

    y = 205
    for r_idx, row in enumerate(rows_data):
        x = 0
        is_total = (r_idx == len(rows_data) - 1)
        row_bg = ORANGE_LIGHT if is_total else (WHITE if r_idx % 2 == 0 else (250, 252, 255))

        # Active selection highlight on row 3
        if r_idx == 2:
            row_bg = (255, 237, 213)

        for c_idx, cw in enumerate(col_widths):
            cell_bg = (235, 240, 245) if c_idx == 0 else row_bg
            draw.rectangle([x, y, x + cw, y + 42], fill=cell_bg, outline=(242, 140, 40) if (r_idx==2 and c_idx==3) else BORDER_GRAY)

            # Draw active cell border
            if r_idx == 2 and c_idx == 3:
                draw.rectangle([x, y, x + cw, y + 42], outline=ORANGE, width=3)
                draw.rectangle([x + cw - 6, y + 42 - 6, x + cw, y + 42], fill=ORANGE)

            txt = row[c_idx]
            txt_font = font_md if is_total else font_sm
            txt_color = ORANGE_DARK if is_total else CHARCOAL
            draw.text((x + 12, y + 12), txt, fill=txt_color, font=txt_font)
            x += cw
        y += 42

    # Bottom Tab Bar
    draw.rectangle([0, h - 45, w, h], fill=CHARCOAL)
    tabs = ["📁 Q4 Summary (Active)", "📊 Revenue Charts", "⚙️ Raw Data", "📋 Audit Log"]
    tx = 20
    for idx, tab in enumerate(tabs):
        t_bg = ORANGE if idx == 0 else (50, 55, 65)
        draw.rounded_rectangle([tx, h - 38, tx + 180, h - 8], radius=6, fill=t_bg)
        draw.text((tx + 15, h - 30), tab, fill=WHITE, font=font_sm)
        tx += 190

    img.save("assets/b.png")
    print("Created assets/b.png")

create_b_png()

# 4. Generate c.png (Analytics & Charts)
def create_c_png():
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw_app_frame(draw, w, h, "Book/Tow — Interactive Visual Analytics")

    # Grid layout for charts
    draw.rectangle([30, 150, 620, 640], fill=WHITE, outline=BORDER_GRAY, width=2)
    draw.rectangle([650, 150, 1250, 640], fill=WHITE, outline=BORDER_GRAY, width=2)

    # Left Chart: Revenue Trend (Bar chart)
    draw.text((50, 170), "Quarterly Revenue Growth ($K)", fill=CHARCOAL, font=font_lg)

    quarters = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024 (Proj)"]
    vals = [469, 521, 575, 657]
    max_val = 700

    bx = 90
    for q, v in zip(quarters, vals):
        bar_h = int((v / max_val) * 320)
        by = 560 - bar_h
        draw.rectangle([bx, by, bx + 80, 560], fill=ORANGE, outline=ORANGE_DARK)
        draw.text((bx + 15, by - 25), f"${v}K", fill=CHARCOAL, font=font_md)
        draw.text((bx + 10, 575), q, fill=CHARCOAL, font=font_sm)
        bx += 130

    draw.line([70, 560, 590, 560], fill=CHARCOAL, width=2)

    # Right Chart: Category Distribution (Line / Area Chart)
    draw.text((670, 170), "Margin & Performance Metrics", fill=CHARCOAL, font=font_lg)

    points = [(720, 500), (820, 420), (920, 350), (1020, 280), (1120, 220)]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=ORANGE, width=5)
        draw.ellipse([points[i][0]-8, points[i][1]-8, points[i][0]+8, points[i][1]+8], fill=ORANGE_DARK)
    draw.ellipse([points[-1][0]-8, points[-1][1]-8, points[-1][0]+8, points[-1][1]+8], fill=ORANGE_DARK)

    labels = ["Jan", "Apr", "Jul", "Oct", "Dec"]
    for pt, lbl in zip(points, labels):
        draw.text((pt[0]-15, 540), lbl, fill=CHARCOAL, font=font_sm)

    draw.line([700, 520, 1200, 520], fill=BORDER_GRAY, width=1)
    draw.line([700, 400, 1200, 400], fill=BORDER_GRAY, width=1)
    draw.line([700, 280, 1200, 280], fill=BORDER_GRAY, width=1)

    # Status Bar
    draw.rectangle([0, h - 45, w, h], fill=CHARCOAL)
    draw.text((20, h - 30), "GPU Accelerated Rendering • 60 FPS • Real-time Data Sync", fill=WHITE, font=font_sm)

    img.save("assets/c.png")
    print("Created assets/c.png")

create_c_png()

# 5. Generate d.png (Formula Assistant)
def create_d_png():
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw_app_frame(draw, w, h, "Book/Tow — Pratt AST Formula Engine & Assistant")

    # Main formula modal panel
    draw.rectangle([100, 160, 1180, 640], fill=WHITE, outline=ORANGE, width=3)
    draw.rectangle([100, 160, 1180, 220], fill=ORANGE_LIGHT)
    draw.text((130, 178), "⚡ Book/Tow Intelligent Formula Assistant & Library", fill=ORANGE_DARK, font=font_lg)

    # Left column: Function category search
    draw.rectangle([130, 240, 450, 610], fill=BG_GRAY, outline=BORDER_GRAY)
    funcs = ["XLOOKUP(lookup_value, ...)", "FINANCIAL_IRR(values)", "INDEX_MATCH(range)", "DYNAMIC_FILTER(array)", "SAFE_DIVIDE(a, b)", "COMPOUND_INTEREST()"]
    fy = 260
    for idx, f in enumerate(funcs):
        bg = ORANGE if idx == 0 else WHITE
        fg = WHITE if idx == 0 else CHARCOAL
        draw.rounded_rectangle([140, fy, 440, fy + 45], radius=6, fill=bg, outline=BORDER_GRAY)
        draw.text((155, fy + 12), f, fill=fg, font=font_sm)
        fy += 55

    # Right column: Function details and execution preview
    draw.rectangle([470, 240, 1150, 610], fill=WHITE, outline=BORDER_GRAY)
    draw.text((490, 260), "Function: XLOOKUP", fill=CHARCOAL, font=font_lg)
    draw.text((490, 305), "Performs high-speed exact or approximate array matching with zero eval/exec risk.", fill=CHARCOAL, font=font_sm)

    draw.rectangle([490, 350, 1130, 450], fill=DARK_NAVY)
    draw.text((510, 370), "Expression Preview:", fill=(255, 200, 100), font=font_sm)
    draw.text((510, 400), "=XLOOKUP(B12, Revenue_Table[ID], Revenue_Table[Q4_Target], 'Not Found')", fill=(100, 255, 180), font=font_md)

    draw.text((490, 470), "Evaluated Result: $185,000.00 [Type: Currency]", fill=(16, 185, 129), font=font_md)

    draw.rounded_rectangle([490, 530, 660, 580], radius=8, fill=ORANGE)
    draw.text((520, 545), "Insert to Cell", fill=WHITE, font=font_md)

    draw.rectangle([0, h - 45, w, h], fill=CHARCOAL)
    draw.text((20, h - 30), "Pratt Parser Engine • Zero Arbitrary Code Execution • Safe Math Sandbox", fill=WHITE, font=font_sm)

    img.save("assets/d.png")
    print("Created assets/d.png")

create_d_png()

# 6. Generate e.png (Export Settings & Native Format)
def create_e_png():
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw_app_frame(draw, w, h, "Book/Tow — Native .BTOW & Universal Export")

    # Dialog box
    draw.rectangle([250, 160, 1030, 620], fill=WHITE, outline=CHARCOAL, width=3)
    draw.rectangle([250, 160, 1030, 220], fill=CHARCOAL)
    draw.text((280, 178), "📤 Export Document & Data Package", fill=WHITE, font=font_lg)

    options = [
        ("Book/Tow Native Package (.btow)", "Includes full formatting, formula AST graph, undo history & metadata.", True),
        ("Microsoft Excel Spreadsheet (.xlsx)", "High compatibility standard workbook format.", False),
        ("Comma Separated Values (.csv)", "Plain text raw data export.", False),
        ("PDF Report Document (.pdf)", "Vector formatted printable presentation layout.", False)
    ]

    oy = 240
    for title, desc, active in options:
        bg = ORANGE_LIGHT if active else BG_GRAY
        border = ORANGE if active else BORDER_GRAY
        draw.rounded_rectangle([280, oy, 1000, oy + 70], radius=8, fill=bg, outline=border, width=2)

        # Radio button
        r_fill = ORANGE if active else WHITE
        draw.ellipse([300, oy + 25, 320, oy + 45], fill=r_fill, outline=ORANGE if active else BORDER_GRAY, width=2)

        draw.text((340, oy + 12), title, fill=CHARCOAL, font=font_md)
        draw.text((340, oy + 40), desc, fill=(100, 110, 120), font=font_sm)
        oy += 85

    draw.rounded_rectangle([780, 545, 990, 595], radius=8, fill=ORANGE)
    draw.text((820, 560), "Export Now", fill=WHITE, font=font_md)

    draw.rectangle([0, h - 45, w, h], fill=CHARCOAL)
    draw.text((20, h - 30), "Fast Multi-threaded Compression • Full Data Integrity", fill=WHITE, font=font_sm)

    img.save("assets/e.png")
    print("Created assets/e.png")

create_e_png()

# 7. Generate HD MP4 Videos (a.mp4 & b.mp4) using imageio + imageio_ffmpeg
def create_videos():
    fps = 30
    duration = 4  # 4 seconds
    num_frames = fps * duration
    w, h = 1280, 720

    print("Generating a.mp4 (Grid Interaction & Scrolling Video)...")
    writer_a = imageio.get_writer("assets/a.mp4", fps=fps, codec="libx264", quality=8)

    # Load b.png image as frame base
    base_img = Image.open("assets/b.png").convert("RGB")

    for i in range(num_frames):
        frame = base_img.copy()
        draw = ImageDraw.Draw(frame)

        # Animate active cell highlight moving down the rows
        row_idx = (i // 12) % 9
        y_pos = 205 + row_idx * 42

        # Highlight current row
        draw.rectangle([60, y_pos, 1180, y_pos + 42], outline=ORANGE, width=3)

        # Animated cursor pulse
        pulse_alpha = int(127 + 127 * np.sin(i * 0.2))
        draw.rectangle([260, y_pos, 420, y_pos + 42], fill=(255, 220, 180, pulse_alpha) if pulse_alpha > 128 else None, outline=ORANGE_DARK, width=2)

        # Formula update overlay text
        draw.rectangle([80, 142, w - 20, 168], fill=WHITE, outline=ORANGE, width=2)
        draw.text((95, 146), f"=SUM(C2:C{row_idx + 2}) * 1.15 — Live Evaluating...", fill=ORANGE_DARK, font=font_sm)

        frame_np = np.array(frame)
        writer_a.append_data(frame_np)

    writer_a.close()
    print("Created assets/a.mp4")

    print("Generating b.mp4 (Interactive Visual Analytics Video)...")
    writer_b = imageio.get_writer("assets/b.mp4", fps=fps, codec="libx264", quality=8)

    base_analytics = Image.open("assets/c.png").convert("RGB")

    for i in range(num_frames):
        frame = base_analytics.copy()
        draw = ImageDraw.Draw(frame)

        # Animate chart bar heights rising dynamically
        progress = np.sin((i / num_frames) * np.pi)
        quarters = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024 (Proj)"]
        vals = [469, 521, 575, int(657 + progress * 50)]
        max_val = 750

        bx = 90
        # Redraw chart section cleanly
        draw.rectangle([35, 210, 610, 560], fill=WHITE)
        for q, v in zip(quarters, vals):
            bar_h = int((v / max_val) * 300)
            by = 560 - bar_h
            draw.rectangle([bx, by, bx + 80, 560], fill=ORANGE, outline=ORANGE_DARK)
            draw.text((bx + 15, by - 25), f"${v}K", fill=CHARCOAL, font=font_md)
            draw.text((bx + 10, 575), q, fill=CHARCOAL, font=font_sm)
            bx += 130
        draw.line([70, 560, 590, 560], fill=CHARCOAL, width=2)

        frame_np = np.array(frame)
        writer_b.append_data(frame_np)

    writer_b.close()
    print("Created assets/b.mp4")

create_videos()
print("All assets generated successfully!")
