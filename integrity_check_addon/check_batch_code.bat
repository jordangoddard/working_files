path = %path%;C:\pipeline\python\34_64\;C:\pipeline\python\34_64\scripts\;C:\pipeline\blender\tangent-builds\blender-2.75a-windows64\;c:\pipeline\client\release\v1.00\;C:\pipeline\non_client\integrity_check
Set SNAPSHOT=http://snapshot/api
Set PYTHONPATH=C:\pipeline\python\34_64\;C:\pipeline\python\34_64\DLLs;C:\pipeline\python\34_64\Lib;C:\pipeline\python\34_64\Scripts\;C:\pipeline\client\release\v1.00\;C:\pipeline\non_client\integrity_check
Set PYTHONHOME=C:\pipeline\python\34_64\
Set BLENDER_SYSTEM_PYTHON=C:\pipeline\python\34_64\
Set BLENDER_USER_SCRIPTS=C:\pipeline\addons\scripts\

C:\pipeline\blender\tangent-builds\blender-2.75a-windows64\blender.exe --background --python c:\pipeline\non_client\integrity_check\blender_checklayout_run_script.py