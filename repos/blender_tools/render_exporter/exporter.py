import bpy
class RestoreLibraryData(object):
    '''
    Remap libraries to new paths, move libraries to those paths, and save all to new, mobile, directory.
    '''
    def __init__(self):
        '''
        Initialize definition
        '''
        self.source_list = []
        self.target_list = []
        self.base_path = 'C:\\Temp\\RenderData'
        self.root_path = '%s\\Projects\\0043_Ozzy\\'%self.base_path

    def execute(self, blendfile_path):
        '''
        Manage what function is run, and when.
        '''
        self.blend_file = blendfile_path
        self.clear_list()
        self.open_file()
        self.clear_list()
        self.remap_libraries()
        self.clear_list()
        self.save_file()
        self.clear_list()

    def open_file(self):
        bpy.ops.wm.open_mainfile(filepath=self.blend_file)

    def clear_list(self):
        '''
        Ensure that the arrays are empty and have no active slots.
        '''
        self.source_list = []
        self.target_list = []
        self.source_list.clear()
        self.target_list.clear()
        self.source_list = []
        self.target_list = []

    def remap_libraries(self):
        '''
        Gather library data, convert it to the new directory format, create new directories, duplicate files and relocate to new path, and remap current libraries.
        '''
        import os
        import shutil
        if not os.path.exists('%sShots'%self.root_path):
            os.makedirs('%sShots'%self.root_path)
        if not os.path.exists('%sAssets'%self.root_path):
            os.makedirs('%sAssets'%self.root_path)
        try:
            for lib in bpy.data.libraries:
                emp = lib.filepath
                #print("%s"%lib.filepath)
        except:
            pass
        else:
            for lib in bpy.data.libraries:
                source_path = "%s"%(lib.filepath)
                target_path = "%s"%(self.base_path)
                final_path = "%s%s"%(target_path,source_path[2:])
                self.source_list.append(source_path)
                self.target_list.append(final_path)
                lib.filepath = final_path
                dir = final_path.rpartition('\\') #where dir[0] is the directory
                if not os.path.exists("%s"%dir[0]):
                    os.makedirs("%s"%dir[0])
                print("Moving %s to %s"%(source_path,final_path))
                shutil.copyfile(source_path,final_path)

# Add image maps
# Add check for messed up assets ...... separate tool?

    def save_file(self):
        '''
        Create main file directory, and save main file.
        '''
        import os
        source_file_path = bpy.data.filepath
        taget_file_path = "%s"%(self.base_path)
        final_file_path = "%s%s"%(taget_file_path,source_file_path[2:])
        file_dir = final_file_path.rpartition('\\')
        if not os.path.exists("%s"%file_dir[0]):
            os.makedirs("%s"%file_dir[0])
        bpy.ops.wm.save_as_mainfile(filepath=final_file_path)

files = ['T:\\Projects\\0043_Ozzy\\Shots\\140\\0010\\layout\\publish\\test.blend','T:\\Projects\\0043_Ozzy\\Shots\\170\\0010\\layout\\publish\\SM_170.0010_publish.v0004.blend','T:\\Projects\\0043_Ozzy\\Shots\\170\\0020\\layout\\publish\\170.0020_publish.v0004.blend','T:\\Projects\\0043_Ozzy\\Shots\\170\\0030\\layout\\publish\\170.0030_publish.v0004.blend']
c = RestoreLibraryData()

for fp in files:
    c.execute(fp)