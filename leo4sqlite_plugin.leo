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
<v t="tscv11.20180125192120.1"><vh>@settings</vh>
<v t="tsc.20180129232027.1"><vh>@data free-layout-layout</vh></v>
</v>
<v t="tscv11.20180119175627.1" a="E"><vh>Sqlite3</vh>
<v t="tscv11.20180119175627.2" a="E" descendentVnodeUnknownAttributes="7d710058010000003071017d710228580b0000005f5f626f6f6b6d61726b7371037d7104580700000069735f6475706571054930300a73580500000069636f6e7371065d71077d710828580400000066696c65710958460000002f686f6d652f7473632f4465736b746f702f6c656f2d656469746f722d6d61737465722f6c656f2f49636f6e732f66696c655f69636f6e732f66696c655f66696c652e706e67710a5807000000786f6666736574710b4b02580700000072656c50617468710c581800000066696c655f69636f6e732f66696c655f66696c652e706e67710d58050000007768657265710e580e0000006265666f7265486561646c696e65710f58040000007479706571106809580a00000076697375616c49636f6e711158010000003171125807000000796f666673657471134b0058020000006f6e71145805000000766e6f6465711558040000007870616471164b01756175732e"
expanded="tscv11.20180119175627.10,tscv11.20180119175627.26,tscv11.20180119175627.37,"><vh>@file /home/tsc/Desktop/leo-editor-master/leo/plugins/leo4sqlite.py</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="tsc.20180129232027.1">{
    "content": [
        "_leo_pane:bodyFrame",
        {
            "content": [
                "_leo_pane:outlineFrame",
                "_leo_pane:logFrame"
            ],
            "orientation": 2,
            "sizes": [
                276,
                274
            ]
        }
    ],
    "orientation": 1,
    "sizes": [
        787,
        569
    ]
}</t>
<t tx="tscv11.20180119175627.1">@nocolor

**leo4sqlite.py plugin**

*This node belongs at the top level of 'leoPlugins.leo'*

|
         
**Notes**

 | 1. This script needs to be streamlined and polished, which I intend to do (in the end I'm a perfectionist). Any suggestions toward that end are welcome!
 
**Issues**

 | 1. If the user cancels the file selection dialog after using the command: 'sqlite-import-table' they are still asked to enter a table name before script execution stops. This is an unwanted artifact that I intend to remove.

 | 2. Error handling
 
 | 3. Data types - column affinity, manifest type, storage type

**Ideas**
    
 | 1. Recent files for blob command dialogs?

 | 2. Edit text in individual blob row columns without having to start the row over from scratch.
 
 | 3. Should settings be kept in myLeoSettings.leo instead of the current outline? It seems like a better idea to me - see the third child of this node for an example of leo4sqlite settings.

 | 4. Add a setting - overwrite existing tables? It could save a *little* time, but it would be easier  to make a mistake and lose valuable data.

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
<t tx="tscv11.20180125192120.1"></t>
</tnodes>
</leo_file>
