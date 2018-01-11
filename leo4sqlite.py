#leo4sqlite.py

#test msg

c.__ = {}

import leo.core.leoGlobals
from leo.core.leoQt import QtWidgets
import leo.commands.controlCommands as controlCommands

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QDesktopWidget
from PyQt5.QtGui import QIcon
import subprocess
import sys, os, re
import sqlite3
def import_table1(col_nums, col_names, col_types, blob_col, p):

    table_name = c.__['table_name']
    filepath = c.__['db_filename']
    
    num_cols = 0
    for col in col_nums:
        num_cols = num_cols + 1
    
    g.es("\nimporting table: " + table_name + "\n\n(layout 1)\n")
                    
    rx = 0
    delim = ", "
    new_row = ""
    
    p.b = p.b + "filepath: " + str(filepath) + "\n\n"
    p.b = p.b + str(col_names) + "\n"
    p.b = p.b + str(col_types) + "\n\n"

    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM " + table_name):
    
        cx = 0 
        if row != "":
            cols = re.split(delim, str(row))

            ix = 0
            for col in cols:
                if col != "":
                    new_row = new_row + col + ", "
                    cx = cx + 1
                new_row = re.sub(r'[\"]', " ", str(new_row))   
                                
            p.b = p.b + str(new_row[1:-3]) + "\n"
            new_row = ""
            rx = rx + 1       
    
    g.es("done\n")
    c.redraw()
    headline = ("@tbl " + table_name)    
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
def import_table2(p, col_nums, col_names, col_types, blob_col):

    db_filename = c.__['db_filename']
    table_name = c.__['table_name']

    num_cols = 0
    for col in col_nums:
        num_cols = num_cols + 1
    
    idx = 0
    rx = 0
    
    lines = re.split(r'\n', p.b)

    p.b = p.b + "filepath: " + str(db_filename) + "\n\n"
    p.b = p.b + str(col_names) + "\n"
    p.b = p.b + str(col_types) + "\n\n"
        
    g.es("\nimporting table: " + table_name + "\n\n(layout 2)\n")

    rows = []
    
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM " + table_name):    
        rows.append(row)
    
        idx = idx + 1  
        if idx == 1:
            p = p.insertAsNthChild(1)
        else:
            p = p.insertAfter()

        delim = ","
        new_row = ""
        rx = rx + 1
        
        if row != "":
            cols = re.split(delim, str(row))
            for col in cols:
                new_row = new_row + col + ","
            new_row = re.sub(r'[\"\'\s]', "", str(new_row))
            final_row = re.sub(r',', ", ", str(new_row))
        p.h = str(final_row[1:-3])
    
    g.es("done\n")
    c.redraw()        
    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
