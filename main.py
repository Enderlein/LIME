#!/usr/bin/env python3

"""
A script for automatically filling in the metadata of .mp3 files
(Fills in artist, song name, album name, and track number)
"""

from lime import *

root = tk.Tk()
root.title("LIME 0.1")

#root.columnconfigure(0, weight=1)
#root.columnconfigure(1, weight=1)
#root.columnconfigure(2, weight=1)
#root.rowconfigure(0, weight=1)
#root.rowconfigure(1, weight=1)
#root.rowconfigure(2, weight=1)

app = MainWindow(parent=root)
app.mainloop()
                
__author__ = "Kevin Guzman"
__copyright__ = "Copyright 2017, Kevin Guzman"
__credits__ = ["Kevin Guzman"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Kevin Guzman"
__email__ = "h.keving81@gmail.com"
__status__ = "Development"
