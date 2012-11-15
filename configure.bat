@echo off
set PWD=%cd%
set newpath=;%PWD%\Python;%PWD%\DLLs;%PWD%\Scripts
set PATH=%PATH%%newpath%
start Python\python.exe watch\configure.py
mkdir "%appdata%\Microsoft\Windows\Start Menu\Watch My Folder"
xcopy /Y "Watch My Folder.lnk" "%appdata%\Microsoft\Windows\Start Menu\Watch My Folder\"
xcopy /Y "Edit Config File.lnk" "%appdata%\Microsoft\Windows\Start Menu\Watch My Folder\"