Watch My Folder
---------------

About:
 * This is a program that runs in the background and watches a specified folder.
 * While watching the folder it creates a 1:1 backup of this folder to a specified location.
 * When files are changed Watch My Folder will create copies of the older file to prevent data loss.
 * The reason for this program was to enable shadow copies of network drives which is currently not possible.

Settings:
 * FolderPath - The path that you will be watching. (eg. H:/)
 * BackupPath - The path where the backups are stored. (Default path is %userprofile%\backup)
 * WaitTime - The time to wait before processing the current folder. (Reduce network load if mapped drive)
 * SkipFiles - Folder names and file extensions that will be skipped by the program.

Usage:
 * Extract bin folder to desired location. It can be any folder the user has permission to.
 * Set desired values in the config.txt file.
 * Run the program.

Memory usage is quite low (2mb) while watching and wait times are an effective way of reducing network load. If you are not watching a network folder a lower watch time is recommended.

When typing folder paths try and use the reverse slashes. (C:/users/username/backup)
