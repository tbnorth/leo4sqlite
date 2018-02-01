#@+leo-ver=5-thin
#@+node:tscv11.20180119175627.2: * @file /home/tsc/Desktop/leo-editor-master/leo/plugins/leo4sqlite.py
#@@color
#@+<< docstring >>
#@+node:tscv11.20180119175627.3: ** << docstring >>
#@@nocolor
''' **leo4sqlite v0.31** - by tscv11

|

*Introduction:*

| The script 'leo4sqlite.py' is a Leo-specific python script that provides
| basic import/export functionality between Leo outlines and sqlite3 tables
| as well as blob support  (insert, extract, search for a blob by any value in
| any column, view the blob in the render pane or open it with external tools). 

| Imported tables are stored internally as part of the outline, while exported
| tables (and blobs) are stored in sqlite3 database files.

| Imported tables appear as children of the "data" node (the last top-level
| node). To clear this node of accumulated imports, use the command
| 'sqlite-delete-data'.

| I am considering database level import/export functions to round things
| out if  there's enough interest.
|

*Blobs*

| Blobs are arranged one per row with the other columns in that row
| containing information about them. The last three columns of each row
| are reserved for the blob, the filename, and the extension, in that order.
| Any number of columns may be added  and used to store additional
| information related to the blob (which will precede it in the table).
|

*Development Status:*

| *This script is functional but still needs plenty of bug-fixing and fine-tuning.*
|

**The commands currently added by the plugin are:**
 |
 | sqlite-import-table
 | sqlite-export-table
 | sqlite-insert-blob
 | sqlite-extract-blob
 | sqlite-view-blob
 | sqlite-open-blob
 | sqlite-clear-temp
 | sqlite-delete-data
 | sqlite-purge-files
 |

**How to import a table:**

1. Select "import table" as the sqlite3 action to perform.
2. Choose an external database file
3. Pick a table
4. Select a layout

| *Your imported table should now appear. You're welcome.*  :-)
|

**How to export a table:**

1. Select "export table" as the sqlite3 action to perform.
2. Choose an internal database from those found under the "data" node.
3. Select a table.
4. The correct layout will be read from the table automatically.

| *Your exported table should now be written to the sqlite3 db file.*
|

**How to insert a blob**

1. Select "insert blob" as the sqlite3 action to perform.
2. Choose the target external database file.
3. Pick a 'blob table' where the blob will be stored.
4. Enter information for each column in that blob's row.

| *The blob should now be written to the database file.*
|

**How to extract a blob**

1. Select "extract blob" as the sqlite3 action to perform.
2. Choose the external database file containing the blob.
3. Pick the table containing the blob.
4. Enter a search column and search term.

|  *The matching blob should now be extracted to the*
|  *output folder you've specified in the @settings tree.*
|

**How to view a blob**

1. Select "view blob" as the sqlite3 action to perform.
2. Choose the external database containing the blob you wish to view.
3. Pick the table containing the blob.
4. Specify a search column and search term.

| *The matching blob should now be extracted to the temp folder you've*
| *chosen (in the @settings tree). An @image node is then created for the*
| *blob and the render pane is opened to view it.*
|

**How to open a blob**

1. Select "open blob" as the sqlite3 action to perform.
2. Choose the external database containing the blob you wish to view.
3. Pick the table containing the blob.
4. Specify a search column and search term.
5. Choose an external tool to use when opening the file.

| *The matching blob should now be extracted to the temp folder you've*
| *chosen (in the @settings tree). The file is then opened with the selected*
| *external tool.*
|

**sqlite-clear-temp**

| To remove all temporary blob nodes from the temp node use this command.
| This leaves the files intact.


**sqlite-delete-data**

| This command removes all children of the 'data' node, where all imports
| appear. Use caution!


**sqlite-purge-files**

| This command deletes *all* physical files from the 'leo4sqlite-temp' directory.
|


**Settings**

| There are now four @settings nodes which should be created and placed
| in either the current outline's @settings tree or in myLeoSettings.leo.

| The nodes are:

| @string sqlite_output_dir = "<path>" -> Output directory for extracted blobs.
| @string sqlite_tem_dir = "<path>"     -> Temporary folder for viewed blobs.
| @bool del_blobs_on_exit = 1 (yes) **or** 0 (no)

| And finally,

| @data external tools - this node holds paths to external tools for use when
| opening blobs. The format is simply one full path per line, ending in the name
| of an executable.
|

**Outline Template**

*leo4sqlite_template.leo*

| Included with this distribution you'll find a template made for leo4sqlite that
| includes the standard nodes you'll need, ready for customization.
|

 
contact: tsc.v1.1@gmail.com
'''
#@-<< docstring >>
#@@language python
#@@tabwidth -4
__version__ = '0.031'
#@+<< version history >>
#@+node:tscv11.20180119175627.4: ** << version history >>
#@+at
# version history
# 
# *leo4sqlite.py*
# 
#  **v.010** - first working version of plugin.
# 
#  **v.011** - the import layout is now saved in the @tbl node so the export layout can be chosen automatically.
# 
#  **v.015** - added 'sqlite-clear-data', 'sqlite-reset-temp', and 'sqlite-purge-files'.
# 
#  **v.016** - fixed a bug in 'sqlite-extract-table', thanks to Terry Brown.
# 
#  **v.020** - added command 'sqlite-edit-blob', which enables the user to edit indvidual text columns for a 'blob'.
# 
#  **v.022** - various small fixes and enhancements suggested by Terry Brown
#  
#  **v.023** - dialogs now have the standard Leo icon in the upper-left hand corner.
#  
#  **v.024** - the 'get external database' dialog now has two improved options: 1) all files   or   2) .db .db3 .sqlite .sqlite3
#  
#  **v.026** - added basic error handling
#  
#  **v.029** - added settings to auto-delete temporary blob files on exiting Leo and updated the documentation.
#  
#  **v.030** - removed the unused Leo4SQLiteController node.
# 
#  **v.031** - subclassed custom exceptions instead of creating a separate class for each error.
#  
#@-<< version history >>
#@+<< imports >>
#@+node:tscv11.20180119175627.5: ** << imports >>
import leo.core.leoGlobals as g

