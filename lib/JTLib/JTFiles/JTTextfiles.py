# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 16:23:22 2015
@author: Jonas
###
A package containg functions and classes for the representation of textfiles and
logfiles 
"""
import os
import JTLib.JTOS.JTCombinedOs as jos

def write_file(path, text):
    """
    writes the given string format text into the file specified by the given
    absolute path
    ###
    path - (string) the absolute path of the file to write into
    text - (string) the text to be written into the file
    ###
    RETURNS (void)
    """
    try:
        with open(path, "w") as output:
            output.write(text)
            output.close()
    except:
        print("Die Datei: "+path+" konnte nicht geoffnet werden")
        
        
def append_file(path, text):
    """
    instead of overwriting the whole file, appnds the given text to the end of 
    the file specified by its absolute path
    ###
    path - (string) the absolute path of the file to write into
    text - (string) the text to be written into the file
    ###
    RETURNS (void)
    """
    try:
        with open(path, "r") as inpu:
            val = inpu.read()
            inpu.close()
        with open(path, "w") as output:
            output.write(val+"\n"+text)
            output.close()
    except:
        print("Die Datei: "+path+" konnt nicht geöfnnet werden")
        
      
def is_validtextfile(path):
    """
    given an absolute path, returns wether the path exists, defines an actual
    file and is of the '.txt' format
    ###
    path - (string) the absolute path of the file to be checked 
    ###
    RETURNS (bool)
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            if path[len(path)-3: len(path)] == "txt":
                return True
            else:
                return False
        else:
            return False
    else:
        return False
        
      
"""
a representation of a simple text file, the file is opened with all its previous
contents, or in case there isnt a file with the given name, one will be created.
provides basic file/string manipulation methods and functionalities. Although
mainly serving as the base class for a row of object oriented file descriptors 
###
path - (string) the path of the file to open, or to create 
contentlog - (bool) wether the content is separatly logged within a temporary 
                     class list variable. False on default
overwrite - (bool) if the file already exists, decides wether the content should
                   be overwritten or not
"""        
class SimpleFile():
    """
    path - (string) the string representing the path of the file
    fileinput - (openr) the reading-instance of the file
    fileoutput - (openw) the writing-instance of the file
    contentstring - (string) astring inheriting the whole content of the file
    opsystem - (string) - the operating system of the current computer
    cond - (bool) wether the content is separatly logged within a temporary class
                  list variable    
    """
    #METHODS
    def __init__(self, path, contentlog, overwrite):
        self.path = path
        self.opsystem = jos.get_os()
        self.cond = contentlog
        self.contentstring = ""
        # if there is no file, it'll create one depending on the operating system
        if not(is_validtextfile(self.path)):
            jos.createfile(self.path)
        # declearing reading and writing instances
        self.fileinput = open(self.path, "r")
        if not(overwrite):
            startstr = self.fileinput.read()
            self.contentstring += startstr+"\n"
        self.fileoutput = open(self.path, "w")
        if not(overwrite):
            self.fileoutput.write(self.contentstring)
        
    def writeln(self, text):
        """
        writes the given 'text' into the file and adds a linebreak before
        ###
        text - (string) the text to be written into the file  
        ###
        RETURNS (void)
        """
        if self.cond:
            self.contentstring += "\n"+text
        self.fileoutput.write("\n"+text)
        
    def end(self):
        """
        closes the 'open' objects and shuts down the main object itself. Must 
        be called at the end of every program 
        ###
        RETURNS (void)
        """
        self.fileoutput.close()
        self.fileinput.close()
        
    def getcontent(self):
        """
        returns the content of the whole file up to the point of the call
        ###
        RETURNS (void)
        """
        if self.cond:
            return self.contentstring
    
"""
the interface tom make sure the logging classes implement the 'writelog' function
as this may be useful for working with generalized logging possibilities and 
therefor preventing errors. Should be implemented for every JTLogfile class
"""
class IBaseLog():
    """
    nothing - (?) not here
    """
    def __init__(self):
        # abstract interface
        pass
    
    def writelog(self, datalist):
        """
        writes a logfile entry depending on the given dataset
        ###
        RETURNS (void)
        """
        pass
    
  
