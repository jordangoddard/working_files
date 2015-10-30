
import bpy
import breakout_layout_tool
from bpy.app.handlers import persistent
from imp import reload
reload(breakout_layout_tool)

import time
import re


cl = breakout_layout_tool.CheckLayout()

if __name__ == "__main__":
    cl.check_all()
