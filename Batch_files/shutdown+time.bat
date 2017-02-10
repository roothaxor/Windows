@echo off
color 2 
:::   .            /\         .       .
:::         .     /  \      .          .
:::              /    \   .        .    *
:::             /      \              *
:::             | (__) |   .    .   **
:::      .     /| (oo) |\           **
:::           / | /\/\ | \   .     . *
:::       .  /  |=|==|=|  \     .      *
:::      . /    | |  | |    \  .
:::       / USA | ^||^ |NASA \     .
:::      |______|  ^^  |______|       .
:::     .       (__||__)     .   .
:::        .    /_\  /_\  .     .    .
:::             !!!  !!!
:::
:::

for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
REM batch program managing the shutdown of computer with time limit 
REM all you need to do is double click it and put minutes to shutdown.
title Shutdown PC With Time Limit
set /p time=Set minutes for shuttle to take off PC's Power?: 
set /a time=%time%*60 
shutdown /a 
shutdown /s /f /t %time%
