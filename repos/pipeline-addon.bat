# Pipeline Directory Copy/Merge
# version 2.0
#
# July 30, 2015
#
# Changed Robocopy switches
#	Removed /copyall which was setting permissions from samba/unix from share (breaks windows local)
#	Need to move log directory to C:\temp to make sure regular users have write permission to log, root of C no permission
# Added syntax to create directory c:\pipeline and validate its there
# Added python directory and rv directory
# 
#
#########################
@echo off
@break off
@title Update Pipeline Directory with new versions
@cls
if not exist "C:\temp\" (
  mkdir "C:\temp\"
  if "!errorlevel!" EQU "0" (
    echo Folder created successfully
  ) else (
    echo Error while creating folder
  )
) else (
  echo Folder already exists
)
if not exist "C:\pipeline\" (
  mkdir "C:\pipeline\"
  if "!errorlevel!" EQU "0" (
    echo Folder created successfully
  ) else (
    echo Error while creating folder
  )
) else (
  echo Folder already exists
)
echo "Deleting Local Pipeline Scripts-Addons Contents"
Del c:\pipeline\addons\scripts\* /F /S /Q > C:\temp\delete-addons2.txt
Del c:\pipeline\non_client\* /F /S /Q > C:\temp\delete-addons3.txt
Set sourcedir=%CD%
echo Using the current directory -> %sourcedir%
robocopy "%SOURCEDIR%\blender_addons\external\2.7.x" "c:\pipeline\addons\scripts\addons" /S /E /R:4 /W:15 /LOG:C:\temp\addon-pipeline.txt /TEE
robocopy "%SOURCEDIR%\blender_addons\internal\2.7.x" "c:\pipeline\addons\scripts\addons" /S /E /R:4 /W:15 /LOG:C:\temp\addon-pipeline1.txt /TEE
robocopy "%SOURCEDIR%\blender_addons\scripts\2.7.x" "c:\pipeline\addons\scripts" /S /E /R:4 /W:15 /LOG:C:\temp\addon-pipeline2.txt /TEE
robocopy "%SOURCEDIR%\snapshot_client\scripts\addons" "c:\pipeline\addons\scripts\addons" /S /E /R:4 /W:15 /LOG:C:\temp\addon-pipeline3.txt /TEE
robocopy "%SOURCEDIR%\snapshot_client\config" "C:\pipeline\client\release\v1.00\config" /S /E /R:4 /W:15 /LOG:C:\temp\addon-pipeline4.txt /TEE
robocopy "%SOURCEDIR%\blender_tools" "C:\pipeline\non_client" /S /E /R:4 /W:15 /LOG:C:\temp\addon-pipeline5.txt /TEE



