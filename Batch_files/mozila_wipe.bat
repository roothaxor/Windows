:: Batch script to clear browsing history, download history, and empty the cache for Mozila Firefox.
:: Script can be run via GFI MAX RM 
@echo off
set DataDir=C:\Users\%USERNAME%\AppData\Local\Mozilla\Firefox\Profiles
del /q /s /f "%DataDir%"
rd /s /q "%DataDir%"
for /d %%x in (C:\Users\%USERNAME%\AppData\Roaming\Mozilla\Firefox\Profiles\*) do del /q /s /f %%x\*sqlite
cls
IF %ERRORLEVEL%==0 (
@echo "Everything was fine!! You Good to go"
timeout 5
) ELSE (
@echo "Something is wrong!! Try Again"
exit 1001
)