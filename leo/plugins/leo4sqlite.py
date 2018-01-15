#@+leo-ver=5-thin
#@+node:tscv11.20180114091132.2: * @file leo4sqlite.py
#@+<< docstring >>
#@+node:tscv11.20180114091132.3: ** << docstring >>
'''
leo4sqlite.py
Import/export sqlite3 tables and insert, extract, view or open 'blobs' using Leo.
'''
#@-<< docstring >>
### From leoSettings.leo
# Created 2017/05/30
#@@language python
#@@tabwidth -4
__version__ = '0.5'
#@+<< version history >>
#@+node:tscv11.20180114091132.4: ** << version history >>
#@+at
# leo4sqlite.py
# 
# v0.5 - converting to plugin
#@-<< version history >>
#@+<< imports >>
#@+node:tscv11.20180114091132.5: ** << imports >>
import leo.core.leoGlobals as g
from leo.core.leoQt import QtWidgets
import leo.commands.controlCommands as controlCommands

import subprocess
import sys, os, re
import sqlite3

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QIcon
#@-<< imports >>
#@+others
#@+node:tscv11.20180114091132.6: ** init
def init ():
        
    ok = g.app.gui.guiName() in ('qt','qttabs')
    if ok:
        if 1: # Create the commander class *before* the frame is created.
            g.registerHandler('before-create-leo-frame',onCreate)
        else: # Create the commander class *after* the frame is created.
            g.registerHandler('after-create-leo-frame',onCreate)
        g.plugin_signon(__name__)   
    return ok
#@+node:tscv11.20180114091132.7: ** onCreate
def onCreate (tag, keys):
    
    c = keys.get('c')
    if c:
        theLeo4SQLiteController = Leo4SQLiteController
#@+node:tscv11.20180114091132.8: ** class Leo4SQLiteController
class Leo4SQLiteController:
    
    #@+others
    #@+node:tscv11.20180114124455.1: *3* init
    def init (self, c):
            
        ok = g.app.gui.guiName() in ('qt','qttabs')
        if ok:
            if 1: # Create the commander class *before* the frame is created.
                g.registerHandler('before-create-leo-frame',onCreate)
            else: # Create the commander class *after* the frame is created.
                g.registerHandler('after-create-leo-frame',onCreate)
            g.plugin_signon(__name__)   
        return ok

    #@+node:tscv11.20180114150010.1: *3* sqlite_import_table
    @g.command('sqlite-import-table')
    def sqlite_import_table(event):
        """and the struggle begins"""
        c = event.get('c')

        g.es('hello')
    #@-others
#@+node:tscv11.20180114161701.1: ** class InputDialogs
class InputDialogs(QWidget):

    #@+others
    #@+node:tscv11.20180114161919.1: *3* __init__
    def __init__(self):
        super().__init__()
        self.title = 'leo4sqlite'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI(c)
    #@+node:tscv11.20180114162026.1: *3* initUI
    def initUI(self, c):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        #self.pick_action()
     
        self.show() 


    #@+node:tscv11.20180114162217.1: *3* get_settings
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
        
    #@+node:tscv11.20180114162315.1: *3* get_ext_db
    def get_ext_db(self):

        def get_filename(path):
            filename = os.path.basename(path.rstrip('/'))
            fn = filename
                
        db_fname = g.app.gui.runOpenFileDialog(c, title="Select SQLite Database", \
        filetypes=[("SQLite Database File", "*.db3"), ("SQLite3 Database File", "*.db")], \
        defaultextension=".db3", multiple=False)
            
        no_path = get_filename(db_fname)
        c.__['db_filename'] = db_fname
    #@+node:tscv11.20180114162542.1: *3* get_int_dbs
    def get_int_dbs(self):
        
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
    #@-others
#@-others
#@-leo