def import_table3(p, col_nums, col_names, col_types, blob_col):

    db_filename = c.__['db_filename']
    table_name = c.__['table_name']

    g.es("\nimporting table: " + table_name + "\n\n(layout 3)\n")

    conn = sqlite3.connect(db_filename)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("select * from " + table_name)
    row = cursor.fetchone()
    names = row.keys()

    rx = 0
    cx = 0
    delim = ", "
    new_row = ""
    num_cols = 0

    p.b = p.b + "filepath: " + str(db_filename) + "\n\n"
    p.b = p.b + str(col_names) + "\n"
    p.b = p.b + str(col_types) + "\n\n"

    for col_num in col_nums:
        num_cols = num_cols + 1
    
    cx = 0
    for col_name in names:
        if cx == 0:
            p = p.insertAsLastChild()
        else:
            p = p.insertAfter()
        
        p.h = col_name
        c.redraw()
        
        rx = 0
        rows = []
        for row in cursor.execute("SELECT * FROM " + table_name):
            rows.append(str(row[cx]))
            p.b = p.b + (str(row[cx]) + "\n")
            rx = rx + 1            
            
        cx = cx + 1

    g.es("done\n")
        
    c.redraw()
    headline = ("@tbl " + table_name)    
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
def import_table4(p, col_nums, col_names, col_types, blob_col):

    db_filename = c.__['db_filename']
    table_name = c.__['table_name']
    
    g.es("\nimporting table: " + table_name + "\n\n(layout 4)\n")

    num_cols = 0
    for col_num in col_nums:
        num_cols = num_cols + 1

    idx = 0

    p.b = p.b + "filepath: " + str(db_filename) + "\n\n"
    p.b = p.b + str(col_names) + "\n"
    p.b = p.b + str(col_types) + "\n\n"

    
    for col_name in col_names:
        if idx == 0:
            p = p.insertAsLastChild()
        else:
            p = p.insertAfter()
            
        p.h = col_name
    
        i = 0
        z = 0
        rx = 0
        cx = 0
        rows = []
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("select * from " + table_name)
        results = cursor.fetchall()
        num_rows = len(results)
        
        while rx < num_rows:
            for row in cursor.execute("select * from " + table_name):
                if i == 0:
                    p = p.insertAsLastChild()
                else:
                    p = p.insertAfter()
                            
                new_row = re.sub(r'[\(\)\"]', " ", str(row))
                new_row = new_row.lstrip()
                new_row = re.split(r',', new_row)
                rows.append(new_row)
                
                p.h = str(rows[rx][cx + idx])
                
                i = i + 1
                rx += 1

            p = p.parent()   
            if idx >= num_rows:
                break
            new_row = re.sub(r'[\[\]\'\"\s]', "", str(rows[idx]))        
            new_row = re.sub(r',', ", ", new_row) 
            cx += 1
        idx += 1
    
    p = p.parent()
    p.contract()

    g.es("done\n")
    c.redraw()
    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
def export_table1(p, num_cols, col_names, col_types, blob_col):
    
    hlines = []
    
    def place_holder(line):
        return '({})'.format(', '.join('?' * len(line)))
    
    table_name = c.__['table_name']

    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))        
    c.selectPosition(tbl_node)
    c.redraw()
    p = c.p
    
    g.es("\nexporting table " + table_name + "\n\n(layout 1)\n")

    lines = re.split("\n", p.b)

    db_file_path = lines[0]

    new_names = re.sub(r'[\"\'\[\]\s]', "", str(col_names))
    new_types = re.sub(r'[\"\'\[\]\s]', "", str(col_types))

    split_names = re.split(r',', str(new_names))
    split_types = re.split(r',', str(new_types))
    
    sql = "("
    for i in range(len(split_names)):
        sql = sql + split_names[i] + " " + split_types[i] + ", "
    sql = sql[:-2]
    sql = sql + (")")

    lines = lines[5:]
    
    db_filename = c.__['db_filename']
    
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    if (table_name,) in cur.execute(statement).fetchall():
        overwrite = g.app.gui.runAskYesNoDialog(c, "overwrite existing table?", message="a table by that name already exists.\nreplace it with current table?") 
        if overwrite == "no":
            print("cancelled\n")
            return
        print("table: '%s' exists" % table_name)
        cur.execute("DROP TABLE " + table_name)
        print("\ndropping old table")
    cur.execute("CREATE TABLE " + table_name + " " + sql)
    print("creating new table")

    for line in lines:    
        if line != "":
            cells = re.split(",", line)         
            plh = place_holder(cells)
            cur.execute("insert into " + table_name + " values {} ".format(plh), cells)
            conn.commit()
        else:
            g.es("\ndone\n")
            return
