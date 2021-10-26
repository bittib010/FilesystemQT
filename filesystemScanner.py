import os
import hashlib
from pathlib import Path
from mydatabasemanagerfile import MyDatabaseManager

path = "E:\\Blender"
isFolder = True
fullList = []
currhash = ""
db_name = "testing.db"
table_name = "Windows10"

my_current_db = MyDatabaseManager(db_name, table_name)


#####################################################################
# copied from https://stackoverflow.com/questions/24937495/
# how-can-i-calculate-a-hash-for-a-filesystem-directory-using-python
#####################################################################
def md5_update_from_dir(directory, my_hash):
    assert Path(directory).is_dir()
    for hash_path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        my_hash.update(hash_path.name.encode())
        if hash_path.is_file():
            with open(hash_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    my_hash.update(chunk)
        elif hash_path.is_dir():
            my_hash = md5_update_from_dir(hash_path, my_hash)
    return my_hash


def md5_dir(directory):
    return md5_update_from_dir(directory, hashlib.md5()).hexdigest()


####################################################
# End of copy
####################################################


def file_hasher(hashing_file):
    try:
        if not isFolder:
            with open(hashing_file, "rb") as current:
                readfile = current.read()
                current_hash = hashlib.md5(readfile).hexdigest()
                return current_hash
    except PermissionError:
        current_hash = "Could not hash due to permission"
        return current_hash


for (dirpath, dirnames, filenames) in os.walk(path):
    isFolder = True
    full_dirpath = dirpath + "\\"
    fullList.append([full_dirpath, md5_dir(full_dirpath), isFolder])
    for file in filenames:
        file_path = dirpath + "\\" + file
        isFolder = False
        fullList.append([file_path, file_hasher(file_path), isFolder])

my_current_db.initialize_db()
for file_info in fullList:
    #my_current_db.insert_db_from_filescan(file_info[0], file_info[1], file_info[2])
    my_current_db.my_updater(file_info[0], file_info[1], file_info[2])

    #if my_current_db.update_db(file_info[0], file_info[1], file_info[2]) == False:
        #continue
