#  #  #  #  #  #  #  #  #  #  #
#         Master Tool         #
#     By: Jordan Goddard      #
#  #  #  #  #  #  #  #  #  #  #



import os
import sys
import subprocess
import re

response = None
file_path = None

def create_file():
    file = open("C:\\Temp\\breakout_tool_data\\breakout_log.txt", "w")
    file.write("file=C:\\Temp\n000.0000")
    file.close()

def check_file():
    try:
        file = open("C:\\Temp\\breakout_tool_data\\breakout_log.txt", "r")
    except:
        create_file()
        print("\nThe file is empty, please enter data into the file\n")

def read_file():
    file = open("C:\\Temp\\breakout_tool_data\\breakout_log.txt", "r")
    print("\n-------------------------------------------------------------------------\n")
    for line in file:
        print(line)
    print("\n-------------------------------------------------------------------------\n")

def question_one():
    print("\nThe following shots have been set for breakout: ")
    read_file()
    print("\nIs this correct? (y/n)")
    response = input()
    question_one_answer(response)

def question_one_answer(response):
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
    print("\n-------------------------------------------------------------------------\n")
    directory_creation()
    check_file()
    question_one()

def directory_creation():
    new_path = ["C:\\Temp\\breakout_tool_data", "C:\\Temp\\breakout_tool_data\\blender_files", "C:\\Temp\\breakout_tool_data\\error_logs"]
    if not os.path.exists(new_path[0]):
        os.makedirs(new_path[0])
    if not os.path.exists(new_path[1]):
        os.makedirs(new_path[1])
    if not os.path.exists(new_path[2]):
        os.makedirs(new_path[2])


def run_scripts():
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