from filesystemanalysis import *

class FilesysGUI:
    def __init__(self):
        pass


filesystem = FilesystemScanner()

filesystem.scanner_for_folders()
filesystem.scanner_for_files()

#print(filesystem.complete_scan())

