bl_info = {
    "name": "Submit Blender To Deadline",
    "description": "Submit a Blender job to Deadline",
    "author": "Thinkbox Software Inc",
    "version": (1,0),
    "blender": (2, 5, 0),
    "category": "Render",
    "location": "Render > Submit To Deadline",
    }

import bpy, os, sys, subprocess

def GetRepositoryRoot():
    # On OSX, we look for the DEADLINE_PATH file. On other platforms, we use the environment variable.
    if os.path.exists( "/Users/Shared/Thinkbox/DEADLINE_PATH" ):
        with open( "/Users/Shared/Thinkbox/DEADLINE_PATH" ) as f: deadlineBin = f.read().strip()
        deadlineCommand = "%s/deadlinecommand" % deadlineBin
    else:
        try:
            deadlineBin = os.environ['DEADLINE_PATH']
        except KeyError:
            return ""
    
        if os.name == 'nt':
            deadlineCommand = "%s\\deadlinecommand.exe" % deadlineBin
        else:
            deadlineCommand = "%s/deadlinecommand" % deadlineBin
    
    startupinfo = None
    #if os.name == 'nt':
    #	startupinfo = subprocess.STARTUPINFO()
    #	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    proc = subprocess.Popen([deadlineCommand, "-root"], cwd=deadlineBin, stdout=subprocess.PIPE, startupinfo=startupinfo)
    
    output = proc.stdout.read()
    print( output )
    root = output.decode("utf_8")
    print( root )
    root = root.replace("\r","").replace("\n","").replace("\\","/")
    print( root )
    
    return root

class SubmitToDeadline_Operator (bpy.types.Operator):
    bl_idname = "ops.submit_blender_to_deadline"
    bl_label = "Submit Blender To Deadline"
    
    def execute( self, context ):
        # Get the repository root
        root = GetRepositoryRoot()
        if root != "":
            path = root + "/submission/Blender/Main"
            
            # Add the path to the system path
            if path not in sys.path :
                print( "Appending \"%s\" to system path to import SubmitBlenderToDeadline module" % path )
                sys.path.append( path )
            
            # Import the script and call the main() function
            import SubmitBlenderToDeadline
            SubmitBlenderToDeadline.main( root )
        else:
            print( "The SubmitBlenderToDeadline.py script could not be found in the Deadline Repository. Please make sure that the Deadline Client has been installed on this machine, that the Deadline Client bin folder is set in the DEADLINE_PATH environment variable, and that the Deadline Client has been configured to point to a valid Repository." )
        
        return {'FINISHED'}
    
def deadline_submit_button( self, context ):
    self.layout.separator()
    self.layout.operator( SubmitToDeadline_Operator.bl_idname, text="Submit To Deadline" )

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_render.append( deadline_submit_button )

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_render.remove( deadline_submit_button )

if __name__ == "__main__":
    register()
