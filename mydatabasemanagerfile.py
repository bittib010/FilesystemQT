import sqlite3
import datetime


class MyDatabaseManager:
    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

    def initialize_db(self):
        """Function to open database, create if not exists"""
        print("Opened database successfully")

        # drop_if_exist = "DROP TABLE IF EXISTS {}".format(self.table_name)
        # self.cur.execute(drop_if_exist)

        create_table = '''CREATE TABLE IF NOT EXISTS {}
                ("Path"	            TEXT NOT NULL,
        	    "Information"	    TEXT,
        	    "Tags"	            TEXT,
        	    "Parent"	        INTEGER,
        	    "isFolder"	        INTEGER,
        	    "fileExt"           TEXT,
        	    "MD5"               TEXT,
        	    "Updated"           TEXT,
        	    "See also"          TEXT
        	    )'''.format(self.table_name)
        self.cur.execute(create_table)
        print("Table created successfully")

    def update_db(self, path, md5, isFolder):
        query = '''SELECT Path FROM {} WHERE Path = "{}"'''.format(self.table_name, path)
        result = self.conn.execute(query).fetchone()
        print(str(result[0]), "             ", path)
        update_date = datetime.datetime.now()
        if path == result:
            # And check inside if hash has changed. Then need to update modified date.
            hash_query = '''SELECT MD5 FROM {} WHERE MD5 = "{}"'''
            print("Not updated")
            return False
        else:
            insert_into = '''INSERT INTO {} (Path,MD5,isFolder,Updated) VALUES(?, ?, ?, ?)'''.format(self.table_name)
            self.cur.execute(insert_into, (path, md5, isFolder, update_date))
            self.conn.commit()
            print("Updated")

    def my_updater(self, path, md5, isFolder):
        query_path = '''SELECT rowid, Path FROM {} WHERE Path = "{}"'''.format(self.table_name, path)

        # result_hash = ""
        if self.conn.execute(query_path).fetchone() is None:  # Test if returns None.
            result_path = "Please add me"  # Placeholder to specify that it needs to be inserted, it does not exist
            result_hash = "Please add me"
        else:

            result_path = self.conn.execute(query_path).fetchone()[1]
            rowid = self.conn.execute(query_path).fetchone()[0]
            query_hash = '''SELECT MD5 FROM {} WHERE rowid = "{}"'''.format(self.table_name, rowid)

            result_hash = self.conn.execute(query_hash).fetchone()[0]
        current_time = datetime.datetime.now()

        if path == result_path and md5 != result_hash:
            query = '''UPDATE {} SET MD5=?, Updated=? WHERE rowid = "{}"'''.format(self.table_name, rowid)
            self.cur.execute(query, (md5, current_time))
        elif path != result_path:
            query = '''INSERT INTO {} (Path, MD5, isFolder, Updated) VALUES (?, ?, ?, ?)'''.format(self.table_name)
            self.cur.execute(query, (path, md5, isFolder, current_time))
        else:
            #print("Path: ", path, "\n", "result_path: ", result_path, "\n", "md5      : ", md5, "\n", "result_hash: ",
            #      result_hash, "\n")
            pass
        self.conn.commit()

    def insert_db_from_filescan(self, path, md5, isFolder):
        init_date = datetime.datetime.now()
        insert_into = '''INSERT INTO {} (Path,MD5,isFolder,Updated) VALUES(?, ?, ?, ?)'''.format(self.table_name)
        self.conn.execute(insert_into, (path, md5, isFolder, init_date))
        self.conn.commit()


    def inserting_parentID(self):
        query = '''SELECT rowid, Path FROM {}'''.format(self.table_name)
        all_paths = self.cur.execute(query).fetchall()

        for rowid, path in all_paths:
            parent_path_split = path.split("\\")
            if rowid == 1:
                continue
            if path[-1] == "\\":
                parent_path_joined = "\\".join(parent_path_split[:-2]) + "\\"
                parent_path_joinedads = "\\".join(parent_path_split[:-2]) + "\\"
            else:
                parent_path_joined = "\\".join(parent_path_split[:-1]) + "\\"

            parent_query = '''SELECT rowid FROM {} WHERE Path = "{}"'''.format(self.table_name, parent_path_joined)
            parent_paths = self.cur.execute(parent_query).fetchone()

            update_parentID = '''UPDATE {} SET Parent=? WHERE rowid = "{}"'''.format(self.table_name, rowid)
            self.cur.execute(update_parentID, (parent_paths))
            self.conn.commit()



    def close_db(self):
        self.conn.close()
