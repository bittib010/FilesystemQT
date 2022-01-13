try:
    # Python2
    import Tkinter as tk
    import ttk
    import sqlite3

except ImportError:
    # Python3
    import tkinter as tk
    from tkinter import ttk
    from tkinter.messagebox import showinfo
    import sqlite3
    from itertools import permutations


class FiletreeInfoApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (width, height))
        #self.root.attributes("-fullscreen", True)  # use "-fullscreen to get fullscreen

        ##############
        # Window Title
        ##############

        app_title = "File Structure Info"
        self.root.title(app_title)

        ########################
        # Upper and lower Frames
        ########################

        self.upper_frame = ttk.Frame(root, relief="sunken", height=120)
        self.upper_frame.pack(fill="x", pady=15, padx=15)

        self.lower_frame = ttk.Frame(self.root, relief="sunken")
        self.lower_frame.pack(fill="both", padx=15, pady=15, expand=True)

        ########################
        # Lower frames' Treeview
        ########################

        self.db_reader = ttk.Treeview(self.lower_frame, columns=("#0", "#1"), selectmode="browse")

        ysb = ttk.Scrollbar(self.db_reader, orient='vertical', command=self.db_reader.yview)
        xsb = ttk.Scrollbar(self.db_reader, orient='horizontal', command=self.db_reader.xview)

        self.db_reader.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.db_reader.heading('#0', text='Filename', anchor='w')
        self.db_reader.column('#0', minwidth=25, width=400)
        self.db_reader.heading('#1', text="ID", anchor="e")
        self.db_reader.column("#1", width=30)
        self.db_reader.pack(padx=30, pady=30, fill="both", side="left", expand=True)
        self.db_reader.bind("<<TreeviewSelect>>", self.db_reader_selector())

        ysb.pack(fill="y", anchor="e", side="right")
        xsb.pack(fill="x", anchor="s", side="bottom")

        #####################
        # Information textbox
        #####################

        self.info_text = tk.Text(self.lower_frame, width=100)
        self.info_text.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        # Button updater based on selection
        self.update_btn = ttk.Button(self.upper_frame, text="Show Selected Info", command=self.textretrieve_query)
        self.update_btn.pack(pady=30, padx=30, side="left", anchor="e")

        ####################
        # Upper frame layout
        ####################

        self.tag_search = tk.StringVar(self.upper_frame, name="Entered tag(s)")
        self.search_btn = ttk.Button(self.upper_frame, text="Search", command=self.query_search_db)
        self.search_btn.pack(pady=30, padx=30, side="left", anchor="w")
        self.show_full_db_btn = ttk.Button(self.upper_frame, text="Show full DB", command=self.query_full_db)
        self.show_full_db_btn.pack(pady=30, padx=30, side="left")

        self.search_text = tk.Entry(self.upper_frame, text="Enter space separated tags", textvariable=self.tag_search)
        self.search_text.pack(pady=30, padx=30, side="left", anchor="w")

    def db_id_textretrieve(self, event):
        # TODO: Change Filename to Tags
        self.sql = """SELECT Tags FROM Windows10 WHERE Node = {}""".format(event)
        return self.sql

    def textretrieve_query(self):
        conn = sqlite3.connect('Win10.db')
        c = conn.cursor()
        sql = self.db_id_textretrieve(self.db_reader_selector()[0])
        c.execute(sql)
        records = c.fetchall()
        for record in records:
            self.info_text.delete('1.0', "end")
            self.info_text.insert('1.0', record)

        conn.commit()
        conn.close()

    def db_reader_selector(self):
        return self.db_reader.selection()

    def view_full_db(self):
        return "SELECT * FROM Windows10"

    def search(self, searchtags):
        my_tags = searchtags.get().strip(" ").split(" ")
        combinations = ["'%" + "%".join(tag) + "%'" for tag in list(permutations(my_tags))]
        sql = """SELECT * FROM Windows10 WHERE Filename LIKE {0}""".format(
            " OR Filename LIKE ".join(_ for _ in combinations))
        return sql

    def query_full_db(self):
        self.db_reader.delete(*self.db_reader.get_children())
        conn = sqlite3.connect('windows_iterator/Win10.db')
        c = conn.cursor()
        c.execute(self.view_full_db())
        records = c.fetchall()

        # Add data to ttk treeview
        counter = 0
        for record in records:
            # params: 1st: 2nd: where to insert, values: data to add to next iteration of columns, iid: ,
            # open: open/closed folder, text: insert text to first special column

            self.db_reader.insert('', "end", values=record[0], iid=record[0], open=False, text=record[1])
            # 0th index is hardcoded to show path name of root. Node starts at 1
            if record[7] == 0:
                counter +=1
                continue
            if counter != 0:
                # params: ID, Parent, where to insert
                self.db_reader.move(record[0], record[7], "end")

            counter += 1
        conn.commit()
        conn.close()

    def query_search_db(self):
        self.db_reader.delete(*self.db_reader.get_children())
        conn = sqlite3.connect('windows_iterator/Win10.db')
        c = conn.cursor()
        c.execute(self.search(self.tag_search))
        records = c.fetchall()

        # Add data to ttk treeview
        counter = 0
        for record in records:
            # params: 1st: 2nd: where to insert, values: data to add to next iteration of columns, iid: ,
            # open: open/closed folder, text: insert text to first special column

            self.db_reader.insert('', "end", text=record[1])

            counter += 1
        conn.commit()
        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    myApp = FiletreeInfoApp(root)
    root.attributes('-toolwindow', True)
    myApp.query_full_db()
    root.mainloop()
