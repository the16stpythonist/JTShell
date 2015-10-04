# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 16:23:22 2015
@author: Jonas
###
A package containg functions and classes for the counterpart analyzation of the
JTTextfiles created logfiles
"""
import os

"""
a class which is used to analyze the logfile, produced by the Schiller in Space
microcontroller. Also providing methods, to save such data or output it directly
in individual datasets
###
path - (string) the path of the logfile to be used 
"""
class SimpleLogfileAnalyzer():
    """
    path - (string) the filepath of the file
    file - (open) the opened version of the file as a reading instance
    subjectlist - (list/string) a list containing the names of the subjects
    datasetlist - (list/list/string) a list containing various sublist, which
                                      themselves represent the datasets of the 
                                      individual columns
    """
    def __init__(self, path):
        # opening the file
        self.path = path
        self.file = open(self.path, "r")
        # a temporary list of lines
        lines = self.getlines(self.file)
        lines = self.remove_linebreak(lines)
        lines = self.remove_nondata(lines)
        self.rowcount = len(lines) - 1
        # the list of subjects
        self.subjectlist = self.get_subjectlist(lines)
        self.columncount = len(self.subjectlist)
        # the main list of the individual data sets
        self.datasetlist = self.get_datasetlist(lines)
        self.datasetlist = self.convert_data(self.datasetlist)
        
        
    def getlines(self, file):
        """
        given a file, this method will divide it into a list, containing the
        single lines of the file ('\n' included)
        ###
        file - (open) the reading instance of the file 
        ###        
        RETURNS (list\file)
        """
        return file.readlines()
    
    def remove_linebreak(self, line_list):
        """
        given the list of lines, this method will remove the '\n' from the strings
        line_list - (list\string) a list of lines of the file
        ###        
        RETURNS (list\file)
        """
        temp_list = line_list
        for line in temp_list:
            line.replace("\n", "")
        return temp_list
        
    def remove_nondata(self, line_list):
        """
        given the list of lines, this will remove every line, which is not relevant
        for the data of the log
        ###        
        line_list - (list\string) a list of lines of the file
        ###        
        RETURNS (list\file)
        """
        temp_list = line_list
        new_list = []
        for line in temp_list:
            if "|" in line:
                new_list.append(line)
        return new_list
        
    def convert_data(self, datasetlists):
        """
        converts the data, in string format to floating point format
        ###
        datasetlists - (list\list\string)
        ###        
        RETURNS (list\list\float)
        """
        new_list = []
        temp_list = []
        try:
            for sublist in datasetlists:
                temp_list = []
                temp_list.append(sublist[0])
                for a in range(1, len(sublist)-1, 1):
                    temp_list.append(float(sublist[a]))
                new_list.append(temp_list)
            return new_list
        except:
            print("the SimpleLogfile couldn't be converted")
            return ""
        
    def divide_by(self, string, symbol):
        """
        given a string and a specific symbol, this method will turn the string into
        multiple substrings dividing the main string by breaking after the symbol
        is referenced inside the string
        ###
        string - (string) the string to be divided
        symbol - (char) the break condition, only one character allowed
        ###        
        RETURNS (list\file)
        """
        new_list = []
        temp_string = ""
        # if the break symbol is registered the temporary string is added to
        # the new list, therefor beginning anew
        for char in string:
            if str(char) == symbol:
                new_list.append(temp_string)
                temp_string = ""
            else:
                temp_string += str(char)
        return new_list
        
    def get_subjectlist(self, line_list_removed):
        """
        given the list of lines, which has already been refined by the remove methods
        this method will calculate a list with all the column titles
        ###
        line_list_removed - (string) a list of lines, already refinded
        ###        
        RETURNS (list\string)
        """
        return self.divide_by(line_list_removed[0], "|")

    def get_datasetlist(self, line_list_removed):
        """
        given the list of lines, which has already been refined by the remove methods,
        this method will create a list, made out of sublists, all represnting
        a dataset of an column, rather than a line\row
        ###
        line_list_removed - (string) a list of lines, already refinded
        ###        
        RETURNS (list\list\string)
        """
        new_list = []
        temp_list = []
        p_list = line_list_removed
        # adding the right amount of sublists to the main list, which is to be 
        # returned later
        for a in range(0, len(self.divide_by(p_list[0], "|")), 1):
            new_list.append([])
        # the foreach loop through the lines of the logfile
        for line in p_list:
            # adding the divided data to the right sublists
            temp_list = self.divide_by(line, "|")
            b = 0
            for substr in temp_list:
                new_list[b].append(substr.replace(" ", ""))
                b += 1
        return new_list
        
    def get_length(self):
        """
        returns the amount of datasets within the file
        ###        
        RETURNS (int)
        """
        return len(self.subjectlist)
    
    def get_dataset_windex(self, index):
        """
        returns the dataset at the given index 
        ###        
        index - (int) the index
        ###        
        RETURNS (list\string)
        """
        if self.get_length() >= index+1:
            return self.datasetlist[index]
        else:
            return self.datasetlist[0]
            
    def get_dataset_wname(self, subjectstring):   
        """
        returns the dataset from the given subject
        ###
        subjectstring - (string) the subject of the dataset
        ###        
        RETURNS (list\string..double)
        """
        new = []
        for sublist in self.datasetlist:
            if sublist[0] in subjectstring:
                new = sublist[1:]
        return new
        

            
    def get_rowcount(self):
        """
        returns the rowcount of the file
        ###        
        RETURNS (int)
        """
        return self.rowcount
        
    def get_columncount(self):
        """
        returns the columncount of the file
        ###        
        RETURNS (int)
        """
        return self.columncount


