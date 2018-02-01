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
<v t="tsc.20180201085229.1"><vh>leo4sqlite template</vh>
<v t="tsc.20180201085229.2"><vh>@settings</vh>
<v t="tsc.20180201085229.9"><vh>@string sqlite_temp_dir = "~/leo4sqlite-temp"</vh></v>
<v t="tsc.20180201085229.10"><vh>@string sqlite_output_dir = "~/leo4sqlite-output"</vh></v>
<v t="tsc.20180201085229.8"><vh>@bool del_blobs_on_exit = 1: yes | 2: no</vh></v>
<v t="tsc.20180201085229.7"><vh>@data external tools</vh></v>
<v t="tsc.20180201085229.3"><vh>@commands</vh>
<v t="tsc.20180201085229.4"><vh>@command sqlite-clear-temp @key Alt-Shift-Ctrl-t</vh></v>
<v t="tsc.20180201085229.5"><vh>@command sqlite-delete-data @key Alt-Shift-Ctrl-d</vh></v>
<v t="tsc.20180201085229.6"><vh>@command sqlite-purge-files @key Alt-Shift-Ctrl-p</vh></v>
</v>
</v>
<v t="tsc.20180201085229.12"><vh>temp</vh></v>
<v t="tsc.20180201085229.11"><vh>data</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="tsc.20180201085229.1">This subtree will get you started quickly - it's a leo4sqlite-specific "new outline" template
with all of the nodes you'll need, ready to customize.

I do recommend, however, that you don't alter the @settings--&gt;@commands nodes
unless you know what you're doing :-)</t>
<t tx="tsc.20180201085229.10">Enter the path to your leo4sqlite-output directory in the headline of this node.</t>
<t tx="tsc.20180201085229.11">All table imports appear as children of this node,
and all table exports come from children of this node.</t>
<t tx="tsc.20180201085229.12">Temporary nodes appear here when viewing a blob, 
(or longer if desired).</t>
<t tx="tsc.20180201085229.2">These settings need to be customized before using the leo4sqlite.</t>
<t tx="tsc.20180201085229.3">@others

Cleanup commands</t>
<t tx="tsc.20180201085229.4">@language python

c.executeMinibufferCommand('sqlite-clear-temp')
</t>
<t tx="tsc.20180201085229.5">@language python

c.executeMinibufferCommand('sqlite-delete-data')
</t>
<t tx="tsc.20180201085229.6">@language python

c.executeMinibufferCommand('sqlite-purge-files')
</t>
<t tx="tsc.20180201085229.7">Enter one full path (including executable) per line.
Leave one blank line at the end of this body text.

Examples for linux:

/usr/bin/gimp
/usr/bin/xviewer
</t>
<t tx="tsc.20180201085229.8">The headline explains this one.</t>
<t tx="tsc.20180201085229.9">Enter the path to your leo4sqlite-temp directory in the headline of this node.</t>
</tnodes>
</leo_file>
