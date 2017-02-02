@echo off
set ChromeDir=C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data
del /q /s /f "%ChromeDir%"
rd /s /q "%ChromeDir%"
cls
IF %ERRORLEVEL%==0 (
@echo "Done Wiping cache ,cookies,browsing and Download History"
exit0
) ELSE (
@echo "Error Something wrong! Try Again"
exit 1001
)
