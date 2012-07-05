Watch My Folder
---------------

About:
 * This is a program that runs in the background
   and watches a specified folder.

 * While watching the folder it creates a 1:1 backup of this
   folder to a specified location.

 * When files are changed Watch My Folder will create copies
   of the older file to prevent data loss.

 * The reason for this program was to enable shadow copies of
   network drives which is not possible with offline files.

Settings:
 * FolderPath - The path that you will be watching. (eg. H:)
 * BackupPath - The path where the backups are stored.
 * WaitTime - Wait before each folder to reduce network load.
 * SkipFiles - File extensions that will be skipped when found.
   (Single space seperated. ' ')
 * SkipFolders - Skip directories that contains these strings.
   (Four space seperated. '    ')


Usage:
 * Extract to your profile (C:\Users\%username%\)
 * Set desired values in the relevant config.txt file for your OS.


Memory usage is quite low (2-3mb) while watching and wait times are an effective way of reducing network load. If you are not watching a network folder a lower watch time is recommended.

