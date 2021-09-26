import sqlite3


class DatabaseManager():
    def __init__(self, db_name):
        self.db_name = db_name

    def initialize_db(self, db_name):
        """Function to open database, create if not exists"""
        conn = sqlite3.connect(db_name)
        print("Opened database successfully")
        conn.execute('''DROP TABLE IF EXISTS {db_name}''')
        conn.execute('''CREATE  TABLE IF NOT EXISTS Windows10 
                ("Node"	            INTEGER NOT NULL,
        	    "Filename"	        TEXT,
        	    "Path"	            TEXT    NOT NULL,
        	    "Beginner Info"	    TEXT    DEFAULT 'Info',
        	    "Intermediate Info"	TEXT    DEFAULT 'Info',
        	    "Advanced Info"	    TEXT    DEFAULT 'Info',
        	    "Tags"	            TEXT    DEFAULT 'separated by whitespace tags',
        	    "Parent"	        INTEGER NOT NULL,
        	    "isFolder"	        INTEGER DEFAULT NULL,
        	    "fileExt"           TEXT DEFAULT NULL,
        	    PRIMARY             KEY("Node")
            )''')
        print("Table created successfully")

    def update_db(self):
        pass