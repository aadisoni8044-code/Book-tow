@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON=py -3"
) else (
    set "PYTHON=python"
)

%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install the build dependencies.
    exit /b 1
)

%PYTHON% -m PyInstaller --noconfirm --clean --windowed --onedir --name Booktow --icon "%CD%\assets\book_tow.ico" --version-file "%CD%\scripts\windows_version_info.txt" --add-data "%CD%\licenses\THIRD_PARTY_NOTICES.txt;licenses" --add-data "%CD%\assets\book_tow.svg;assets" --distpath "build\windows-onedir" --workpath "build\pyinstaller-onedir" --specpath "build\spec" "main.py"
if errorlevel 1 (
    echo The one-folder build failed.
    exit /b 1
)

"build\windows-onedir\Booktow\Booktow.exe" --smoke-test
if errorlevel 1 (
    echo The one-folder executable failed its startup smoke test.
    exit /b 1
)

%PYTHON% -m PyInstaller --noconfirm --clean --windowed --onefile --name Booktow --icon "%CD%\assets\book_tow.ico" --version-file "%CD%\scripts\windows_version_info.txt" --add-data "%CD%\licenses\THIRD_PARTY_NOTICES.txt;licenses" --add-data "%CD%\assets\book_tow.svg;assets" --distpath "dist" --workpath "build\pyinstaller-onefile" --specpath "build\spec" "main.py"
if errorlevel 1 (
    echo The single-file build failed.
    exit /b 1
)

echo Build complete: dist\Booktow.exe
endlocal