import glob
#import sys
import os
import re
import sqlite3
import subprocess

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QDesktopWidget
#@-<< imports >>
#@+others
#@+node:tscv11.20180119175627.6: ** onCreate
def onCreate (tag, keys):
    
    c = keys.get('c')
    c._leo4sqlite = {}

    g.registerHandler('end1', delBlobs(c))
#@+node:tscv11.20180119175627.7: ** init
def init ():

    ok = g.app.gui.guiName() in ('qt','qttabs')
    if ok:
        if 1: # Create the commander class *before* the frame is created.
            g.registerHandler('before-create-leo-frame',onCreate)
        else: # Create the commander class *after* the frame is created.
            g.registerHandler('after-create-leo-frame',onCreate)
        g.plugin_signon(__name__)       
    return ok

#@+node:tscv11.20180119175627.10: ** class InputDialogs
class InputDialogs(QWidget):
    
    #@+others
    #@+node:tscv11.20180119175627.11: *3* __init__
    def __init__(self, c):
        super().__init__()
        self.title = 'leo4sqlite'
        self.setWindowIcon(QtGui.QIcon(r'leo/Icons/application-x-leo-outline.png'))
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        try:
            self.initUI(c)
        except Leo4SqliteError as l4serr:
            g.es("\nleo4sqlite plugin: %s\n" % l4serr.__doc__)  
            return
    #@+node:tscv11.20180119175627.12: *3* initUI
    def initUI(self, c):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        self.pick_action(c)
     
        self.show() 


    #@+node:tsc.20180201065401.1: *3* pick_action
    def pick_action(self, c):
        
        """This is Terry Brown's brainchild. I added 'cmds' to make it easier to customize the routine of functions that is executed before each command (in the future, if needed - plus I'm a lazy typist))."""
        
        action = c._leo4sqlite['action']    
        cmds = ("get_ext_db select_table get_blob_col")
        
        actions = {
            "insert blob": ((cmds) + " insert blob"),
            "extract blob": ((cmds) + " extract blob"),
            "open blob": ((cmds) + " open blob"),
            "view blob": ((cmds) + " view blob"),
            "edit blob": ((cmds) + " edit blob")
        }
        
        if action not in actions:
            raise UnknownActionError()
        for step in actions[action].split():
            method = getattr(self, step)
            method(c)
    #@+node:tscv11.20180119175627.15: *3* get_ext_db
    def get_ext_db(self, c):
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.setStyleSheet('padding: 3px; background: white');
        db_fname, _ = QFileDialog.getOpenFileName(self,"select an external database:", "","sqlite files (*.db *.db3 *.sqlite *.sqlite3);;all files (*.*)", options=options) # tnb
        if db_fname == '':
            raise UserCancel()
            return
        else:
            c._leo4sqlite['db_filename'] = db_fname
    #@+node:tscv11.20180119175627.16: *3* get_int_dbs
    def get_int_dbs(self, c):
        
        def get_filename(path):
            fn_lst = []
            filename = os.path.basename(path.rstrip('/'))
            fn_lst.append(filename)
            return filename
        
        db3_lst = c.find_h(r'^.*@db3.*$')   

        if db3_lst:
            new_db3_lst = []
            new_db3_cleans = []
            for db3 in db3_lst: 
                new_db3 = re.sub(r'^.*@db3', '', str(db3))
                new_db3 = new_db3[:-1]
                new_db3 = new_db3.lstrip()
                new_db3_lst.append(new_db3)
                new_db3_clean = get_filename(new_db3)
                new_db3_cleans.append(new_db3_clean)

            self.setStyleSheet('padding: 3px; background: white');
            item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose internal database.", new_db3_lst, 0, False)
            if not okPressed:
                raise NoInternalDBsError
                return
            else:
                c._leo4sqlite['db_filename'] = item


    #@+node:tscv11.20180119175627.17: *3* select_table
    def select_table(self, c):

        db_filename = c._leo4sqlite['db_filename']
        tbl_names = []
      
        conn = sqlite3.connect(db_filename)
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        tbl_nm_str = ''
        for name in res:
            tbl_names.append(name[0])
            tbl_nm_str += "\"" + name[0] + "\", "
        tbl_nm_str = tbl_nm_str[:-3] + "\""

        self.setStyleSheet('padding: 3px; background: white');
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","select a table: ", tbl_names, 0, False)    
        if not okPressed:
                raise UserCancel()
                return
                
        c._leo4sqlite['table_name'] = item
        c._leo4sqlite['tbl_names'] = tbl_names

    #@+node:tscv11.20180119175627.18: *3* get_blob_col
    def get_blob_col(self, c):
        
        col_nums = []
        col_names = []
        col_types = []
        num_cols = 0
        file_col = 0
        blob_col = 0
        ext_col = 0
        
        db_filename = c._leo4sqlite['db_filename']
        table_name = c._leo4sqlite['table_name']

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
        
        num_cols += len(col_nums) # tnb
        
        # for i in range(len(col_nums)) # tsc
            # num_cols += 1
        
        c._leo4sqlite['num_cols'] = num_cols
        c._leo4sqlite['col_names'] = col_names
        c._leo4sqlite['col_types'] = col_types
        c._leo4sqlite['col_nums'] = col_nums
        c._leo4sqlite['blob_col'] = blob_col
        c._leo4sqlite['file_col'] = file_col
        c._leo4sqlite['ext_col'] = ext_col
    #@+node:tscv11.20180119175627.19: *3* insert_blob
    def insert_blob(self, c):
            
        import os.path
        
        def place_holder(line):
            return '({})'.format(', '.join('?' * len(line)))
        
        col_vals = []
        
        db_filename = c._leo4sqlite['db_filename']
        table_name = c._leo4sqlite['table_name']
        col_names = c._leo4sqlite['col_names']
        
        str_col_names = str(col_names)
        str_col_names = str_col_names[1:-1]

        for i in range(len(col_names)):
            if col_names[i] != "Blobs" and col_names[i] != "Filename" and col_names[i] != "Extension":
                text, okPressed = QInputDialog.getText(self, table_name, col_names[i], QLineEdit.Normal, "")
                if okPressed and text != '':
                    col_vals.append(text)
        
        str_col_names = str(col_names)
        str_col_names = str_col_names[1:-1]
                    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.setStyleSheet('padding: 3px; background: white');
        blob_filepath, _ = QFileDialog.getOpenFileName(self,"select file to insert:", "","binary files (*)", options=options)
        
        full_filename = os.path.basename(blob_filepath)
        filename, extension = os.path.splitext(full_filename)

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
            
            g.es("\ndone\n")
    #@+node:tscv11.20180119175627.20: *3* extract_blob
    def extract_blob(self, c):
        
        ablob = []
        search_items = []

        file_col = c._leo4sqlite['file_col']
        ext_col = c._leo4sqlite['ext_col']
        blob_col = c._leo4sqlite['blob_col']
        col_names = c._leo4sqlite['col_names']
        table_name = c._leo4sqlite['table_name']
        db_filename = c._leo4sqlite['db_filename']

        sqlite_out_dir = c.config.getString("sqlite_output_dir")
        
        if not sqlite_out_dir:
            raise NoOutputDirectory
            return
        
        sqlite_out_dir = sqlite_out_dir[1:-1]
        
        items = (col_names)
        self.setStyleSheet('padding: 3px; background: white');
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","select column to search:", items, 0, False)
        
        search_col = item
        
        items = []    
        self.setStyleSheet('padding: 3px; background: white');
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose a search term:", items, 0, False)
        
        search_term = item
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        i = 0
        for row in cursor.execute("SELECT * FROM " + table_name):
            if col_names[i] == search_col:
                search_items.append(row[i])
        
        cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term]) # tnb
        row = cursor.fetchone()
        filename = os.path.basename(row[file_col])
        extension = row[ext_col]
        
        
        filepath = sqlite_out_dir + '/' + filename + extension
        
        with open(filepath, "wb") as output_file:   
            cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term]) # tnb
            ablob = cursor.fetchone()
            output_file.write(ablob[blob_col])
            cursor.close()
        
        conn.close()
        g.es("\ndone\n")
    #@+node:tscv11.20180119175627.21: *3* open_blob
    def open_blob(self, c):
        
        items = []
        
        ext_col = c._leo4sqlite['ext_col']
        blob_col = c._leo4sqlite['blob_col']
        file_col = c._leo4sqlite['file_col']
        col_names = c._leo4sqlite['col_names']
        table_name = c._leo4sqlite['table_name']
        db_filename = c._leo4sqlite['db_filename']
        
        sqlite_temp_dir = c.config.getString('sqlite_temp_dir')
        
        if not sqlite_temp_dir:
            raise NoTempDirectory
            return
        
        sqlite_temp_dir = sqlite_temp_dir[1:-1]
        
        p = g.findNodeAnywhere(c, '@data external tools')
        c.selectPosition(p)
        tools = re.split(r'\n', p.b)
        tools = tools[2:-1]
        c.selectThreadBack()
        c.redraw()
        
        items = (col_names)
        self.setStyleSheet('padding: 3px; background: white');
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","select column to search:", items, 0, False)
        search_col = item
        
        items = []
        self.setStyleSheet('padding: 3px; background: white');
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose a search term:", items, 0, False)
        search_term = item
                              
        self.setStyleSheet('padding: 3px; background: white');
        item, okPressed = QInputDialog.getItem(self, "leo4sqlite","select external tool:", tools, 0, False)
        ext_tool = item
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term])
        row = cursor.fetchone()
        filename = row[file_col]
        filename = os.path.basename(filename)
        extension = row[ext_col]

        filepath = (sqlite_temp_dir + '//' + filename + extension)

        with open(filepath, "wb") as output_file:        
            cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term])
            ablob = cursor.fetchone()
            output_file.write(ablob[blob_col])
            cursor.close()

            p = subprocess.Popen([ext_tool, filepath])
    #@+node:tscv11.20180119175627.22: *3* view_blob
    def view_blob(self, c):

        img_types = ['.png', '.jpg', '.bmp', '.gif']
        vid_types = ['.mp4', '.avi', '.wmv', '.flv', '.mov', '.mkv']
        
        file_col = c._leo4sqlite['file_col']
        ext_col = c._leo4sqlite['ext_col']
        blob_col = c._leo4sqlite['blob_col']
        col_names = c._leo4sqlite['col_names']
        
        table_name = c._leo4sqlite['table_name']
        db_filename = c._leo4sqlite['db_filename']
        
        temp_dir = c.config.getString("sqlite_temp_dir")
        if not temp_dir:
            raise NoTempDirectory
            return
            
        temp_dir = temp_dir[1:-1]
        
        def get_extension(path):
            extension = os.path.splitext(path)[1]
            return extension
        
        def get_filename(path):
            filename = os.path.basename(path)
            return filename    
            
        items = col_names
        self.setStyleSheet('padding: 3px; background: white');
        col, okPressed = QInputDialog.getItem(self, "leo4sqlite","select column to search:", items, 0, False)
        search_col = col
        
        items = []
        self.setStyleSheet('padding: 3px; background: white');
        term, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose a search term:", items, 0, False)
        search_term = term
        
        ablob = []
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term]) 
        row = cursor.fetchone()
        filename = row[file_col]
        extension = row[ext_col]

        filepath = temp_dir + "//" + filename + extension

        with open(filepath, "wb") as output_file:               
            cursor.execute("select * from %s where %s = ?" % (table_name, search_col), [search_term]) 
            ablob = cursor.fetchone()
            output_file.write(ablob[blob_col])
            cursor.close()
            
            if extension in img_types: 
                ph2b =  (r"@image " + filename + extension)
            if extension in vid_types:
                ph2b =  (r"@movie " + filename + extension)
                
            p = g.findNodeAnywhere(c, "temp")
            c.selectPosition(p)
            
            for child in p.children():
                if child.h == ph2b:
                    c.selectPosition(child)
                    c.executeMinibufferCommand('vr-show')
                    raise NodeExists()
                    return
            
            p = p.insertAsLastChild() # tsc - add option: insert as firstChild
            c.selectPosition(p)
            p.h = ph2b
            p.b = filepath
            
            c.executeMinibufferCommand('vr-show')
            c.redraw()
            p = p.parent() 
            c.redraw()    
    #@+node:tscv11.20180119175627.23: *3* edit_blob
    def edit_blob(self, c):
        
        def place_holder(line):
            return '({})'.format(', '.join('?' * len(line)))
            
        col_names = c._leo4sqlite['col_names']
        table_name = c._leo4sqlite['table_name']
        db_filename = c._leo4sqlite['db_filename']
        
        names = []

        self.setStyleSheet('padding: 3px; background: white');
        name, okPressed = QInputDialog.getItem(self, "leo4sqlite","enter blob name:", names, 0, False)
        blob_name = name
        
        cols = (col_names)

        self.setStyleSheet('padding: 3px; background: white');
        col, okPressed = QInputDialog.getItem(self, "leo4sqlite","select column name:", cols, 0, False)
        edit_col = col
        
        values = []
        
        self.setStyleSheet('padding: 3px; background: white');
        value, okPressed = QInputDialog.getItem(self, "leo4sqlite", "enter new value:", values, 0, False)
        new_val = value
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        cursor.execute("update %s set %s = %s where Filename = ?" % (table_name, edit_col, new_val), [blob_name])
        conn.commit()

        g.es('done')
    #@+node:tscv11.20180119175627.24: *3* get_layout
    def get_layout(self, c):
        
        action = c._leo4sqlite['action']
        table_name = c._leo4sqlite['table_name']    
        
        if action == 'import table':
            items = ('one', 'two', 'three', 'four')
            self.setStyleSheet('padding: 3px; background: white');
            item, okPressed = QInputDialog.getItem(self, "leo4sqlite","choose a layout: ", items, 0, False)
            if not okPressed:
                raise UserCancel()
                return

            c._leo4sqlite['layout'] = item

        if action == 'export table':
            tbl_h = "@tbl " + str(table_name)
            p = g.findNodeAnywhere(c, tbl_h)
            c.selectPosition(p)
            lines = re.split(r'\n', p.b)
            line = lines[5]
            layout = line[8:]
            c._leo4sqlite['layout'] = layout
            g.es('layout: ' + str(layout))
    #@+node:tscv11.20180119175627.25: *3* grand_central
    def grand_central(self, c):
        
        db_filename = c._leo4sqlite['db_filename']
        col_names = c._leo4sqlite['col_names']
        col_nums = c._leo4sqlite['col_nums']
        col_types = c._leo4sqlite['col_types']
        blob_col = c._leo4sqlite['blob_col']
        layout = c._leo4sqlite['layout']
        
        #if c._leo4sqlite['action'] == 'import table':
        db3_h = "@db3 " + str(db_filename)
        p = g.findNodeAnywhere(c, db3_h)
        if p:
            pass
        
        else:    
            p = c.lastTopLevel().insertAsLastChild()
            c.selectPosition(p)
            p.h = "@db3 " + str(db_filename)
            c.redraw(p)
        
            p = p.insertAsNthChild(1)
            c.selectPosition(p)
            p.h = "@tbl " + str(c._leo4sqlite['table_name'])
            c.redraw(p)
        
        if c._leo4sqlite['action'] == 'import table':
            if layout == "one":
                import_table1(self, c, p, col_nums, col_names, col_types, blob_col)
        
            if layout == "two":
                import_table2(self, c, p, col_nums, col_names, col_types, blob_col)
                
            if layout == "three":
                import_table3(self, c, p, col_nums, col_names, col_types, blob_col)
            
            if layout == "four":
                import_table4(self, c, p, col_nums, col_names, col_types, blob_col)
            
        
        if c._leo4sqlite['action'] == 'export table':
            
            p = c.p # tsc - is this necessary?
            
            if c._leo4sqlite['layout'] == "one":
                export_table1(self, c, p, col_nums, col_names, col_types, blob_col)
            
            if c._leo4sqlite['layout'] == "two":
                export_table2(self, c, p, col_nums, col_names, col_types, blob_col)
                
            if c._leo4sqlite['layout'] == "three":
                export_table3(self, c, p, col_nums, col_names, col_types, blob_col)
                
            if c._leo4sqlite['layout'] == "four":
                export_table4(self, c, p, col_nums, col_names, col_types, blob_col)
    #@-others
