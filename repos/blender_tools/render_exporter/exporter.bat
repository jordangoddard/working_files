rem ##### BEGIN SCRIPT COMMENTS #####
rem  Main Tool: "Breakout Tool"
rem  Parent: "Breakout Controler"
rem  Name: "Breakout Batch Code",
rem  Author: "Jordan Goddard",
rem  Company: "Tangent Animation"
rem  Blender: (2, 74, 0),
rem  Description: "Handels main breakout script and file save"
rem ##### END SCRIPT COMMENTS #####

path = %path%;C:\pipeline\python\34_64\;C:\pipeline\python\34_64\scripts\;C:\pipeline\blender\tangent-builds\blender-2.75a-windows64\;C:\pipeline\non_client\render_exporter\
Set SNAPSHOT=http://snapshot/api
Set PYTHONPATH=C:\pipeline\python\34_64\;C:\pipeline\python\34_64\DLLs;C:\pipeline\python\34_64\Lib;C:\pipeline\python\34_64\Scripts\;C:\pipeline\non_client\render_exporter\
Set PYTHONHOME=C:\pipeline\python\34_64\
Set BLENDER_SYSTEM_PYTHON=C:\pipeline\python\34_64\
Set BLENDER_USER_SCRIPTS=C:\pipeline\addons\scripts\
pause
C:\pipeline\blender\tangent-builds\blender-2.75a-windows64\blender.exe --background --python c:\pipeline\non_client\render_exporter\exporter.py
pause
pause
pause
pause
pause
