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

import gtk
import os
import time
import shutil
import ConfigParser
import subprocess
import sys

from multiprocessing import Process
from threading import *


windowOpen = True
STOP = False
started = False
OS = os.name
if OS == 'nt':
    SLASH = '\\'
elif OS == 'posix':
    SLASH = '/'

class WorkerThread(Thread):

    """Worker Thread Class."""
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        super(WorkerThread, self).__init__()
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        watch.main(watch())


class watch_my_folder(gtk.Window):
    ### Initialise Main Window ###
    def __init__(self):
        global watch_process
        self.Builder = gtk.Builder()
        self.Builder.add_from_file("watch-my-folder.ui")
        self.Window = self.Builder.get_object("main_window")
        self.Window.set_title("Watch My Folder")
        self.Window.connect("delete-event", self.delete_event)
        self.statuslabel = self.Builder.get_object("statuslabel")
        self.statuslabel.set_text('Scan Running')
        self.quitbutton = self.Builder.get_object("quitbutton")
        self.quitbutton.connect("clicked",self.quit)
        self.startButton = self.Builder.get_object("startbutton")
        self.startButton.connect("clicked",self.start_scan)
        self.stopButton = self.Builder.get_object("stopbutton")
        self.stopButton.connect("clicked",self.stop_scan)
        #show all of the stuff
        self.Window.show_all()
        #make a status icon
        self.statusicon = gtk.status_icon_new_from_file('watch.png')
        self.statusicon.connect('activate', self.status_clicked )
        self.statusicon.set_tooltip("Watch My Folder")
        self.Window.hide()
        #Start main function first
        self.worker = None
        if not self.worker:
            self.worker = WorkerThread(self)
        #start the gtk main loop
        gtk.main()


    def start_scan(self, *args):
        self.statuslabel.set_text('Scan Running')
        global watch_process
        global STOP
        if not self.worker:
            self.worker = WorkerThread(self)
        if self.worker.is_alive():
            print 'already started'
        else:
            print 'starting'
            STOP = False
            self.worker.__init__(self)


    def stop_scan(self, *args):
        self.statuslabel.set_text('Scan Stopped')
        global watch_process
        if not self.worker:
            self.worker = WorkerThread(self)
        if self.worker.is_alive():
            print 'stopping'
            watch.stop_main(watch())
        else:
            print 'already stopped'
        STOP = True
        return
                

    def quit(self,button):
        self.stop_scan()
        #quit the gtk main loop
        gtk.main_quit()
        return False


    def delete_event(self,window,event):
        global windowOpen
        #don't delete; hide instead
        self.Window.hide_on_delete()
        windowOpen = False
        return True
 

    def status_clicked(self,status):
        global windowOpen
        #unhide the window
        if not windowOpen:
            self.Window.show_all()
            windowOpen = True
        elif windowOpen:
            self.delete_event(self, self.Window)