#@+node:tsc.20180130234230.1: ** class Leo4SqliteError
class Leo4SqliteError(Exception): pass

class Sqlite3DatabaseError(Leo4SqliteError):
    """File is encrypted or is not a database."""
    
class NoInternalDBsError(Leo4SqliteError):
    """No internal database(s) present."""

class NoOutputDirectory(Leo4SqliteError):
    """No output directory specified in settings."""

class NoTempDirectory(Leo4SqliteError):
    """No temp directory specified in settings."""

class UserCancel(Leo4SqliteError):
    """Action cancelled by user."""

class NodeExists(Leo4SqliteError):
    """Node already exists. New node not created."""

class UnknownActionError(Leo4SqliteError):
    """Unknow action error."""
    
#@+node:tsc.20180130145507.1: ** delBlobs
def delBlobs(c): 
    
    del_blobs_on_exit = c.config.getBool('del_blobs_on_exit')
    
    if del_blobs_on_exit == 1:
        sqlite_temp_dir = c.config.getString('sqlite_temp_dir') 
        sqlite_temp_dir = sqlite_temp_dir[1:-1]
            
        os.chdir(sqlite_temp_dir)
        files=glob.glob('*')
        if files:
            for filename in files:
                os.unlink(filename)
#@+node:tscv11.20180119175627.26: ** imports
#@+others
#@+node:tscv11.20180119175627.29: *3* import_table1
def import_table1(self, c, p, col_nums, col_names, col_types, blob_col):

    table_name = c._leo4sqlite['table_name']
    filepath = c._leo4sqlite['db_filename']
    layout = c._leo4sqlite['layout'] 
    
    num_cols = 0
    for col in col_nums:
        num_cols = num_cols + 1
    
    g.es("\nimporting table: " + table_name + "\n\n(layout 1)\n")
                    
    rx = 0
    delim = ", "
    new_row = ""
    
    p.b = p.b + 'filepath: ' + filepath + '\n\n'
    p.b = p.b + str(col_names) + '\n'
    p.b = p.b + str(col_types) + '\n\n'
    p.b = p.b + 'layout: ' + layout + '\n\n'

    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()

    for row in cursor.execute("SELECT * FROM " + table_name):
    
        cx = 0 
        if row != "":
            cols = re.split(delim, str(row))

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
#@+node:tscv11.20180119175627.28: *3* import_table2
def import_table2(self, c, p, col_nums, col_names, col_types, blob_col):

    db_filename = c._leo4sqlite['db_filename']
    table_name = c._leo4sqlite['table_name']
    layout = c._leo4sqlite['layout']

    num_cols = 0
    for col in col_nums:
        num_cols = num_cols + 1
    
    idx = 0
    rx = 0
    
    p.b = p.b + "filepath: " + str(db_filename) + "\n\n"
    p.b = p.b + str(col_names) + "\n"
    p.b = p.b + str(col_types) + "\n\n"
    p.b = p.b + 'layout: ' + layout + '\n\n'
    
    g.es("\nimporting table: " + table_name + "\n\n(layout 2)\n")

    rows = []
    
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM " + table_name):    
        rows.append(row)
    
        idx = idx + 1  
        if idx == 1:
            p = p.insertAsNthChild(1)
            c.selectPosition(p)
        else:
            p = p.insertAfter()
            c.selectPosition(p)

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
    
    g.es("\ndone\n")
    c.redraw()        
    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