"""
a representation of a simple log file, divided into varios columns and rows
of data.
###
path - (string) the path of the file 
columnsubjectlist - (list/string) the list of columntitles
text - (string) the string, with which the log begins
overwrite - (~bool) if the file already exists, decides wether the content should
                    be overwritten or not. False on default
"""      
class SimleLogfile(SimpleFile, IBaseLog):
    """
    path - (string) the string representing the path of the file
    fileinput - (open(mode='r')) the reading-instance of the file
    fileoutput - (open(mode='w')) the writing-instance of the file
    contentstring - (string) astring inheriting the whole content of the file
    opsystem - (string) - the operating system of the current computer
    columncount - (int) the number of columns used
    rowcount - (int) the number of rows used
    columnsubjects - (list/string) the list of columntitles
    bar - (string) an alignment of '----'
    """  
    def __init__(self,path,columnsubjectlist, text="*** log begin ***", overwrite=False):
        SimpleFile.__init__(self,path,False,overwrite)
        IBaseLog.__init__(self)
        self.columnsubjects = columnsubjectlist
        self.columncount = len(self.columnsubjects)
        self.rowcount = 0
        self.bar = "------------------------------------------------------------------------\n"
        columntitles = ""
        for a in self.columnsubjects:
            columntitles += a + " |"
        self.writeln("\n"+text+"\n")
        self.writeln(columntitles + self.bar)
        
    def writelog(self, datalist):
        """
        writes a logfile entry depending on the given dataset defined by 'vallist'
        vallist - (list\int) a list full of values to be asigned to the columns
                             in an order from left to right
        """
        # in case the data set has the same length like the subjects
        if len(datalist) == len(self.columnsubjects):
            b = 0
            newstr = ""
            temp = ""
            for a in datalist:
                temp = ""
                newstr += str(a)
                for c in range(0,len(self.columnsubjects[b])-len(str(a)), 1):
                    temp += " "
                newstr += temp
                newstr += " |"
            self.writeln(newstr)
            
    def end(self, text="*** log end """):
        """
        ends the the file ! must be called at the end of the program
        text - (string) the text, which ends the logfile
        """
        self.writeln(self.bar)
        self.writeln(text)
        SimpleFile.end(self)

        
"""
an extension to the SimpleFile functionalities, giving the posibility to
write gathered data into a Microsoft Excel compatible textfile 
###
path - (string) the path of the file to be used as the datalog
subjects - (list/string) the subject of the specific column 
separation - (~string) the character wich is used as the excel separation
                       condition for the individual columns. is set to
                       semicolon on default
contentlog - (~bool) wether the content is separatly logged within a temporary 
                     class list variable. False on default
overwrite - (~bool) if the file already exists, decides wether the content should
                    be overwritten or not
"""        
class ExcelLogfile(SimpleFile):
    """
    path - (string) the string representing the path of the file
    fileinput - (openr) the reading-instance of the file
    fileoutput - (openw) the writing-instance of the file
    contentstring - (string) astring inheriting the whole content of the file
    opsystem - (string) - the operating system of the current computer
    subjects - (list/string) the subjects of the individual columns of data
    separation - (string) the character wich is used as the excel separation
                          condition for the individual columns
    cond - (bool) wether the content is separatly logged within a temporary class
                  list variable
    """    
    def __init__(self, path, subjects, separation=";", contentlog=False, overwrite=False):
        # initializing the construtor of SimpleFile
        SimpleFile.__init__(self, path, contentlog, overwrite)
        self.separation = separation
        self.subjects = subjects 
        self.contentlist = []
        self.cond = contentlog
        # writing the subjects into the file
        self.writelog(self.subjects)
        
    def writelog(self, datalist):
        """
        writes the given list if data into the next row of the textfile
        ###
        datalist - (list/int) a list with the data to be written into the file
        ###
        RETURNS (void)
        """
        main_str = ""
        # adds all items in the datalist to the temporary string
        for item in datalist:
            if not(main_str == ""):
                main_str += self.separation
            if self.cond:
                self.contentlist += datalist
            main_str += str(item)
        # writes the temporary string into the file
        self.writeln(main_str)
        
    def __len__(self):
        """
        if the contentlog behaviour is enabled this will, upon calling the 
        python len() function on the object, return the number of rows given.
        ###
        RETURNS (int)
        """
        if self.cond:
            return len(self.contentlist)
        else:
            print("the excel log hasnt enabled the contentlog option, thus not being able to return the length")
            
    def get_column(self, index):
        """
        if the contentlog behaviour is enabled, this will return the column with
        the number specified by the index, otherwise it'll raise an error message
        and return an empty list
        ###
        RETURNS (list/int)        
        """
        if self.cond:
            # adding the item at the index of every sublist to the temporary list
            main_list = []
            for sublist in self.contentlist:
                main_list.append(sublist[index])
            return main_list
        else:
            print("the excel log hasnt enabled the contentlog option, thus not being able to return the column")
            
    def get_row(self, index):
        """
        if the contentlog behaviour is enabled, this will return the row with
        the number specified by the index, otherwise it'll raise an error message
        and return an empty list
        ###
        RETURNS (list/int)  
        """
        if self.cond:
            # adding the sublist of the given index to the temporary list
            return self.contentlist[index]
        else:
            print("the excel log hasnt enabled the contentlog option, thus not being able to return the row")
            