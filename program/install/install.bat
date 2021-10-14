@ECHO off
cls
:start
SET "ThisScriptsDirectory=%~dp0\\..\\.."
SET AppName=Torque Accuracy Tool
SET FileName=torque_accuracy_tool
ECHO.
ECHO ##### %AppName% Install #####
ECHO. 
ECHO    [1] Install Python 3.7.4, Paths, Dependancies and Launch %AppName% [Powershell]
ECHO. 
ECHO    [2] Install Dependancies and Launch %AppName%
ECHO. 

set choice=
set /p choice=Type the [number] of the option you want to use: 
ECHO. 

if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='1' goto install_full
if '%choice%'=='2' goto install_dep

ECHO "%choice%" is not valid, try again
ECHO.
goto start

:install_full

ECHO Downloading Python Installer (python-3.7.4-amd64.exe)
ECHO.

curl "https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe" -o python-3.7.4-amd64.exe

ECHO.
ECHO Installing Python (python-3.7.4-amd64.exe)
ECHO.

python-3.7.4-amd64.exe /quiet InstallAllUsers=0 PrependPath=1 AssociateFiles=0

ECHO Refreshing Environmental Variables
ECHO.

call %ThisScriptsDirectory%\program\install\RefreshEnv.cmd

del python-3.7.4-amd64.exe

goto install_dep

:install_dep

ECHO.
ECHO Generating Desktop Shortcut and Icon
ECHO.

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\%AppName%.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath ="%comspec%" >> %SCRIPT%
echo oLink.Arguments = " /c ""%ThisScriptsDirectory%\program\%FileName%.bat""" >> %SCRIPT%
echo oLink.IconLocation = "%ThisScriptsDirectory%\icon\icon.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

ECHO Installing Dependancies
ECHO.

py -3.7 -m pip install --upgrade pip
py -3.7 -m pip install -r %ThisScriptsDirectory%\program\install\requirements.txt

ECHO.
ECHO Launching %AppName%
ECHO.

py -3.7 -m streamlit run %ThisScriptsDirectory%\program\%FileName%.py