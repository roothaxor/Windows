::Internet Explorer

@echo off

REM Cookies:

REM RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 2

REM RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 8

::Firefox

@echo off

taskkill /im "firefox.exe"

set DataDir=C:\Users\%USERNAME%\AppData\Local\Mozilla\Firefox\Profiles

del /q /s /f "%DataDir%"

rd /s /q "%DataDir%"

for /d %%x in (C:\Users\%USERNAME%\AppData\Roaming\Mozilla\Firefox\Profiles\*) do del /q /s /f %%x\*sqlite

::Google Chrome

@echo off

set ChromeDir=C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data

del /q /s /f "%ChromeDir%"

rd /s /q "%ChromeDir%"

Msg * "Cache, Cookies have been cleared"?

