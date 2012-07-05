from distutils.core import setup
import py2exe

setup(
    name = 'watch-my-folder',
    description = 'Watch My Folder',
    version = '1.0',

    windows = [
                  {
                      'script': 'watch-my-folder.py',
                      'icon_resources': [(1, "icon.ico")]
                  }
              ],

    options = {
                  'py2exe': {
                      'packages': 'encodings',
                      'includes': 'cairo, pango, pangocairo, atk, gobject, gtk, gio, glib',
                  }
              },

    data_files=[
                   'LICENSE.txt',
                   'README.txt',
                   'config-linux.txt',
                   'config-windows.txt',
                   'watch.png',
                   'watch-my-folder.ui',
                   'watch-my-folder.py'
               ]
    )
