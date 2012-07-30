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

from multiprocessing import Process
from threading import Thread


WINDOWOPEN = True
STOP = False
STARTED = False
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


class watch_my_folder(gtk.Builder):
    """ Initialise Main Window """
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("watch-my-folder.ui")
        self.window = self.builder.get_object("main_window")
        self.window.set_title("Watch My Folder")
        self.window.connect("delete-event", self.delete_event)
        self.statuslabel = self.builder.get_object("statuslabel")
        self.statuslabel.set_text('Scan Running')
        self.quitbutton = self.builder.get_object("quitbutton")
        self.quitbutton.connect("clicked", self.quit)
        self.startbutton = self.builder.get_object("startbutton")
        self.startbutton.connect("clicked", self.start_scan)
        self.stopbutton = self.builder.get_object("stopbutton")
        self.stopbutton.connect("clicked", self.stop_scan)
        #show all of the stuff
        self.window.show_all()
        #make a status icon
        self.statusicon = gtk.status_icon_new_from_file('watch.png')
        self.statusicon.connect('activate', self.status_clicked )
        self.statusicon.set_tooltip("Watch My Folder")
        self.window.hide()
        #Start main function first
        self.worker = None
        if not self.worker:
            self.worker = WorkerThread(self)
        #start the gtk main loop
        gtk.main()


    def start_scan(self, *args):
        """ Start the scan process separate of the GUI """
        self.statuslabel.set_text('Scan Running')
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
        """ Stop the scan process """
        global STOP
        self.statuslabel.set_text('Scan Stopped')
        if not self.worker:
            self.worker = WorkerThread(self)
        if self.worker.is_alive():
            print 'stopping'
            watch.stop_main(watch())
        else:
            print 'already stopped'
        STOP = True
        return
                

    def quit(self, button):
        """ Close down the program and quit the main loop """
        self.stop_scan()
        #quit the gtk main loop
        gtk.main_quit()
        return False


    def delete_event(self,window, event):
        """ Hide the window then the close button is clicked """
        global WINDOWOPEN
        #don't delete; hide instead
        self.window.hide_on_delete()
        WINDOWOPEN = False
        return True
 

    def status_clicked(self, status):
        """ hide and unhide the window when clicking the status icon """
        global WINDOWOPEN
        #unhide the window
        if not WINDOWOPEN:
            self.window.show_all()
            WINDOWOPEN = True
        elif WINDOWOPEN:
            self.delete_event(self, self.window)


