import os
from win32com.client import Dispatch
installfolder = os.getcwd()

shell = Dispatch('WScript.Shell')

#Program Shortcut
path = os.path.join(installfolder, "Watch My Folder.lnk")
target = installfolder + r"\watch\watch-my-folder.bat"
wDir = installfolder + r"\watch"
icon = installfolder + r"\watch\icon.ico"

#config Shortcut
confpath = os.path.join(installfolder, "Edit Config File.lnk")
conftarget = installfolder + r"\watch\config-windows.txt"

shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()

confshortcut = shell.CreateShortCut(confpath)
confshortcut.Targetpath = conftarget
confshortcut.WorkingDirectory = wDir
confshortcut.save()
