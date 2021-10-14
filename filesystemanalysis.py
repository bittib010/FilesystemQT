import os


class FilesystemScanner:
    def __init__(self, folder_list=None, current_filename="", current_folder_path="", node=0,
                 current_full_file_path=""):
        if folder_list is None:
            self.folder_and_file_with_id = {}
        self.my_path = "F:\Bilde"
        self.current_full_file_path = current_full_file_path
        self.current_filename = current_filename
        self.current_folder_path = current_folder_path
        self.node = node

    def is_folder(self, current_file):
        return current_file[-1] == "/"

    def add_to_list_if_not_exist(self, folder_or_file):
        """Adds to list of folders if it does not exist already."""
        if folder_or_file not in self.folder_and_file_with_id:
            self.folder_and_file_with_id[str(self.node)] = [folder_or_file]
            if self.node is not None:
                self.folder_and_file_with_id[str(self.node)].append(str(self.parent_node()))

    def node_counter(self):
        """ID/node counter for every file and folder"""
        self.node += 1

    def parent_node(self):
        """"""

        for node_id, path in self.folder_and_file_with_id.items():
            splitted_path = self.current_full_file_path.split("\\")
            files_parent = "\\".join(splitted_path)[0:-1]
            print(self.node, files_parent, path[0])
            if files_parent == path[0]:
                return node_id
            elif self.current_folder_path == path:
                return node_id

    def scanner_for_folders(self):
        """Scanner for folders. Initially this is separated from the file scan, only to provide Tkinter with ease
        when doing directory treestructure. It needs parents to come before children, to avoid this, folders first"""
        for (dirpath, dirnames, filenames) in os.walk(self.my_path):

            #self.current_folder_path = dirpath + "\\"
            self.add_to_list_if_not_exist(str(self.current_folder_path))

            # Node counter has to be the last action
            self.node_counter()

    def scanner_for_files(self):
        """Scans for files, after calling the folder scan within"""
        self.scanner_for_folders()

        for (folder, subfolders, filenames) in os.walk(self.my_path):
            for file in filenames:
                self.current_filename = file
                self.current_full_file_path = os.path.join(os.path.abspath(folder), file)
                self.add_to_list_if_not_exist(self.current_full_file_path)

                # Node counter has to be the last action
                self.node_counter()

    def get_complete_scan(self):
        self.scanner_for_folders()
        self.scanner_for_files()

        return self.folder_and_file_with_id
