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
<v t="tscv11.20180126132059.1"><vh>@data free-layout-layout</vh></v>
</v>
<v t="tscv11.20180127104929.1"><vh>RenderPaneHideEvent</vh></v>
<v t="tscv11.20180119175627.1" a="E"><vh>Sqlite3</vh>
<v t="tscv11.20180119175627.2" a="E" descendentVnodeUnknownAttributes="7d710058010000003071017d7102580b0000005f5f626f6f6b6d61726b7371037d7104580700000069735f6475706571054930300a7373732e"
expanded="tscv11.20180119175627.10,"><vh>@file ~/Desktop/leo-editor/leo/plugins/leo4sqlite.py</vh></v>
</v>
</vnodes>
<tnodes>
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
<t tx="tscv11.20180126132059.1">{
    "content": [
        "_leo_pane:bodyFrame",
        {
            "content": [
                "_leo_pane:outlineFrame",
                "_leo_pane:logFrame"
            ],
            "sizes": [
                302,
                299
            ],
            "orientation": 2
        }
    ],
    "sizes": [
        786,
        569
    ],
    "orientation": 1
}</t>
<t tx="tscv11.20180127104929.1">@

Terry:
    
The "proper" way to modify them is to create a descendant class, as you
did with InputDialogs, and re-implement the function in the descendant
class, usually calling the original classes function as well:

class MyHideAwareWidget(QWidget):

    def hideEvent(self, event):
        QWidget.hideEvent(self, event) # the rare case when you do
                                       # include self
        &lt;do your hide related stuff&gt;

But that assumes you're instantiating the descendant class yourself.
That's not the case with the viewrendered pane, so it's probably
easiest to "monkey patch" the methods on the existing widget.

so the pattern is something like

def myHideEvent(self, event):
    &lt;do your hide related stuff&gt;
    self.realHideEvent(self, event)

def get_vr(self):
    vr = c.frame.top.findChild(QtWidgets.QWidget, 'viewrendered_pane')
    if not vr:
        return None  # not opened yet
    if vr.hideEvent != InputDialogs.myHideEvent:
        self.realHideEvent = vr.hideEvent
        vr.hideEvent = InputDialogs.myHideEvent
    return vr

then use self.get_vr() to get vr, instead of whatever you're doing now
to get it.
@c
</t>
</tnodes>
</leo_file>