class watch(Process):
    """ Class that controls the scan process """
    def __init__(self):
        global STOP
        global SLASH
        global ORIGINAL_FOLDER
        if OS == 'nt':
            local_profile = os.getenv("userprofile")
            username = os.getenv("username")
            homeshare = os.getenv("homeshare")
            conf_file = 'config-windows.txt'
            print conf_file
        elif OS == 'posix':
            local_profile = os.getenv("HOME")
            username = os.getenv("USER")
            conf_file = 'config-linux.txt'
        else:
            STOP = True
        if STOP:
            return
        self.conf = ConfigParser.RawConfigParser()
        self.conf.read(conf_file)
        self.skip_file_list = self.conf.get('conf', 'SkipFiles').split(' ')
        self.skip_folder_list = self.conf.get('conf', 'SkipFolders').split('    ')
        self.wait_time = self.conf.get('conf', 'WaitTime')
        try:
            self.wait_time = int(self.wait_time)
        except:
            self.wait_time = 1
        self.destination = self.conf.get('conf', 'BackupPath')
        self.input_folder = self.conf.get('conf', 'FolderPath')
        if OS == 'nt':
            self.destination = self.destination.replace('%username%', 
                                                        username)
            self.input_folder = self.input_folder.replace('%username%', 
                                                        username)
            self.destination = self.destination.replace('%userprofile%', 
                                                        local_profile)
            self.input_folder = self.input_folder.replace('%userprofile%', 
                                                        local_profile)
            self.destination = self.destination.replace('%homeshare%', 
                                                        homeshare)
            self.input_folder = self.input_folder.replace('%homeshare%', 
                                                        homeshare)
            self.skip_tilde = False
        if OS == 'posix':
            if self.conf.get('conf', 'SkipTildeFiles') == 'True':
                self.skip_tilde =  True
            else:
                self.skip_tilde =  False
            self.destination = self.destination.replace('$USER', username)
            self.input_folder = self.input_folder.replace('$USER', username)
            self.destination = self.destination.replace('$HOME', local_profile)
            self.input_folder = self.input_folder.replace('$HOME', local_profile)
        # Attempt to make the backup path
        if not os.path.isdir(self.destination):
            try:
                os.makedirs(self.destination)
            except:
                self.destination = (local_profile + SLASH + '.backup' + SLASH + 
                                'BACKUP')
        if not os.path.isdir(self.input_folder):
            self.input_folder = local_profile
        # used to strip useless folders from the backup path
        ORIGINAL_FOLDER = self.input_folder
        

    def check_file(self, *args):
        """ File operation Function """
        global STOP
        global SLASH
        global ORIGINAL_FOLDER
        if STOP:
            return
        input_file = args[0]
        backup_path = args[1]
        insplit = os.path.dirname(input_file).split(SLASH)
        orig_folder =  ORIGINAL_FOLDER.split(SLASH)
        outdir = ''
        for items in orig_folder:
            if not len(insplit) == 0:
                for folders in insplit:
                    if items in folders:
                        try:
                            insplit.remove(items)
                        except ValueError:
                            pass
        for items in insplit:
            outdir = outdir + SLASH + items
        backup_file = (os.path.normpath(backup_path + outdir + SLASH + 
                        (os.path.basename(input_file))))
        backup_dir = os.path.dirname(backup_file)
        # Only backup files that contain data
        if os.stat(input_file)[6] == 0:
            pass
        # Copy file if it doesn't exist in backup location
        elif not os.path.isfile(backup_file):
            if not os.path.exists(backup_dir):
                try:
                    os.makedirs(backup_dir)
                except:
                    pass
            try:
                shutil.copyfile(input_file, backup_file)
                print 'New Backup: ' + backup_file
            except IOError:
                pass
        elif os.path.isfile(backup_file):
            # Compare files and backup modified versions since the last cycle.
            if (not os.stat(input_file)[6] == os.stat(backup_file)[6] or 
                not os.path.getmtime(input_file) < os.path.getmtime(backup_file)):
                new_file = backup_file
                new_count = 0
                # Create new destination (for versioning)
                while os.path.isfile(new_file):
                    if new_count == 6:
                        five = (os.path.join(os.path.dirname(new_file), 
                                             (os.path.basename(new_file) + 
                                                 '-5.old')))
                        zero = (os.path.join(os.path.dirname(new_file), 
                                             (os.path.basename(new_file) + 
                                                 '-0.old')))
                        shutil.copyfile(five, zero)
                        temp_count = ['1', '2', '3', '4', '5']
                        for count in temp_count:
                            temp = '-' + count + '.old'
                            os.remove(os.path.join(os.path.dirname(new_file), 
                                                   (os.path.basename(new_file) +
                                                       temp)))
                        new_count = 1
                    temp = '-' + str(new_count) + '.old'
                    old_file = os.path.join(os.path.dirname(new_file), 
                                           (os.path.basename(new_file) + temp))
                    if not os.path.isfile(old_file):
                        new_file = old_file
                    new_count = new_count + 1
                shutil.move(backup_file, new_file)
                try:
                    shutil.copyfile(input_file, backup_file)
                    print 'New Version: ' + new_file
                except IOError:
                    # Error: File in Use
                    pass
        return

    def check_folder(self, *args):
        """ Recursive loop function for watch_folder function """
        global STOP
        if STOP:
            return
        input_string = args[0]
        backup_path = args[1]
        if os.path.isdir(input_string):
            # wait to reduce load
            time.sleep(self.wait_time)
            self.watch_folder(backup_path, input_string)
        return


    def watch_folder(self, *args):
        """ Search recursively through folders looking for files """
        global STOP
        if STOP:
            return
        backup_path = args[0]
        input_folder = args[1]
        print 'Opening: ' + input_folder
        skip_me = False
        for items in self.skip_folder_list:
            if items.lower() in input_folder.lower():
                skip_me = True
                print 'skipping ' + items
        if not skip_me:
            try:
                for items in os.listdir(input_folder):
                    skipme = False
                    for ignored in self.skip_file_list:
                        # don't try to process blank items
                        if not items == '' and not ignored == '':
                            if ignored.lower() in items.lower():
                                skipme = True
                            elif os.path.splitext(items)[1] in self.skip_file_list:
                                if not os.path.splitext(items)[1] == '':
                                    skipme = True
                            elif self.skip_tilde:
                                if items[-1] == '~':
                                    skipme=True
                    # Run check_file if a file is found
                    if (os.path.isfile(os.path.join(input_folder, items)) and 
                        not skipme):
                        self.check_file(os.path.join(input_folder, items), 
                                        backup_path)
                    # Run check_folder if a folder is found
                    if (os.path.isdir(os.path.join(input_folder, items)) and 
                        not skipme):
                        self.check_folder(os.path.join(input_folder, items), 
                                          backup_path)
            # Ignore Inaccessible Directories
            except:
                # Error: Inaccessible Directory
                pass
        return


    def main(self, *args):
        """ Main Function """
        global STOP
        if STOP:
            return
        global STARTED
        if not STARTED:
            STARTED = True
            while 1 and not STOP:
                time.sleep(self.wait_time)
                try:
                    if not os.path.exists(self.destination):
                        os.makedirs(self.destination)
                    if not os.path.exists(self.input_folder):
                        os.makedirs(self.input_folder)
                    self.watch_folder(self.destination, self.input_folder)
                except:
                    # Skip error when directory is missing
                    print '** Error: Moving to next directory'
                    pass
                print ''
            STARTED = False

    def stop_main(self):
        """ Set stop to force the main function to stop """
        global STOP
        STOP = True

if __name__ == "__main__":
    gtk.gdk.threads_init()
    watch_my_folder()