#@+node:tscv11.20180119175627.27: *3* import_table3
def import_table3(self, c, p, col_nums, col_names, col_types, blob_col):

    db_filename = c._leo4sqlite['db_filename']
    table_name = c._leo4sqlite['table_name']
    layout = c._leo4sqlite['layout']
    
    g.es("\nimporting table: " + table_name + "\n\n(layout 3)\n")

    conn = sqlite3.connect(db_filename)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("select * from " + table_name)
    row = cursor.fetchone()
    names = row.keys()

    rx = 0
    cx = 0
    num_cols = 0

    p.b = p.b + "filepath: " + str(db_filename) + "\n\n"
    p.b = p.b + str(col_names) + "\n"
    p.b = p.b + str(col_types) + "\n\n"    
    p.b = p.b + 'layout: ' + layout + '\n\n'

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
#@+node:tscv11.20180119175627.30: *3* import_table4
def import_table4(self, c, p, col_nums, col_names, col_types, blob_col):

    db_filename = c._leo4sqlite['db_filename']
    table_name = c._leo4sqlite['table_name']
    layout = c._leo4sqlite['layout']
    
    g.es("\nimporting table: " + table_name + "\n\n(layout 4)\n")

    num_cols = 0
    for col_num in col_nums:
        num_cols = num_cols + 1

    idx = 0

    p.b = p.b + "filepath: " + str(db_filename) + "\n\n"
    p.b = p.b + str(col_names) + "\n"
    p.b = p.b + str(col_types) + "\n\n"
    p.b = p.b + 'layout: ' + layout + '\n\n'
    
    for col_name in col_names:
        if idx == 0:
            p = p.insertAsLastChild()
        else:
            p = p.insertAfter()
            
        p.h = col_name
    
        i = 0
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
#@-others
#@+node:tscv11.20180119175627.31: ** exports
#@+others
#@+node:tscv11.20180119175627.32: *3* export_table1
def export_table1(self, c, p, col_nums, col_names, col_types, blob_col):
    
    def place_holder(line):
        return '({})'.format(', '.join('?' * len(line)))
    
    table_name = c._leo4sqlite['table_name']

    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))        
    c.selectPosition(tbl_node)
    c.redraw()
    p = c.p
    
    g.es("\nexporting table " + table_name + "\n\n(layout 1)\n")

    lines = re.split("\n", p.b)

    new_names = re.sub(r'[\"\'\[\]\s]', "", str(col_names))
    new_types = re.sub(r'[\"\'\[\]\s]', "", str(col_types))

    split_names = re.split(r',', str(new_names))
    split_types = re.split(r',', str(new_types))
    
    sql = "("
    for i in range(len(split_names)):
        sql = sql + split_names[i] + " " + split_types[i] + ", "
    sql = sql[:-2]
    sql = sql + (")")

    lines = lines[7:]
    
    db_filename = c._leo4sqlite['db_filename']
    
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
#@+node:tscv11.20180119175627.34: *3* export_table2
def export_table2(self, c, p, col_nums, col_names, col_types, blob_col):
    
    hlines = []
    table_name = c._leo4sqlite['table_name']
    db_filename = c._leo4sqlite['db_filename']
   
    def place_holder(line):
        return '({})'.format(', '.join('?' * len(line)))

    g.es("\nexporting table: " + table_name + "\n\n(layout 2)\n") 

    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
    c.redraw()
    p = c.p
    lines = re.split(r"\n", p.b)
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

    lines = lines[7:]
    
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
#@+node:tscv11.20180119175627.35: *3* export_table3
def export_table3(self, c, p, col_nums, col_names, col_types, blob_col):

    def place_holder(line):
        return '({})'.format(', '.join('?' * len(line)))

    table_name = c._leo4sqlite['table_name']
    db_filename = c._leo4sqlite['db_filename']

    g.es("\nexporting table: " + table_name + "\n\n(layout 3)\n") 
    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
    c.redraw()
    p = c.p
    lines = re.split(r'\n', str(p.b))
    names = lines[2]
    types = lines[3]

    new_names = re.sub(r'[\"\'\[\]\s]', "", str(names))
    new_types = re.sub(r'[\"\'\[\]\s]', "", str(types))
    split_names = re.split(r',', str(new_names))
    split_types = re.split(r',', str(new_types))

    row = []
    rows = []
    cols = []
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

    lines = lines[7:]

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

        rows.append(row)
        row = row[num_cols:]
        x += 1    
    
    row = rows[0][:num_cols]
    row = rows[0][num_cols:num_cols * num_rows]
    
    row = row[num_cols:]
            
    print("\ndone\n")
