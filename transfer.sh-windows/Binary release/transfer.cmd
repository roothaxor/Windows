@echo off
:main
::: _                        __              _     
:::| |                      / _|            | |    
:::| |_ _ __ __ _ _ __  ___| |_ ___ _ __ ___| |__  
:::| __| '__/ _` | '_ \/ __|  _/ _ \ '__/ __| '_ \ 
:::| |_| | | (_| | | | \__ \ ||  __/ | _\__ \ | | |
::: \__|_|  \__,_|_| |_|___/_| \___|_|(_)___/_| |_|
:::
:::           Developer: @root_haxor
:::
::: Windows Command line file Upload/Download utility
:::
ECHO.
::Banner
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
::program start to if to goto
:start
ECHO a. Upload
ECHO b. Download
ECHO c. Exit
ECHO.
SET /P option=Select a option :
if "%option%" == "" goto noinput
if "%option%" == "a" goto uFile
if "%option%" == "b" goto dFile
if "%option%" == "c" goto exit
::Upload something 
:uFile
cls
ECHO.
ECHO File names of current directory are :
ECHO.
dir /b /a-d
ECHO.
ECHO.
SET /P file=Input file name :
transfr.exe %file%
goto exit
::Download something
:dFile
cls
ECHO.
SET /P dFil=Link to download :
transfr.exe %dFil%
goto exit
::shit happens
:noinput
cls
ECHO.
ECHO ERROR! no input, Choose from options
ECHO.
goto start
::DIE
:exit
exit /B