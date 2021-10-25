from os import walk
import hashlib


class FilesystemScanner:
    def __init__(self, folder_list=None, current_filename="", current_foldername="", node=0):
        self.parent_ID = 0
        if folder_list is None:
            self.folder_and_file_with_id = []
        self.my_path = "C:\\Users\\Skaft\\Documents"
        self.current_filename = current_filename
        self.current_foldername = current_foldername

    def is_folder(self, current_file):
        return current_file[-1] == "/"

    def add_to_list_if_not_exist(self, folder_or_file):
        """Adds to list of folders if it does not exist already."""
        if folder_or_file not in self.folder_and_file_with_id:
            self.folder_and_file_with_id.append(folder_or_file)

    def file_hasher(self, file):
        if self.is_folder(file) == False:
            with open(file, "rb") as current:
                readfile = current.read()
                currhash = hashlib.md5(readfile).hexdigest()
                return currhash

    def scanner(self):
        """Scanner for folders. Initially this is separated from the file scan, only to provide Tkinter with ease
        when doing directory treestructure. It needs parents to come before children, to avoid this, folders first"""
        for (dirpath, dirnames, filenames) in walk(self.my_path):
            self.current_foldername = dirpath
            self.add_to_list_if_not_exist(str(dirpath + "\\"))
            """Scans for files, after calling the folder scan within"""
            for file in filenames:
                self.current_filename = file
                full_file_path = dirpath + "\\" + file
                self.add_to_list_if_not_exist([full_file_path])

    def get_complete_scan(self):
        self.scanner()

        return self.folder_and_file_with_id