#@+node:tscv11.20180119175627.36: *3* export_table4
def export_table4(self, c, p, col_nums, col_names, col_types, blob_col):
    
    def place_holder(line):
        return '({})'.format(', '.join('?' * len(line)))

    col_hlines = []
    row_hlines = []
    
    db_filename = c._leo4sqlite['db_filename']
    table_name = c._leo4sqlite['table_name']
    
    g.es("\nexporting table: " + table_name + "\n\n(layout 4)\n") 
    headline = ("@tbl " + table_name)
    tbl_node = g.findNodeAnywhere(c, (headline))
    c.selectPosition(tbl_node)
    c.redraw()
    p = c.p
    
    lines = re.split(r'\n', str(p.b))
  
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
    
    lines = lines[7:]
    
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
#@-others
#@+node:tscv11.20180119175627.37: ** g.commands
#@+others
#@+node:tscv11.20180119175627.38: *3* @g.command('sqlite-import-table')
@g.command('sqlite-import-table')
def sqlite_import_table(event):
    
    c = event.get('c')
    
    action = "import table"
    c._leo4sqlite['action'] =  action
    
    InputDialogs(c)
#@+node:tscv11.20180119175627.39: *3* @g.command('sqlite-export-table')
@g.command('sqlite-export-table')
def sqlite_export_table(event):
    
    c = event.get('c')
    
    action = "export table"
    c._leo4sqlite['action'] = action
    
    InputDialogs(c)
