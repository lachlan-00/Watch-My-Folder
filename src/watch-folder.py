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
skipList = (conf.get('conf', 'SkipFiles')).split()
waitTime = int(conf.get('conf', 'WaitTime'))
scancyclecount = 0

### Define Functions ###


# File operation Function
def check_file(inputfile, backupPath):
    backupfile = os.path.normpath(backupPath + (inputfile.replace(HOME, '')))
    backupdir = os.path.dirname(backupfile)
    # Only backup files that contain data
    if os.stat(inputfile)[6] == 0:
        pass
    # Copy file if it doesn't exist in backup location
    elif not os.path.isfile(backupfile):
        if not os.path.exists(backupdir):
            try:
                os.makedirs(backupdir)
            except:
                pass
        try:
            shutil.copyfile(inputfile, backupfile)
            print 'New Backup: ' + backupfile
        except IOError:
            pass
    elif os.path.isfile(backupfile):
        # Compare existing files and backup modified versions since the last cycle.
        if not os.stat(inputfile)[6] == os.stat(backupfile)[6] or not os.path.getmtime(inputfile) < os.path.getmtime(backupfile):
            newfile = backupfile
            newcount = 0
            # Create new destination (for versioning)
            while os.path.isfile(newfile):
                if newcount == 6:
                    five = os.path.join(os.path.dirname(newfile), (os.path.basename(newfile) + '-5.old'))
                    zero = os.path.join(os.path.dirname(newfile), (os.path.basename(newfile) + '-0.old'))
                    shutil.copyfile(five, zero)
                    tempcount = ['1','2','3','4','5']
                    for count in tempcount:
                        temp = '-' + count + '.old'
                        os.remove(os.path.join(os.path.dirname(newfile), (os.path.basename(newfile) + temp)))
                    newcount = 1
                temp = '-' + str(newcount) + '.old'
                oldfile = os.path.join(os.path.dirname(newfile), (os.path.basename(newfile) + temp))
                if not os.path.isfile(oldfile):
                    newfile = oldfile
                newcount = newcount + 1
            shutil.move(backupfile, newfile)
            try:
                shutil.copyfile(inputfile, backupfile)
                print 'New Version: ' + newfile
            except IOError:
                # Error: File in Use
                pass
    return


# Recursive loop function using watch_folders
def check_folder(inputstring, backupPath):
    if os.path.isdir(inputstring):
        # wait to reduce load
        time.sleep(waitTime)
        watch_folder(inputstring, backupPath)
    return

### Main Function ###


# Search recursively through folders looking for files to backup
def watch_folder(inputfolder, backupPath):
    if os.path.abspath(inputfolder) == os.path.abspath(backupPath):
        print 'Skipping Backup Folder'
    else:
        try:
            for items in os.listdir(inputfolder):
                skipme = False
                for ignored in skipList:
                    if ignored in items:
                        skipme = True
                    elif os.path.splitext(items)[1] in skipList:
                        skipme = True
                # Run check_file if a file is found
                testPath = os.path.join(inputfolder, items)
                if os.path.isfile(testPath) and not skipme:
                    check_file(os.path.join(inputfolder, items), backupPath)
                # Run check_folder if a folder is found
                if os.path.isdir(testPath) and not skipme:
                    check_folder(testPath, backupPath)
        # Ignore Inaccessible Directories
        except WindowsError:
            # Error: Inaccessible Directory
            pass
    return


### Main Program ###

# Create main backup folder if not found
while 1:
    #Begin Scanning
    scancyclecount = scancyclecount + 1
    print ''
    print 'Beginning Scan Cycle ' + str(scancyclecount)
    for destination in backupList:
        if destination == 'USEDEFAULT':
            destination = os.path.join(LOCAL_PROFILE, ".backup")
        print 'Copying files to: ' + destination
        for items in folderList:
            if not items == '':
                time.sleep(waitTime)
                if items == 'USEDEFAULT':
                    items = LOCAL_PROFILE
                    backupPath = destination + '/profile/'
                else:
                    backupPath = (destination + '/' +
                                    (items).replace(':\\', '\\') + '/')
                HOME = items
                print 'Opening folder...  ' + items
                try:
                    if not os.path.exists(backupPath):
                        os.makedirs(backupPath)
                    if os.path.isdir(items):
                        watch_folder(items, backupPath)
                except WindowsError:
                    # Skip error when directory is missing
                    print '** Error: Moving to next directory'
                    pass
                print ''
