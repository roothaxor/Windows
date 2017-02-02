@echo off
if exist "%programfiles(x86)%\CCleaner" (
start /d "C:\Program Files (x86)\CCleaner" CCleaner.exe /AUTO
)

if exist "%programfiles%\CCleaner" (
start /d "C:\Program Files\CCleaner" CCleaner.exe /AUTO
)

time /T >> %appdata%\CCleaner_history.txt



exit
