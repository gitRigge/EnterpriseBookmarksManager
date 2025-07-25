@echo off
REM The MIT License (MIT)
REM 
REM Copyright (c) 2025, Roland Rickborn (r_2@gmx.net)
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

setlocal EnableDelayedExpansion
echo [1mInstall Requirements[0m
python.exe -m pip install --upgrade pip
python -m pip install -r requirements.txt
GOTO :TESTING

:TESTING
echo [1mRun Tests[0m
rmdir /Q /S coverage
tox
if %ERRORLEVEL% == 0 (
    echo [1mPrint Coverage Report[0m
    coverage report -m
    GOTO :VERSIONFILE
) else (
    echo [1mThere were Errors in Tests - Abort[0m
    GOTO :DONE
)

:VERSIONFILE
echo [1mCreate Version File[0m
@SET AUTHOR=
FOR /F "tokens=9-10" %%I IN ('python .\src\ebm\enterprise_bookmarks_manager.py -l') DO @SET "AUTHOR=%%I %%J"
@SET COPYRIGHT=
FOR /F "tokens=2 delims=," %%I IN ('python .\src\ebm\enterprise_bookmarks_manager.py -l') DO @SET "COPYRIGHT=%%I"
@SET VERSION=
FOR /F "tokens=2" %%I IN ('python .\src\ebm\enterprise_bookmarks_manager.py --version') DO @SET "VERSION=%%I"
pyivf-make_version --outfile VERSION --version %VERSION% --company-name "%AUTHOR%" --file-description "M365 Enterprise Bookmark Manager" --internal-name enterprise_bookmarks_manager --legal-copyright "%COPYRIGHT%" --original-filename enterprise_bookmarks_manager.exe --product-name enterprise_bookmarks_manager
IF EXIST VERSION (
    echo [1mVersion File created[0m
    GOTO :BUILDING
) else (
    echo [1mThere was an Error creating the Version File - Abort[0m
    GOTO :DONE
)

:BUILDING
if %ERRORLEVEL% == 0 (
    echo [1mBuild Executable[0m
    IF EXIST release\enterprise_bookmarks_manager.zip DEL /F release\enterprise_bookmarks_manager.zip
    pyinstaller ^
        --onefile ^
        --distpath .\release ^
        --workpath .\build ^
        --version-file %cd%\VERSION ^
        --paths %cd%\src\ebm\ ^
        --clean ^
        --log-level INFO ^
        --name enterprise_bookmarks_manager ^
        --hidden-import openpyxl ^
        --hidden-import validators ^
        --hidden-import pycountry ^
        --add-data %cd%\src\ebm\*.py;src\ebm\ ^
        src/ebm/enterprise_bookmarks_manager.py
    GOTO :CHECKSUM
) else (
    echo [1mThere were Errors while code style checking with Flake8 - Abort[0m
    GOTO :DONE
)

:CHECKSUM
echo [1mCreate Checksum File[0m
powershell -Command "& {$((CertUtil -hashfile .\release\enterprise_bookmarks_manager.exe SHA256)[1] -replace ' ','') + ' *enterprise_bookmarks_manager.exe' | Out-File -FilePath .\release\enterprise_bookmarks_manager.sha256}"
where gpg >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo [1mSign Executable with GPG[0m
    gpg --output .\release\enterprise_bookmarks_manager.sha256.sig --detach-sign .\release\enterprise_bookmarks_manager.sha256
) else (
    echo [1mGPG not found, skipping signature[0m
)
powershell Compress-Archive release\enterprise_bookmarks_manager.* release\enterprise_bookmarks_manager.zip
if EXIST release\enterprise_bookmarks_manager.zip (
    echo [1mExecutable created successfully[0m
    GOTO :CLEANUP
) else (
    echo [1mThere was an Error creating the Executable - Abort[0m
    GOTO :DONE
)

:CLEANUP
echo [1mCleanup[0m
IF EXIST release\enterprise_bookmarks_manager.exe DEL /F release\enterprise_bookmarks_manager.exe
IF EXIST release\enterprise_bookmarks_manager.spec DEL /F release\enterprise_bookmarks_manager.spec
IF EXIST release\enterprise_bookmarks_manager.sha256 DEL /F release\enterprise_bookmarks_manager.sha256
IF EXIST release\enterprise_bookmarks_manager.sha256.sig DEL /F release\enterprise_bookmarks_manager.sha256.sig
IF EXIST enterprise_bookmarks_manager.spec DEL /F /Q enterprise_bookmarks_manager.spec
IF EXIST VERSION DEL /F /Q VERSION
IF EXIST __pycache__ rmdir /Q /S __pycache__
IF EXIST build rmdir /Q /S build
GOTO :DONE

:DONE
pause