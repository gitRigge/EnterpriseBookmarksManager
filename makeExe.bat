@echo off
TITLE Build Executable
set PATH=c:\Python310\;c:\Python310\Lib\site-packages\;c:\Python310\Scripts\;%PATH%
set PYTHONPATH=c:\Python310\Lib\
set PYTHONHOME=c:\Python310\
rmdir /Q /S release
pyinstaller ^
    --onefile ^
    --distpath bin ^
    --clean ^
    --log-level INFO ^
    --name enterprise_bookmarks_manager ^
    --distpath release ^
    --hidden-import openpyxl ^
    --hidden-import xls2bm ^
    --hidden-import bm2xls ^
    --hidden-import enums ^
    --hidden-import utils ^
    enterprise_bookmarks_manager.py
powershell Compress-Archive release\enterprise_bookmarks_manager.exe release\enterprise_bookmarks_manager.zip
del release\enterprise_bookmarks_manager.exe
del /F /Q enterprise_bookmarks_manager.spec
rmdir /Q /S __pycache__
rmdir /Q /S build
pause