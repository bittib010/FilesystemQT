from os import walk


class FilesystemScanner:
    def __init__(self, folder_list=None, current_filename="", node=0):
        if folder_list is None:
            self.folder_and_file_with_id = {}
        self.my_path = "C:\\"
        self.current_filename = current_filename
        self.node = node

    def is_folder(self, current_file):
        return current_file[-1] == "/"


    def add_to_folder_list_if_not_exist(self, folder):
        """Adds to list of folders if it does not exist already. Should be used before adding files, to make IDs
            work better with treeview hierarchy in Tkinter. If a folder has a higher ID than its children files, it
            will not work."""
        if folder not in self.folder_and_file_with_id:
            self.folder_and_file_with_id[str(self.node)] = folder

    def add_to_file_list_if_not_exist(self, file):
        if file not in self.folder_and_file_with_id:
            self.folder_and_file_with_id[str(self.node)] = file


    def node_counter(self):
        """Keeps track over the IDs generated for each file and folder"""
        self.node += 1

    def parent_node(self):
        """if path ends with \\ its a folder
                if folder_path.split('\\')[0:-1] in folder_and_file_with_id:
                    folder_parent = folder_and_file_with_id[folder.split()[0:-1]]
                elif file_path.split('\\')[0:-1] in folder_and_file_with_id:
                    file_parent = folder_and_file_with_id[folder.split()[0:-1]]
                    """
        pass

    def scanner_for_folders(self):
        for (dirpath, dirnames, filenames) in walk(self.my_path):
            self.add_to_folder_list_if_not_exist(str(dirpath + "\\"))
            self.node_counter()
            print(self.node, dirpath + "\\")

    def scanner_for_files(self):
        """Scans for files, after calling the folder scan within"""
        self.scanner_for_folders()

        for (dirpath, dirnames, filenames) in walk(self.my_path):
            for file in filenames:
                full_file_path = dirpath + "\\" + file
                self.add_to_file_list_if_not_exist(full_file_path)
                self.node_counter()
                print(self.node, full_file_path)


    def complete_scan(self):
        return self.folder_and_file_with_id
