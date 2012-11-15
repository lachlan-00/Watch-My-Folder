@echo off
set COPYCMD=/Y
set PWD=%cd%
echo Extracting Portable Python
tools\unzip -o Python\python.zip -d Python\
set newpath=;%PWD%\Python;%PWD%\DLLs;%PWD%\Scripts
set PATH=%PATH%%newpath%
start Python\python.exe watch\configure.py
mkdir "%appdata%\Microsoft\Windows\Start Menu\Watch My Folder"
xcopy "Watch My Folder.lnk" "%appdata%\Microsoft\Windows\Start Menu\Watch My Folder\"
xcopy "Edit Config File.lnk" "%appdata%\Microsoft\Windows\Start Menu\Watch My Folder\"