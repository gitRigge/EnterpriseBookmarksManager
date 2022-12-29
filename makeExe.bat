@echo off
REM The MIT License (MIT)
REM 
REM Copyright (c) 2023, Roland Rickborn (r_2@gmx.net)
REM
REM Permission is hereby granted, free of charge, to any person obtaining a copy
REM of this software and associated documentation files (the "Software"), to deal
REM in the Software without restriction, including without limitation the rights
REM to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
REM copies of the Software, and to permit persons to whom the Software is
REM furnished to do so, subject to the following conditions:
REM 
REM The above copyright notice and this permission notice shall be included in
REM all copies or substantial portions of the Software.
REM 
REM THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
REM IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
REM FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
REM AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
REM LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
REM OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
REM THE SOFTWARE.
REM
REM ---------------------------------------------------------------------------
TITLE Build Executable
setlocal enabledelayedexpansion
echo Set Python Path Variables
set PATH=c:\Python310\;c:\Python310\Lib\site-packages\;c:\Python310\Scripts\;%PATH%
set PYTHONPATH=c:\Python310\Lib\
set PYTHONHOME=c:\Python310\
echo Install Requirements
pip install -r requirements.txt
echo Run Tests
coverage run -m pytest .\tests
if %ERRORLEVEL% == 0 (
    coverage report -m
    echo Build Executable
    IF EXIST release\enterprise_bookmarks_manager.zip DEL /F release\enterprise_bookmarks_manager.zip
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
) else (
    echo There were Errors in Tests - Abort
)
pause