def export_table2(p, col_nums, col_names, col_types, blob_col):
    
    hlines = []
    table_name = c.__['table_name']
    db_filename = c.__['db_filename']
   
    def place_holder(line):
        return '({})'.format(', '.join('?' * len(line)))

    g.es("\nexporting table: " + table_name + "\n\n(layout 2)\n") 

    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
    c.redraw()
    p = c.p
    lines = re.split(r"\n", p.b)
    db_file_path = lines[0]
    names = lines[2]
    types = lines[3]
    
    for p in p.children():
        hlines.append(p.h)
    
    new_names = re.sub(r'[\"\'\[\]\s]', "", str(names))
    new_types = re.sub(r'[\"\'\[\]\s]', "", str(types))
    
    split_names = re.split(r',', str(new_names))
    split_types = re.split(r',', str(new_types))

    sql = "("
    for i in range(len(split_names)):
        sql = sql + split_names[i] + " " + split_types[i] + ", "
    sql = sql[:-2]
    sql = sql + (")")


    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    if (table_name,) in cur.execute(statement).fetchall():
        overwrite = g.app.gui.runAskYesNoDialog(c, "overwrite existing table?", message="a table by that name already exists.\nreplace it with current table?") 
        if overwrite == "no":
            print("cancelled\n")
            return
        print("table: '%s' exists" % table_name)
        cur.execute("DROP TABLE " + table_name)
        print("\ndropping old table")
    cur.execute("CREATE TABLE " + table_name + " " + sql)
    print("creating new table")
    
    for line in hlines:    
        if line != "":
            cells = re.split(",", line)
            
            plh = place_holder(cells)
            cur.execute("insert into " + table_name + " values {} ".format(plh), cells)
            conn.commit()
    g.es("\ndone\n")
def export_table3(p, col_nums, col_names, col_types, blob_col):

    def place_holder(line):
        return '({})'.format(', '.join('?' * len(line)))

    table_name = c.__['table_name']
    db_filename = c.__['db_filename']

    g.es("\nexporting table: " + table_name + "\n\n(layout 3)\n") 
    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
    c.redraw()
    p = c.p
    lines = re.split(r'\n', str(p.b))
    db_file_path = lines[0]
    names = lines[2]
    types = lines[3]

    new_names = re.sub(r'[\"\'\[\]\s]', "", str(names))
    new_types = re.sub(r'[\"\'\[\]\s]', "", str(types))
    split_names = re.split(r',', str(new_names))
    split_types = re.split(r',', str(new_types))

    blines = []
    row = []
    rows = []
    cols = []
    all_cols = []
    num_rows = 0
    num_cols = 0
    split_blines = []
    clean_blines = []
    
    for p in p.children():

        split_blines = re.split(r'\n', p.b)
        num_rows = (len(split_blines))
        clean_blines = re.sub(r'[\'\[\]\s]', "", str(split_blines))
        clean_blines = clean_blines[:-1]
        clean_blines = re.split(r',', clean_blines)
        cols.append(clean_blines)
        num_cols = num_cols + 1
    
    sql = "("
    for i in range(len(split_names)):
        sql = sql + split_names[i] + " " + split_types[i] + ", "
    sql = sql[:-2]
    sql = sql + (")")

    lines = lines[3:]

    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    if (table_name,) in cur.execute(statement).fetchall():
        overwrite = g.app.gui.runAskYesNoDialog(c, "overwrite existing table?", message="a table by that name already exists.\nreplace it with current table?") 
        if overwrite == "no":
            print("cancelled\n")
            return
        print("table: '%s' exists" % table_name)
        cur.execute("DROP TABLE " + table_name)
        print("\ndropping old table")
    cur.execute("CREATE TABLE " + table_name + " " + sql)
    print("creating new table")
    
    x = 0
    z = 0
    row = []
    rows = []
    while x < num_rows - 1:
        for i in range(len(cols)):
            row.append((cols[i][x]))
        row = re.sub(r'[\[\]\'\"\s]', "", str(row))
        row = re.sub(r',', ", ", row) 
        row = re.split(r',', row)
        cells = row[:int(num_cols)]
        plh = place_holder(cells)
        cur.execute("insert into " + table_name + " values {} ".format(plh), cells)
        conn.commit()
        rows = rows[num_cols:]
        z += 1
        if cells == ['']:
            print("\ntriggd")

        rows.append(row)
        row = row[num_cols:]
        x += 1    
    
    row = rows[0][:num_cols]
    row = rows[0][num_cols:num_cols * num_rows]
    
    row = row[num_cols:]
            
    print("\ndone\n")