class watch(Process):
    ### Define Functions ###
    def __init__(self):
        global STOP
        global OS
        global SLASH
        global ORIGINAL_FOLDER
        if OS == 'nt':
            LOCAL_PROFILE = os.getenv("userprofile")
            USERNAME = os.getenv("username")
            CONF = 'config-windows.txt'
        elif OS == 'posix':
            LOCAL_PROFILE = os.getenv("HOME")
            USERNAME = os.getenv("USER")
            CONF = 'config-linux.txt'
        else:
            STOP = True
        if STOP:
            return
        self.conf = ConfigParser.RawConfigParser()
        self.conf.read(CONF)
        self.skipFileList = self.conf.get('conf', 'SkipFiles').split(' ')
        self.skipFolderList = self.conf.get('conf', 'SkipFolders').split('    ')
        self.waitTime = self.conf.get('conf', 'WaitTime')
        try:
            self.waitTime = int(self.waitTime)
        except:
            self.waitTime = 1
        self.destination = self.conf.get('conf', 'BackupPath')
        self.inputFolder = self.conf.get('conf', 'FolderPath')
        if OS == 'nt':
            self.destination = self.destination.replace('%username%', USERNAME)
            self.inputFolder = self.inputFolder.replace('%username%', USERNAME)
            self.destination = self.destination.replace('%userprofile%', LOCAL_PROFILE)
            self.inputFolder = self.inputFolder.replace('%userprofile%', LOCAL_PROFILE)
        if OS == 'posix':
            self.destination = self.destination.replace('$USER', USERNAME)
            self.inputFolder = self.inputFolder.replace('$USER', USERNAME)
            self.destination = self.destination.replace('$HOME', LOCAL_PROFILE)
            self.inputFolder = self.inputFolder.replace('$HOME', LOCAL_PROFILE)
        if not os.path.isdir(self.destination):
            self.destination = LOCAL_PROFILE + SLASH + '.backup' + SLASH + 'BACKUP'
        if not os.path.isdir(self.inputFolder):
            self.inputFolder = LOCAL_PROFILE
        ORIGINAL_FOLDER = self.inputFolder
        

    # File operation Function
    def check_file(self, *args):
        global STOP
        global SLASH
        if STOP:
            return
        inputFile = args[0]
        backupPath = args[1]
        insplit = os.path.dirname(inputFile).split(SLASH)
        origFolder =  ORIGINAL_FOLDER.split(SLASH)
        outdir = ''
        for items in origFolder:
            if not len(insplit) == 0:
                for folders in insplit:
                    if items in folders:
	                #insplit = insplit[1:]
                        try:
                            insplit.remove(items)
                        except ValueError:
                            pass
        for items in insplit:
            outdir = outdir + SLASH + items
        backupFile = os.path.normpath(backupPath + outdir + SLASH + (os.path.basename(inputFile)))
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
            # Compare existing files and backup modified versions since the last cycle.
            if not os.stat(inputFile)[6] == os.stat(backupFile)[6] or not os.path.getmtime(inputFile) < os.path.getmtime(backupFile):
                newFile = backupFile
                newCount = 0
                # Create new destination (for versioning)
                while os.path.isfile(newFile):
                    if newCount == 6:
                        five = os.path.join(os.path.dirname(newFile), (os.path.basename(newFile) + '-5.old'))
                        zero = os.path.join(os.path.dirname(newFile), (os.path.basename(newFile) + '-0.old'))
                        shutil.copyfile(five, zero)
                        tempCount = ['1','2','3','4','5']
                        for count in tempCount:
                            temp = '-' + count + '.old'
                            os.remove(os.path.join(os.path.dirname(newFile), (os.path.basename(newFile) + temp)))
                        newCount = 1
                    temp = '-' + str(newCount) + '.old'
                    oldFile = os.path.join(os.path.dirname(newFile), (os.path.basename(newFile) + temp))
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
    def check_folder(self, *args):
        global STOP
        if STOP:
            return
        inputString = args[0]
        backupPath = args[1]
        if os.path.isdir(inputString):
            # wait to reduce load
            time.sleep(self.waitTime)
            self.watch_folder(backupPath, inputString)
        return


    # Search recursively through folders looking for files to backup
    def watch_folder(self, *args):
        global STOP
        if STOP:
            return
        backupPath = args[0]
        inputFolder = args[1]
        print 'opening: ' + inputFolder
        skipMe = False
        for items in self.skipFolderList:
            if items.lower() in inputFolder.lower():
                skipMe = True
        if not skipMe:
            try:
                for items in os.listdir(inputFolder):
                    skipme = False
                    for ignored in self.skipFileList:
                        if ignored.lower() in items.lower():
                            skipme = True
                        elif os.path.splitext(items)[1] in self.skipFileList:
                            skipme = True
                    # Run check_file if a file is found
                    if os.path.isfile(os.path.join(inputFolder, items)) and not skipme:
                        self.check_file(os.path.join(inputFolder, items), backupPath)
                    # Run check_folder if a folder is found
                    if os.path.isdir(os.path.join(inputFolder, items)) and not skipme:
                        self.check_folder(os.path.join(inputFolder, items), backupPath)
            # Ignore Inaccessible Directories
            except OSError:
                # Error: Inaccessible Directory
                pass
        return


    ### Main Function ###
    def main(self, *args):
        global STOP
        if STOP:
            return
        global started
        if not started:
            started = True
            while 1 and not STOP:
                time.sleep(self.waitTime)
                print 'Opening folder...'
                try:
                    if not os.path.exists(self.destination):
                       os.makedirs(self.destination)
                    if not os.path.exists(self.inputFolder):
                       os.makedirs(self.inputFolder)
                    self.watch_folder(self.destination, self.inputFolder)
                except OSError:
                    # Skip error when directory is missing
                    print '** Error: Moving to next directory'
                    pass
                print ''
            started = False

    def stop_main(self):
        global STOP
        STOP = True

if __name__=="__main__":
    gtk.gdk.threads_init()
    watch_my_folder()

