path = %path%;C:\pipeline\python\34_64\;C:\pipeline\python\34_64\scripts\;C:\pipeline\blender\tangent-builds\blender-2.75a-windows64\;c:\pipeline\client\release\v1.00\;C:\pipeline\non_client\breakout
Set SNAPSHOT=http://snapshot/api
Set PYTHONPATH=C:\pipeline\python\34_64\;C:\pipeline\python\34_64\DLLs;C:\pipeline\python\34_64\Lib;C:\pipeline\python\34_64\Scripts\;C:\pipeline\client\release\v1.00\;C:\pipeline\non_client\breakout
Set PYTHONHOME=C:\pipeline\python\34_64\
Set BLENDER_SYSTEM_PYTHON=C:\pipeline\python\34_64\
Set BLENDER_USER_SCRIPTS=C:\pipeline\addons\scripts\
python C:\pipeline\non_client\breakout\check_controler.py
python C:\pipeline\non_client\breakout\breakout_controler.py
@echo off
echo .
echo .
echo .
echo .
echo .Program Complete
echo .
echo .
echo .
pause
