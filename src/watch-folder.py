#!/usr/bin/env python

""" Watch My Folder

    ----------------Authors----------------
    Lachlan de Waard <lachlan.00@gmail.com>
    ----------------Licence----------------
    GNU General Public License version 3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


import os
import time
import shutil
import ConfigParser

### Define Constants ###
LOCAL_PROFILE = os.getenv("userprofile")
CONF = 'config.txt'
conf = ConfigParser.RawConfigParser()
conf.read(CONF)

### Define Variables ###
folderList = str(conf.get('conf', 'FolderPath'))
folderList = folderList.split(',')
backupList = str(conf.get('conf', 'BackupPath'))
backupList = backupList.split(',')
skipFileList = (conf.get('conf', 'SkipFiles')).split(' ')
skipFolderList = (conf.get('conf', 'SkipFolders')).split('    ')
waitTime = int(conf.get('conf', 'WaitTime'))
scanCycleCount = 0


### Define Functions ###
# File operation Function
def check_file(inputFile, backupPath, homePath):
    backupFile = (os.path.normpath(backupPath +
                    (inputFile.replace(homePath, ''))))
    backupDir = os.path.dirname(backupFile)
    # Only backup files that contain data
    if os.stat(inputFile)[6] == 0:
        pass
    # Copy file if it doesn't exist in backup location
    elif not os.path.isfile(backupFile):
        if not os.path.exists(backupDir):
            try:
                os.makedirs(backupDir)
            except:
                pass
        try:
            shutil.copyfile(inputFile, backupFile)
            print 'New Backup: ' + backupFile
        except IOError:
            pass
    elif os.path.isfile(backupFile):
        # Compare existing files and backup the modified version.
        if (not os.stat(inputFile)[6] == os.stat(backupFile)[6] or not
                os.path.getmtime(inputFile) < os.path.getmtime(backupFile)):
            newFile = backupFile
            newCount = 0
            # Create new destination (for versioning)
            while os.path.isfile(newFile):
                if newCount == 6:
                    five = (os.path.join(os.path.dirname(newFile),
                                (os.path.basename(newFile) + '-5.old')))
                    zero = (os.path.join(os.path.dirname(newFile),
                                (os.path.basename(newFile) + '-0.old')))
                    shutil.copyfile(five, zero)
                    tempCount = ['1', '2', '3', '4', '5']
                    for count in tempCount:
                        temp = '-' + count + '.old'
                        os.remove(os.path.join(os.path.dirname(newFile),
                                        (os.path.basename(newFile) + temp)))
                    newCount = 1
                temp = '-' + str(newCount) + '.old'
                oldFile = (os.path.join(os.path.dirname(newFile),
                                (os.path.basename(newFile) + temp)))
                if not os.path.isfile(oldFile):
                    newFile = oldFile
                newCount = newCount + 1
            shutil.move(backupFile, newFile)
            try:
                shutil.copyfile(inputFile, backupFile)
                print 'New Version: ' + newFile
            except IOError:
                # Error: File in Use
                pass
    return


# Recursive loop function using watch_folders
def check_folder(inputString, backupPath, homePath):
    if os.path.isdir(inputString):
        # wait to reduce load
        time.sleep(waitTime)
        watch_folder(inputString, backupPath, homePath)
    return


# Search recursively through folders looking for files to backup
def watch_folder(inputFolder, backupPath, homePath):
    skipMe = False
    for items in skipFolderList:
        if items.lower() in inputFolder.lower():
            skipMe = True
    if not skipMe:
        try:
            for items in os.listdir(inputFolder):
                skipme = False
                for ignored in skipFileList:
                    if ignored.lower() in items.lower():
                        skipme = True
                    elif os.path.splitext(items)[1] in skipFileList:
                        skipme = True
                # Run check_file if a file is found
                if (os.path.isfile(os.path.join(inputFolder, items)) and not
                        skipme):
                    temp = os.path.join(inputFolder, items)
                    check_file(temp, backupPath, homePath)
                # Run check_folder if a folder is found
                if (os.path.isdir(os.path.join(inputFolder, items)) and not
                        skipme):
                    temp = os.path.join(inputFolder, items)
                    check_folder(temp, backupPath, homePath)
        # Ignore Inaccessible Directories
        except WindowsError:
            # Error: Inaccessible Directory
            pass
    return


### Main Function ###
def main(inputFolder, outputFolder):
    for destination in outputFolder:
        if destination == 'USEDEFAULT':
            destination = os.path.join(LOCAL_PROFILE, ".backup")
        print 'Copying files to: ' + destination
        for items in inputFolder:
            if not items == '':
                time.sleep(waitTime)
                if items == 'USEDEFAULT':
                    items = LOCAL_PROFILE
                    backupPath = destination + '/profile/'
                else:
                    backupPath = (destination + '/' +
                                    (items).replace(':\\', '\\') + '/')
                homePath = items
                print 'Opening folder...  ' + items
                try:
                    if not os.path.exists(backupPath):
                        os.makedirs(backupPath)
                    if os.path.isdir(items):
                        watch_folder(items, backupPath, homePath)
                except WindowsError:
                    # Skip error when directory is missing
                    print '** Error: Moving to next directory'
                    pass
                print ''

### Main Program ###

# Create main backup folder if not found
while 1:
    #Begin Scanning
    scanCycleCount = scanCycleCount + 1
    print 'Beginning Scan Cycle ' + str(scanCycleCount)
    main(folderList, backupList)
    #Sleep after each cycle
    time.sleep(120)
