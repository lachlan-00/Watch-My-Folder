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


import os, time, shutil, ConfigParser

### Define Constants ###

LOCAL_PROFILE = os.getenv("userprofile")
USERNAME = os.getenv("userprofile")
CONF = 'config.txt'
conf = ConfigParser.RawConfigParser()
conf.read(CONF)

### Define Variables ###

if conf.get('conf', 'BackupPath') == 'USEDEFAULT':
    BACKUP_PATH = os.path.join(LOCAL_PROFILE, ".backup")
else:
    BACKUP_PATH = conf.get('conf', 'BackupPath')
if conf.get('conf', 'FolderPath') == 'USEDEFAULT':
    HOME = LOCAL_PROFILE + '/'
else:
    HOME = str(conf.get('conf', 'FolderPath'))
SKIP = (conf.get('conf', 'SkipFiles')).split()
WAITTIME = int(conf.get('conf', 'WaitTime'))

### Define Functions ###

# File operation Function
def check_file(inputfile):
    backupfile = os.path.join(BACKUP_PATH, (inputfile.replace(HOME, '')))
    backupdir = os.path.dirname(backupfile)
    # Copy file if it doesn't exist in backup location
    if not os.path.isfile(backupfile):
        print 'Copying file:  ' + backupfile
        if not os.path.exists(backupdir):
            try:
                os.makedirs(backupdir)
            except:
                print 'Create folder Failed'
        try:
            shutil.copyfile(inputfile, backupfile)
        except:
            print 'Failed to create file backup.'
    elif os.path.isfile(backupfile):
        # Compare existing files and backup modified versions.
        if not os.stat(inputfile)[6] == os.stat(backupfile)[6]:
            print 'size difference ' + backupfile
            newfile = backupfile
            newcount = 0
            # Create new destination (for versioning)
            while os.path.isfile(newfile):
                if newcount == 6:
                    five = os.path.join(os.path.dirname(newfile), (os.path.basename(newfile) + 'backup-5.old'))
                    zero = os.path.join(os.path.dirname(newfile), (os.path.basename(newfile) + 'backup-0.old'))
                    shutil.copyfile(five, zero)
                    tempcount = ['1','2','3','4','5']
                    for count in tempcount:
                        temp = 'backup-' + count + '.old'
                        os.remove(os.path.join(os.path.dirname(newfile), (os.path.basename(newfile) + temp)))
                    newcount = 1
                temp = 'backup-' + str(newcount) + '.old'
                oldfile = os.path.join(os.path.dirname(newfile), (os.path.basename(newfile) + temp))
                if not os.path.isfile(oldfile):
                    newfile = oldfile
                newcount = newcount + 1
            print newfile + backupfile
            shutil.move(backupfile, newfile)
            shutil.copyfile(inputfile, backupfile)
    return

# Recursive loop function using watch_folders
def check_folder(inputstring):
    if os.path.isdir(inputstring):
        # wait to reduce load
        time.sleep(WAITTIME)
        watch_folder(inputstring)
    return

### Main Function ###

# Search recursively through folders looking for files to backup
def watch_folder(inputfolder):
    if os.path.abspath(inputfolder) == os.path.abspath(BACKUP_PATH):
        print 'Skipping Backup Folder'
    else:
        for items in os.listdir(inputfolder):
            skipme = False
            for ignored in SKIP:
                if ignored in items:
                    skipme = True
                elif os.path.splitext(items)[1] in SKIP:
                    skipme = True
            # run check_file if a file is found
            if os.path.isfile(os.path.join(inputfolder, items)) and not skipme:
                check_file(os.path.join(inputfolder, items))
            # runs check_folder if a folder is found
            if os.path.isdir(os.path.join(inputfolder, items)) and not skipme:
                check_folder(os.path.join(inputfolder, items))
    return


### Main Program ###

# Create backup folder if not found
if not os.path.exists(BACKUP_PATH):
    os.makedirs(BACKUP_PATH)
while 1:
    # wait a bit for things to settle
    time.sleep(10)
    print 'Scanning Home Folder'
    watch_folder(HOME)
    print ''
