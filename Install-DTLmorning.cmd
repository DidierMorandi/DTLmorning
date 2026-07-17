@echo off
setlocal
chcp 65001 >nul
title DTL Morning - Installation

if exist "%~dp0Install-DTLmorning.exe" (
    "%~dp0Install-DTLmorning.exe"
    goto :finished
)

py -3.12 "%~dp0Install-DTLmorning.py"

:finished
set "DTL_EXIT_CODE=%ERRORLEVEL%"
endlocal & exit /b %DTL_EXIT_CODE%
