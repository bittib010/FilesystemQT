from os import walk


class FilesystemScanner:
    def __init__(self, folder_list=None, current_filename="", current_foldername="", node=0):
        if folder_list is None:
            self.folder_and_file_with_id = {}
        self.my_path = "F:\Bilde"
        self.current_filename = current_filename
        self.current_foldername = current_foldername
        self.node = node

    def is_folder(self, current_file):
        return current_file[-1] == "/"

    def add_to_list_if_not_exist(self, folder_or_file):
        """Adds to list of folders if it does not exist already."""
        if folder_or_file not in self.folder_and_file_with_id:
            self.folder_and_file_with_id[str(self.node)] = folder_or_file

    def node_counter(self):
        """ID/node counter for every file and folder"""
        self.node += 1

    def parent_node(self):
        """"""
        for node, path in self.folder_and_file_with_id.items():
            if self.current_filename == path:
                return node
            elif self.current_foldername == path:
                return node

    def scanner_for_folders(self):
        """Scanner for folders. Initially this is separated from the file scan, only to provide Tkinter with ease
        when doing directory treestructure. It needs parents to come before children, to avoid this, folders first"""
        for (dirpath, dirnames, filenames) in walk(self.my_path):
            self.current_foldername = dirpath + "\\"
            self.add_to_list_if_not_exist(str(self.current_foldername))
            self.node_counter()

    def scanner_for_files(self):
        """Scans for files, after calling the folder scan within"""
        self.scanner_for_folders()

        for (dirpath, dirnames, filenames) in walk(self.my_path):
            for file in filenames:
                self.current_filename = file
                full_file_path = dirpath + "\\" + self.current_filename
                self.add_to_list_if_not_exist(full_file_path)
                self.node_counter()
                print(self.current_filename, self.parent_node())

    def get_complete_scan(self):
        self.scanner_for_folders()
        self.scanner_for_files()

        return self.folder_and_file_with_id
