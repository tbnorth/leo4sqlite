<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="tscv11.20180119175627.1"><vh>Sqlite3</vh>
<v t="tscv11.20180119175627.2"><vh>@file leo4sqlite.py</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="tscv11.20180119175627.1">@nocolor
@
**leo4sqlite.py plugin**

*This node belongs at the top level of 'leoPlugins.leo'*

|
         
**Notes**

 This script needs to be streamlined and polished, which I intend to
 do (in the end I'm a perfectionist). Any suggestions toward that
 end are welcome!
 
**Issues**

 1. The 'switchboard code' is convoluted - it jumps around much more than necessary, I\'m
 sure of that... and now I'll eat my words. After looking at it again I don't think it's too bad,
 other than mixing the creation of the @db3 and @tbl nodes with the code for routing table
 imports/exports.

 2. If the user cancels the file selection dialog after using the command: 'sqlite-import-table'
 they are still asked to enter a table name before execution stops. This is an unwanted artifact that I intend to remove.

**Ideas**
    
 | 1. Recent files for blob command dialogs?

 | 2. Edit text in individual blob row columns without having to
    start the row over from scratch.
 
 | 3. Should settings be kept in myLeoSettings.leo instead of the
    current outline? It seems like a better idea to me - see the
    third child of this node for an example of leo4sqlite settings.

 | 4. Add a setting - overwrite existing tables? It could save a
    *little* time, but it would be easier  to make a mistake and
    lose valuable data.

 | 5. Dialog icons
 |

**The commands currently added by the plugin are:**

 | sqlite-import-table
 | sqlite-export-table
 | sqlite-open-blob
 | sqlite-view-blob
 | sqlite-insert-blob
 | sqlite-extract-blob
 | sqlite-reset-temp
 | sqlite-clear-data
 | sqlite-purge-files
 |
 
I want to make this the best plugin I can rather than rushing to finish it. Leo deserves no less! Please provide any feedback you can, and don't hesitate to suggest improvements! :-)</t>
</tnodes>
</leo_file>
