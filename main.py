from filesystemanalysis import *
import os

class FilesysGUI:
    def __init__(self):
        pass


filesystem = FilesystemScanner()
files = filesystem.get_complete_scan()
#for key in files:
  # print(key, "->", files[key])



