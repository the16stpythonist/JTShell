# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 09:55:16 2015
@author: Jonas
###
A package combining the os-specific packages and using the variuos functions and
classes depending on operating system the program is run on
"""
# IMPORTS
import sys
import os
import inspect
PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import JTLib.JTOS.JTLinux as jtlinux
import JTLib.JTOS.JTWindows as jtwindows
import JTLib.JTUtility.JTString as jtstr
import platform
import io

# FUNCTIONS
def get_os():
    """
    returns string name of the operating system of the system the script is 
    running on while during runtime, so speficicly at the point the function is called
    ###
    RETURNS (string)
    """
    return platform.system()
    

def createfile(filepath):
    """
    creates a file independant from the used operating system
    ###
    filepath - (string) the string of the file to create
    ###
    RETURNS (void)
    """
    operating_system = platform.system()
    if operating_system == "Linux":
        jtlinux.createfile(filepath)
    elif operating_system == "Windows":
        jtwindows.createfile(filepath)
        
def dir_files(directory_path):
    """
    returns a list of the names of the files within the directory specified by
    the given path. In case there are no files or the given path doesnt exist
    an empty list will be returned.
    ###
    directory_path - (string) the absolute path of the directory to search in
    ###
    RETURNS (list/string)
    """
    # checking wether the path exists and specifies a directory
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # only checking in the very next layer of files
        temp_files = []
        for root, dirs, files in os.walk(directory_path):
            temp_files = files
            break
        if not(temp_files == False):
            return temp_files
        else:
            return []
    else: 
        return []
        
def dir_subdirs(directory_path):
    """
    returns a list of the names of the directories within the directory specified by
    the given path. In case there are no files or the given path doesnt exist
    an empty list will be returned.
    ###
    directory_path - (string) the absolute path of the directory to search in
    ###
    RETURNS (list/string)
    """
    # checking wether the path exists and specifies a directory
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # only checking in the very next layer of files
        temp_dirs = []
        for root, dirs, files in os.walk(directory_path):
            temp_dirs = dirs
            break
        if not(temp_dirs == False):
            return temp_dirs
        else:
            return []
    else: 
        return []        

"""
class defining a directory in the filepath system, capable of creating a path
hierarchy in ascii letters aswell as in latex format
###
directory_path - (string) the path of the directory to be specified
"""
class Directory():
    """
    path - (string) the absolute path of the directory to be specified
    name - (string) the name of the directory
    subdirs - (list/Directory) a list with subdirectories in the main directory
    files - (list/string) a list with the names of all files within the directory
    _subdirs - (dict/string-Directory) the names of the subdirectories and their
                                       corresponding 'Directory' objects    
    """
    def __init__(self, directory_path):
        # setting up the class variables
        self.path = directory_path
        self.name = os.path.basename(self.path)    
        self._subdirs = {}
        self.subdirs = []
        self.files = []
        # creating the main lists
        self.files = dir_files(self.path)
        temp_dirs = dir_subdirs(self.path)
        for subdir in temp_dirs:
            self._subdirs[subdir] = Directory(self.path+"\\"+subdir)
        self.subdirs = self._subdirs.values()
            
    def get_hierarchy_ascii(self):
        """
        creates a hierarchy of files and subdirectories within the main directory
        ###
        RETURNS (string)
        """
        indent = "    "
        main_string = ""
        main_string += self.name+"\n"
        for subdir in self.subdirs:
            # going for he first layer of subdirectories
            main_string += "-> "+subdir.get_name()+"\n"
            if not(subdir.subdirs == []):
                for subdir2 in subdir.subdirs:
                    main_string += indent+"-> "+subdir2.get_name()+"\n"
                    # going for the second layer
                    if not(subdir2.subdirs == []):
                        for subdir3 in subdir2.subdirs:
                            main_string += indent+indent+"-> "+subdir3.get_name()+"\n"
                            # going for the third layer
                            if not(subdir3.subdirs == []):
                                for subdir4 in subdir3.subdirs:
                                    main_string += indent+indent+indent+"-> "+subdir4.get_name()+"\n"
                            for file4 in subdir3.files:
                                main_string += indent+indent+indent+"-- "+file4+"\n"
                            main_string += "\n"
                    for file3 in subdir2.files:
                        main_string += indent+indent+"-- "+file3+"\n"
                    main_string += "\n"
            for file2 in subdir.files:
                main_string += indent+"-- "+file2+"\n"
            main_string += "\n"
        for file in self.files:
            main_string += "-- "+file+"\n"
        main_string += "\n"
        # returning the whole string
        return main_string
        
    def get_hierarchy_latex(self):
        """
        creates a hierarchy of files and subdirectories within the main directory
        and writes it into a latex compatible string
        ###
        RETURNS (string)
        """
        indent = "    "
        main_string = ""
        main_string += "\\setstretch {0.74}%\n"
        main_string += self.name+"\n"
        main_string += "\\begin{itemize}\n"
        for subdir in self.subdirs:
            # going for he first layer of subdirectories
            main_string += "\item[$\\blacktriangleright$] "+jtstr.latex_compatible(subdir.get_name())+"\n"
            main_string += indent+"\\begin{itemize}\n"
            if not(subdir.subdirs == []):
                for subdir2 in subdir.subdirs:
                    main_string += indent+"\item[$\\blacktriangleright$] "+jtstr.latex_compatible(subdir2.get_name())+"\n"
                    # going for the second layer
                    main_string += indent+indent+"\\begin{itemize}\n"
                    if not(subdir2.subdirs == []):
                        for subdir3 in subdir2.subdirs:
                            main_string += indent+indent+"\item[$\\blacktriangleright$] "+jtstr.latex_compatible(subdir3.get_name())+"\n"
                            # going for the third layer
                            main_string += indent+indent+indent+"\\begin{itemize}\n"
                            if not(subdir3.subdirs == []):
                                for subdir4 in subdir3.subdirs:
                                    main_string += indent+indent+indent+"\item[$\\blacktriangleright$] "+jtstr.latex_compatible(subdir4.get_name())+"\n"
                            for file4 in subdir3.files:
                                main_string += indent+indent+indent+"\item[$\\vartriangleright$] "+jtstr.latex_compatible(file4)+"\n"
                            main_string += indent+indent+indent+"\end{itemize}\n"
                    for file3 in subdir2.files:
                        main_string += indent+indent+"\item[$\\vartriangleright$] "+jtstr.latex_compatible(file3)+"\n"
                    main_string += indent+indent+"\end{itemize}\n"
            for file2 in subdir.files:
                main_string += indent+"\item[$\\vartriangleright$] "+jtstr.latex_compatible(file2)+"\n"
            main_string += indent+"\end{itemize}\n"
        for file in self.files:
            main_string += "\item[$\\vartriangleright$] "+jtstr.latex_compatible(file)+"\n"
        main_string += "\end{itemize}\n"
        "\\setstretch {1.433}%\n"
        # returning the whole string
        return main_string
        
    def get_name(self, path=False):
        """
        returns the name of the directory
        ###
        path - (~bool) wether the whole path shall be returned or not   
        ###
        RETURNS (string)
        """
        if path == False:
            return self.name
        else:
            return self.path
        
    def get_file(self, value, path=False):
        """
        returns the file specified value, either by name or index
        ###
        value - (int) the index of the file with in the local list
        path - (~bool) wether the whole path shall be returned or not
        ###
        RETURNS (string)
        """
        if value < len(self.files):
            # checking wether the whole path or the name is requested
            if path == False:
                return self.files[value]
            elif path == True:
                return self.path+"\\"+self.files[value]
        else:
            return False
            
    def get_files(self, path=False):
        """
        returns the list of filenames
        ###
        path - (~bool) wether the whole path shall be returned or not
        ###
        RETURNS (list/string)
        """
        # checking wether the whole path or the name is requested
        if path == False:
            return self.files
        elif path == True:
            temp_list = []
            for filename in self.files:
                temp_list.append(self.path+"\\"+filename)
            return temp_list
    
    def get_subdir(self, name):
        """
        returns the file specified value, either by name or index
        ###
        name - (string) the name of the directory
        path - (~bool) wether the whole path shall be returned or not
        ###
        RETURNS (Directory)
        """
        return self._subdirs[name]
        
    def get_subdirs(self):
        """
        returns the list of Directory objects of the subdirectories within
        ###
        path - (~bool) wether the whole path shall be returned or not
        ###
        RETURNS (list/string)
        """
        return self.subdirs
        
    def create_file(self, name, content=None):
        """
        creates a file with the given name in the directory and returns wether
        the creation was successful or not
        ###
        name - (string) the name and the filetype of the file to create
        content - (~string) the string content, that should be written into the file
                            after creation
        ###
        RETURNS (bool)
        """
        fullpath = self.path+"\\"+name
        if not(os.path.exists(fullpath)):
            createfile(fullpath)
            if not(content == None):
                try:
                    file = io.open(fullpath, "w")
                    file.write(content)
                    file.close()
                except:
                    return False
            if os.path.exists(fullpath):
                return True
            else:
                return False
        else:
            return False
        