#@+node:tscv11.20180119175627.40: *3* @g.command('sqlite-insert-blob')
@g.command('sqlite-insert-blob')
def sqlite_insert_blob(event):   
    
    c = event.get('c')
    
    action = "insert blob"
    c._leo4sqlite['action'] = action
    
    InputDialogs(c)
    
#@+node:tscv11.20180119175627.41: *3* @g.command('sqlite-extract-blob')
@g.command('sqlite-extract-blob')
def sqlite_extract_blob(event):    
    
    c = event.get('c')
    
    action = "extract blob"
    c._leo4sqlite['action'] = action
    
    InputDialogs(c)
    
#@+node:tscv11.20180119175627.42: *3* @g.command('sqlite-open-blob')
@g.command('sqlite-open-blob')
def sqlite_open_blob(event):
    
    c = event.get('c')
    
    action = "open blob"
    c._leo4sqlite['action'] = action
    
    InputDialogs(c)
    
#@+node:tscv11.20180119175627.43: *3* @g.command('sqlite-view-blob')
@g.command('sqlite-view-blob')
def sqlite_view_blob(event):
    
    c = event.get('c')
    
    action = "view blob"
    c._leo4sqlite['action'] = action
    
    InputDialogs(c)
    
#@+node:tscv11.20180119175627.44: *3* @g.command('sqlite-edit-blob')
@g.command('sqlite-edit-blob')
def sqlite_edit_blob(event):

    c = event.get('c')
    
    action = "edit blob"
    c._leo4sqlite['action'] = action
    
    InputDialogs(c)
    
