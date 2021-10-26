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

        drop_if_exist = "DROP TABLE IF EXISTS {}".format(self.table_name)
        self.conn.execute(drop_if_exist)

        create_table = '''CREATE TABLE IF NOT EXISTS {}
                ("Path"	            TEXT NOT NULL,
        	    "Beginner Info"	    TEXT,
        	    "Intermediate Info"	TEXT,
        	    "Advanced Info"	    TEXT,
        	    "Tags"	            TEXT,
        	    "Parent"	        INTEGER,
        	    "isFolder"	        INTEGER,
        	    "fileExt"           TEXT,
        	    "MD5"               TEXT,
        	    "Updated"           TEXT,
        	    "See also"          TEXT
        	    )'''.format(self.table_name)
        self.conn.execute(create_table)
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
            self.conn.execute(insert_into, (path, md5, isFolder, update_date))
            self.conn.commit()
            print("Updated")

    def insert_db_from_filescan(self, path, md5, isFolder):
        init_date = datetime.datetime.now()
        insert_into = '''INSERT INTO {} (Path,MD5,isFolder,Updated) VALUES(?, ?, ?, ?)'''.format(self.table_name)
        self.conn.execute(insert_into, (path, md5, isFolder, init_date))
        self.conn.commit()

    def find_rowid(self):
        query = '''SELECT rowid, WHERE {} '''