def export_table4(p, col_nums, col_names, col_types, blob_col):
    
    def place_holder(line):
        return '({})'.format(', '.join('?' * len(line)))

    col_hlines = []
    row_hlines = []
    new_row = []
    hline_rows = []
    hline_cols = []
    
    db_filename = c.__['db_filename']
    table_name = c.__['table_name']
    layout = c.__['layout']
    
    g.es("\nexporting table: " + table_name + "\n\n(layout 4)\n") 
    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
    c.redraw()
    p = c.p
    
    lines = re.split(r'\n', str(p.b))
    db_file_path = lines[0]
    names = lines[2]
    types = lines[3]
  
    for p in p.children():
        col_hlines.append(p.h)
        for p in p.children():
            row_hlines.append(p.h)

    num_cols = len(col_hlines)
    num_rows =int(len(row_hlines) / num_cols)

    new_names = re.sub(r'[\"\'\[\]\s]', "", str(col_names))
    new_types = re.sub(r'[\"\'\[\]\s]', "", str(col_types))
    
    split_names = re.split(r',', str(new_names))
    split_types = re.split(r',', str(new_types))
    
    sql = "("
    for i in range(len(split_names)):
        sql = sql + split_names[i] + " " + split_types[i] + ", "
    sql = sql[:-2]
    sql = sql + (")")
    
    lines = lines[3:]
    
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    
    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    if (table_name,) in cur.execute(statement).fetchall():
        overwrite = g.app.gui.runAskYesNoDialog(c, "overwrite existing table?", message="a table by that name already exists.\nreplace it with current table?") 
        if overwrite == "no":
            print("cancelled\n")
            return
        print("table: '%s' exists" % table_name)
        cur.execute("DROP TABLE " + table_name)
        print("\ndropping old table")
    cur.execute("CREATE TABLE " + table_name + " " + sql)
    print("creating new table\n")
    
    i = 0
    x = 0
    row = []
    lines = []
    rows = []
    while x < num_rows:
        for i in range(len(col_hlines)):
            row.append(row_hlines[i * num_rows + x])
            i += num_cols
        if row:
            plh = place_holder(row)
            cur.execute("insert into " + table_name + " values {} ".format(plh), row)
            conn.commit()
        row = row[num_cols:]
        x+= 1
    
    g.es("done\n")