#@+node:tsc.20180131045323.1: *3* @g.command('sqlite-clear-temp')
@g.command('sqlite-clear-temp')
def sqlite_clear_temp(event):
    
    c = event.get('c')

    p = g.findNodeAnywhere(c, 'temp')
    if p:
        c.selectPosition(p)
        p.deleteAllChildren()
        c.redraw()
    else:
        pass
#@+node:tscv11.20180119175627.46: *3* @g.command('sqlite-delete-data')
@g.command('sqlite-delete-data')
def sqlite_delete_data(event):
    
    c = event.get('c')
    
    p_lst = c.find_h('data')
    
    if p_lst[0]:
        c.selectPosition(p_lst[0])
        p_lst[0].doDelete()
        
    p = c.lastTopLevel().insertAfter()
    c.selectPosition(p)
    p.h = "data"
    c.redraw()
#@+node:tscv11.20180119175627.47: *3* @g.command('sqlite-purge-files')
@g.command('sqlite-purge-files')
def sqlite_purge_files(event):
    
    c = event.get('c')
    
    p = g.findNodeAnywhere(c, 'temp')
    c.selectPosition(p)
    p.deleteAllChildren()
    c.redraw()
    
    sqlite_temp_dir = c.config.getString("sqlite_temp_dir")
    sqlite_temp_dir = sqlite_temp_dir[1:-1]
    
    os.chdir(sqlite_temp_dir)
    files=glob.glob('*')
    if files:
        for filename in files:
            os.unlink(filename)
#@-others
#@-others
#@-leo
