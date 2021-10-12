@ECHO off
cls
:start
SET ThisScriptsDirectory=%~dp0
SET PowerShellScriptPath=%ThisScriptsDirectory%/ps_script.ps1
ECHO.
ECHO ################################
ECHO [         xPlot Install        ]
ECHO ################################
ECHO. 
ECHO    [1] Install Python 3.7.4, Paths, Dependancies and Launch xPlot [Powershell]
ECHO. 
ECHO    [2] Install Dependancies and Launch xPlot
ECHO. 

set choice=
set /p choice=Type the [number] of the option you want to use.
ECHO. 

if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='1' goto install_full
if '%choice%'=='2' goto install_dep

ECHO "%choice%" is not valid, try again
ECHO.
goto start

:install_full
ECHO Installing Python 3.7.4, Paths, Dependancies and Launching xPlot
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%PowerShellScriptPath%""' -Verb RunAs}"
goto end

:install_dep
ECHO Installing Dependancies and Launching xPlot
py -3.7 -m pip install -r requirements.txt
py -3.7 -m streamlit run xPlot.py
goto end

:end
pause