class App(QWidget):

    c.__ = {} 
    
    def __init__(self):
        super().__init__()
        self.title = 'leo4sqlite'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

     
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        self.pick_action()
     
        self.show() 

    def get_settings(self):

        p_lst = c.find_h(r'@directory.*\\leo4sqlite-output')
        c.selectPosition(p_lst[0])
        nd_str = str(p_lst[0])
        folder = re.sub(r'^<pos.*@directory\s\"', '', nd_str)
        folder = folder[:-2]
        c.__['sqlite_out_dir'] = folder

        p_lst = c.find_h(r'@directory.*\\leo4sqlite-temp')
        c.selectPosition(p_lst[0])
        nd_str = str(p_lst[0])
        folder = re.sub(r'^<pos.*@directory\s\"', '', nd_str)
        folder = folder[:-2]
        c.__['sqlite_temp_dir'] = folder
        
    def pick_action(self):

        items = ("import table", "export table", "insert blob", "extract blob", "view blob", "open blob", "import database", "export database")
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose an sqlite action:", items, 0, False) 
        
        if okPressed and item == "import table":
            action = "import table"
            c.__['action'] = action
            self.get_ext_db()
            self.select_table()
            self.get_blob_col()
            self.choose_layout()
            self.grand_central()
            
        if okPressed and item == "export table":
            action = "export table"
            c.__['action'] = action
            self.get_int_dbs()
            self.select_table()
            self.get_blob_col()
            self.choose_layout()
            self.grand_central()
        
        if okPressed and item == "view blob":
            action = "view blob"
            c.__['action'] = action
            self.get_settings()
            self.get_ext_db()
            self.select_table()
            self.get_blob_col()
            self.view_blob()
            self.grand_central()
        
        if okPressed and item == "insert blob":
            action = "insert blob"
            c.__['action'] = action
            self.get_ext_db()
            self.select_table()
            self.get_blob_col()
            self.insert_blob()
        
        if okPressed and item == "extract blob":
            action = "extract blob"
            c.__['action'] = action
            self.get_settings()
            self.get_ext_db()
            self.select_table()
            self.get_blob_col()
            self.extract_blob()
        
        if okPressed and item == "open blob":
            action = "open blob"
            c.__['action'] = action
            self.get_settings()
            self.get_ext_db()
            self.select_table()
            self.get_blob_col()
            self.open_blob()
    def get_ext_db(self):

        def get_filename(path):
            filename = os.path.basename(path.rstrip('/'))
            fn = filename
                
        db_fname = g.app.gui.runOpenFileDialog(c, title="Select SQLite Database", \
        filetypes=[("SQLite Database File", "*.db3"), ("SQLite3 Database File", "*.db")], \
        defaultextension=".db3", multiple=False)
            
        no_path = get_filename(db_fname)
        c.__['db_filename'] = db_fname
    def get_int_dbs(self):
        
        def get_filename(path):
            fn_lst = []
            filename = os.path.basename(path.rstrip('/'))
            fn_lst.append(filename)
            return filename
        
        db3_lst = c.find_h(r'^.*@db3.*$')   
        #print(db3_lst)

        if db3_lst:
            new_db3_lst = []
            new_db3_cleans = []
            for db3 in db3_lst: 
                new_db3 = re.sub(r'^.*@db3', '', str(db3))
                print(new_db3)
                new_db3 = new_db3[:-1]
                new_db3 = new_db3.lstrip()
                new_db3_lst.append(new_db3)
                new_db3_clean = get_filename(new_db3)
                new_db3_cleans.append(new_db3_clean)

            QInputDialog.setStyleSheet(self, "padding: 3px");
            QInputDialog.setStyleSheet(self, "background: white");
            item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose internal database: ", new_db3_lst, 0, False)
            print(item)
            c.__['db_filename'] = item
        else:
            g.es('no internal databases')
            options()
    def select_table(self):

        db_filename = c.__['db_filename']
        tbl_names = []
            
        #get table list
        conn = sqlite3.connect(db_filename)
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        #create table name list and string
        tbl_nm_str = ''
        for name in res:
            tbl_names.append(name[0])
            tbl_nm_str += "\"" + name[0] + "\", "
        tbl_nm_str = tbl_nm_str[:-3] + "\""

        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","select a table: ", tbl_names, 0, False)
        
        c.__['table_name'] = item
        c.__['tbl_names'] = tbl_names
        

    def get_blob_col(self):
        
        col_nums = []
        col_names = []
        col_types = []
        num_cols = 0
        file_col = 0
        blob_col = 0
        ext_col = 0
        
        db_filename = c.__['db_filename']
        table_name = c.__['table_name']
        
        conn = sqlite3.connect(db_filename)
        cur = conn.cursor()
        
        ix = 0
        for row in cur.execute("pragma table_info(" + table_name + ")").fetchall():
        
            col_nums.append(str(row[0]))
            col_names.append(str(row[1]))
            col_types.append(str(row[2]))
        
            if row[2] == "BLOB":
                blob_col = ix
            
            if row[1] == "Filename":
                file_col = ix
            
            if row[1] == "Extension":
                ext_col = ix    
            
            ix = ix + 1
        
        for i in range(len(col_nums)):
            num_cols += 1
        
        c.__['num_cols'] = num_cols
        c.__['col_names'] = col_names
        c.__['col_types'] = col_types
        c.__['col_nums'] = col_nums
        c.__['blob_col'] = blob_col
        c.__['file_col'] = file_col
        c.__['ext_col'] = ext_col
    def view_blob(self):

        img_types = ['.png', '.jpg', '.bmp', '.gif']
        vid_types = ['.mp4', '.avi', '.wmv', '.flv', '.mov', '.mkv']
        
        
        file_col = c.__['file_col']
        ext_col = c.__['ext_col']
        col_names = c.__['col_names']
        table_name = c.__['table_name']
        db_filename = c.__['db_filename']
        
        def get_extension(path):
            extension = os.path.splitext(path)[1]
            return extension
        def get_filename(path):
            filename = os.path.basename(path)
            return filename    
        
        temp_dir = c.__['sqlite_temp_dir']
        
        items = col_names
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        col, okPressed = QInputDialog.getItem(self, "leo4sqlite","select column to search:", items, 0, False)
        search_col = col
        
        items = []
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        term, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose a search term:", items, 0, False)
        search_term = term
        
        # init
        blob_file = ""
        ablob = []
        blob_col = 3
        blob_nm_lst = []
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term]) 
        row = cursor.fetchone()
        filename = row[file_col]
        extension = row[ext_col]

        filepath = temp_dir + "\\" + filename + extension
        g.es(filepath)

        with open(filepath, "wb") as output_file:               
            cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term]) 
            ablob = cursor.fetchone()
            output_file.write(ablob[blob_col])
            cursor.close()
            
            p = g.findNodeAnywhere(c, "temp")
            c.selectPosition(p)
            p = p.insertAsLastChild()
            c.selectPosition(p)
            p.b = filepath
        
            if extension in img_types: 
                p.h =  (r"@image " + filename + extension)
            if extension in vid_types:
                p.h =  (r"@movie " + filename + extension)
                
            p = c.p
            #p = p.getFirstChild()
            c.selectPosition(p)
            c.redraw()
            
            c.executeMinibufferCommand('vr-show')
            c.redraw()
            c.executeMinibufferCommand('vr-zoom')
            p = p.parent() 
            c.redraw()    
    def open_blob(self):
        
        items = []
        
        ext_col = c.__['ext_col']
        blob_col = c.__['blob_col']
        file_col = c.__['file_col']
        col_names = c.__['col_names']
        table_name = c.__['table_name']
        db_filename = c.__['db_filename']
        out_dir = c.find_h(r'@path out_dir.*')
        sqlite_temp_dir = c.__['sqlite_temp_dir']
        
        p = g.findNodeAnywhere(c, '@data external tools')
        c.selectPosition(p)
        tools = re.split(r'\n', p.b)
        tools = tools[2:-1]
        c.selectThreadBack()
        c.redraw()
        
        items = (col_names)
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","select column to search:", items, 0, False)
        search_col = item
        
        items = []
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose a search term:", items, 0, False)
        search_term = item
                              
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","select external tool:", tools, 0, False)
        ext_tool = item
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term])
        #cursor.execute("select * from " + table_name + " where " + search_col + " = " + search_term)
        row = cursor.fetchone()
        filename = row[file_col]
        filename = os.path.basename(filename)
        extension = row[ext_col]

        filepath = (sqlite_temp_dir + "\\" + filename + extension)
        g.es("fp: " + filepath)

        with open(filepath, "wb") as output_file:        
            cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term])
            #cursor.execute("select * from " + table_name + " where " + search_col + " = " + search_term)
            ablob = cursor.fetchone()
            output_file.write(ablob[blob_col])
            cursor.close()

            p = subprocess.Popen([ext_tool, filepath])

    def insert_blob(self):
            
        import os.path
        
        def place_holder(line):
            return '({})'.format(', '.join('?' * len(line)))
        
        col_vals = []
        
        db_filename = c.__['db_filename']
        table_name = c.__['table_name']
        num_cols = c.__['num_cols']
        col_names = c.__['col_names']
        
        str_col_names = str(col_names)
        str_col_names = str_col_names[1:-1]
        print("col_names: " + str_col_names)

        for i in range(len(col_names)):
            if col_names[i] != "Blobs" and col_names[i] != "Filename" and col_names[i] != "Extension":
                text, okPressed = QInputDialog.getText(self, table_name, col_names[i], QLineEdit.Normal, "")
                if okPressed and text != '':
                    print(col_names[i] + " " + text)
                    col_vals.append(text)
        
        str_col_names = str(col_names)
        str_col_names = str_col_names[1:-1]
        print(str_col_names)
                    
        blob_filepath = g.app.gui.runOpenFileDialog(c, title="select file to insert:", \
        filetypes=[("binary files", "*.*")], \
        defaultextension="*.*", multiple=False)
        full_filename = os.path.basename(blob_filepath)
        filename, extension = os.path.splitext(full_filename)
        #g.es(filename + extension)

        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        with open(blob_filepath, "rb") as input_file:
            ablob = input_file.read()
            cells = col_vals
            cells.append(sqlite3.Binary(ablob))
            cells.append(filename)
            cells.append(extension)
            plh = place_holder(cells)
                            
            cursor.execute("insert into " + table_name + " values {} ".format(plh), cells)
            conn.commit()
            
            print("done")
    def extract_blob(self):
        
        ablob = []
        blob_col = 3
        search_items = []
        filenames = []

        file_col = c.__['file_col']
        ext_col = c.__['ext_col']
        blob_col = c.__['blob_col']
        col_names = c.__['col_names']
        table_name = c.__['table_name']
        db_filename = c.__['db_filename']

        # select column to search
        
        items = (col_names)
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","select column to search:", items, 0, False)
        
        search_col = item
        
        items = []
        
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose a search term:", items, 0, False)
        
        search_term = item
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        i = 0
        for row in cursor.execute("SELECT * FROM " + table_name):
            if col_names[i] == search_col:
                search_items.append(row[i])

        cursor.execute("select * from " + table_name + " where " + search_col + " = " + search_term)
        row = cursor.fetchone()
        filename = os.path.basename(row[file_col])
        extension = row[ext_col]
        g.es(filename + extension)
        
        sqlite_out_dir = c.__['sqlite_out_dir']
        filepath = sqlite_out_dir + '\\' + filename + extension
        g.es(filepath)
        
        with open(filepath, "wb") as output_file:   
            cursor.execute("select * from " + table_name + " where " + search_col + " = " + search_term) 
            ablob = cursor.fetchone()
            output_file.write(ablob[blob_col])
            cursor.close()
        
        conn.close()
        g.es("done")
    def choose_layout(self):
        
        items = ('one', 'two', 'three', 'four')
            
        QInputDialog.setStyleSheet(self, "padding: 3px");
        QInputDialog.setStyleSheet(self, "background: white");
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose a layout: ", items, 0, False)
        
        c.__['layout'] = item
        
    def grand_central(self):

        db_filename = c.__['db_filename']
        table_name = c.__['table_name']
        col_names = c.__['col_names']
        col_nums = c.__['col_nums']
        col_types = c.__['col_types']
        blob_col = c.__['blob_col']
        layout = c.__['layout']
        action = c.__['action']
            
        if c.__['action'] == 'import table':
        
            db3_h = "@db3 " + str(db_filename)
            p = g.findNodeAnywhere(c, db3_h)
            if p:
                pass
            else:    
                p = c.lastTopLevel().insertAsNthChild(1)
                p.h = "@db3 " + str(db_filename)
                c.redraw(p)

            p = p.insertAsNthChild(1)
            p.h = "@tbl " + str(c.__['table_name'])
            c.selectPosition(p)
            c.redraw(p)
            
            if layout == "one":
                import_table1(col_nums, col_names, col_types, blob_col, p)
        
            if layout == "two":
                import_table2(p, col_nums, col_names, col_types, blob_col)
                
            if layout == "three":
                import_table3(p, col_nums, col_names, col_types, blob_col)
            
            if layout == "four":
                import_table4(p, col_nums, col_names, col_types, blob_col)
            
        
        if c.__['action'] == 'export table':
            
            p = c.p
            
            if c.__['layout'] == "one":
                export_table1(p, col_nums, col_names, col_types, blob_col)
            
            if c.__['layout'] == "two":
                export_table2(p, col_nums, col_names, col_types, blob_col)
                
            if c.__['layout'] == "three":
                export_table3(p, col_nums, col_names, col_types, blob_col)
                
            if c.__['layout'] == "four":
                export_table4(p, col_nums, col_names, col_types, blob_col)
App()

