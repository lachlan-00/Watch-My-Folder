import os, time, shutil, ConfigParser

### Define Constants ###

LOCAL_PROFILE = os.getenv("userprofile")
USERNAME = os.getenv("userprofile")
CONF = 'config.txt'
conf = ConfigParser.RawConfigParser()
conf.read(CONF)

### Define Variables ###

if conf.get('conf', 'BackupPath') == 'USEDEFAULT':
    BACKUP_PATH = os.path.join(LOCAL_PROFILE, "backup")
else:
    BACKUP_PATH = conf.get('conf', 'BackupPath')
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
        # wait three minutes to reduce LAN load
        time.sleep(WAITTIME)
        watch_folder(inputstring)
    return

### Main Function ###

# Search recursively through folders looking for files to backup
def watch_folder(inputfolder):
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
    time.sleep(60)
    print 'Scanning Home Folder'
    watch_folder(HOME)
    print ''