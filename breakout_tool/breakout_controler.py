# ##### BEGIN GPL LICENSE BLOCK #####
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# ##### END GPL LICENSE BLOCK #####

# ##### BEGIN SCRIPT COMMENTS #####
#  Main Tool: "Breakout Tool"
#  Parent: "Breakout Launcher"
#  Name: "Breakout Controler",
#  Author: "Jordan Goddard",
#  Company: "Tangent Animation"
#  Blender: (2, 74, 0),
#  Description: "Controls what the breakout tool will run on, and how many times it will run"
#  <pep8 compliant>
# ##### END SCRIPT COMMENTS #####

"""
Import the necesary libraries for the application to call as well as declare any global variables
"""
import os
import sys
import subprocess
import re
response = None
file_path = None

def create_file():
    """
    Creates the breakout list that the breakout tool will gather information from
    """
    file = open("C:\\Temp\\breakout_tool_data\\breakout_log.txt", "w")
    file.write("file=C:\\Temp\n000.0000")
    file.close()

def check_file():
    """
    Checks if there is a file for breakout to run and read from
    """
    try:
        file = open("C:\\Temp\\breakout_tool_data\\breakout_log.txt", "r")
    except:
        create_file()
        print("\nThe file is empty, please enter data into the file\n")

def read_file():
    """
    Reads the file that has the data of what to breakout and from where, then prints it for the user
    """
    file = open("C:\\Temp\\breakout_tool_data\\breakout_log.txt", "r")
    print("\n-------------------------------------------------------------------------\n")
    for line in file:
        print(line)
    print("\n-------------------------------------------------------------------------\n")

def question_one():
    """
    Asks the user if they want to breakout the files that have been read from the breakout log file
    """
    print("\nThe following shots have been set for breakout: ")
    read_file()
    print("\nWould you like to break these out? (y/n)")
    response = input()
    question_one_answer(response)

def question_one_answer(response):
    """
    Handles the response from the user for wether or not to breakout the files listed
    """
    if response == 'y':
        print("\nBreakout is beginning\n")
        run_scripts()
        print("\n\n\nrun\n\n\n")
    elif response == 'n':
        print("Please update the file with correct data")
        question_two()
    else:
        print("\nInvalid Entry!\nPlease try again!")
        question_one()

def execute():
    """
    Runs functions in order of execution
    """
    print("\n-------------------------------------------------------------------------\n")
    directory_creation()
    check_file()
    question_one()

def directory_creation():
    """
    Checks if the proper directory of files already exists, and if it doesnt or it is partial, it creates it.
    """
    new_path = ["C:\\Temp\\breakout_tool_data", "C:\\Temp\\breakout_tool_data\\blender_files", "C:\\Temp\\breakout_tool_data\\error_logs"]
    if not os.path.exists(new_path[0]):
        os.makedirs(new_path[0])
    if not os.path.exists(new_path[1]):
        os.makedirs(new_path[1])
    if not os.path.exists(new_path[2]):
        os.makedirs(new_path[2])

def run_scripts():
    """
    Runs breakout tool based on the number of files to be broken out
    """
    try:
        file = open("C:\\Temp\\breakout_tool_data\\breakout_log.txt", "r")
    except:
        print("File Error!")
        file = open("C:\\Temp\\breakout_tool_data\\breakout_log.txt", "w")
        file.close()
    else:
        for line in file.readlines():
            if line.startswith('file='):
                match=re.match("file=(\S+)", line)
                file_path = match.group(1)
            else:
                file_new = open("C:\\Temp\\pass_temp.txt", "w")
                match = re.match(r'(\d+\.\d+)',line)
                scene_name = match.group(1)
                file_new.write("%s\n%s" %(scene_name,file_path))
                file_new.close()
                subprocess.call("C:\\pipeline\\non_client\\breakout\\breakout_batch_code.bat")
    finally:
        print("\n\nComplete\n\n")
        file.close()

execute()