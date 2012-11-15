@echo off
set PWD=%cd%
set newpath=;%PWD%\Python;%PWD%\DLLs;%PWD%\Scripts
set PATH=%PATH%%newpath%
start ..\python\pythonw.exe watch-my-folder.py