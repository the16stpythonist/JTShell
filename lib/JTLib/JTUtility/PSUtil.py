# -*- coding: utf-8 -*-
"""
Created on Fri May 29 09:18:01 2015
@author: Jonas
###
The module to contain additional utilitiy and the overall basics
when programming/designing python scripts to be executed from the microsoft
powershell environment.
"""
import sys
import os
import JTLib.JTOS.JTWindows as jtwin
import JTLib.JTUtility.JTString as jtstr

"""
a function designed for the interactive mode of the Powershell scripts, given an
description of the wanted result and a list of acceptable answers, this function
will keep asking the question given until the user enters an valid answer
###
description - (string) the descriptive string to be displayed to explain the 
                       wanted input to the user
input_string - (string) the rting that shall be showed to the user, when
                        entering the unput
expected_answers - (list/string) a list with predefined answers, that will be
                                 accepted as an input
"""
def ask_for(description, input_string, expected_answers):
    answer_correct = False
    temp_answer = ""
    if not(expected_answers=="all"):
        while(not(answer_correct)):
            print(description)
            temp_answer = input(input_string)
            print(" ")
            if temp_answer in expected_answers:
                answer_correct = True
                break
            else:
                temp_answer = ""
                print("the given answer isnt an available option.")
    # in case every answer is accepted, the function will just return the first input
    else:
        print(description)
        temp_answer = input(input_string)
        print(" ")
    return temp_answer
    

"""
a function to ask the user, wether to save the content in a file or not, if given
the answer yes does so.
Dont fucking ask me about what the fuck i did there, i hope it works
###
content - (string) the content string to be written into the file
"""    
def ask_savefile(content):
    result = ask_for("save the result in a seperate file?", "> ", ["yes","y","no","n"])
    if result in ["y","yes"]:
        temp_path = input("path: ")
        if not(os.path.exists(temp_path)):
            print("...creating file")
            jtwin.createfile(temp_path)
            if os.path.exists(temp_path):
                print("...created file succesfully")
                print("...writing content into the file")
                try:
                    temp_file = open(temp_path, mode="w")
                    temp_file.write(content)
                    temp_file.close()
                    print("...succesfully written content into file: {0}".format(temp_path))
                except:
                    print("...ERROR: failed to write content into file: {0}".format(temp_path))
            else:
                print("...ERROR: failed to create file: {0}".format(temp_path))
                return 0
        else:
            if os.path.getsize() > 50:
                result = ask_for("the file already inherits content, override or append to it?","> ",["override","append"])
                if result == "append":
                    try:
                        print("...appending content to the file")
                        temp_file = open(temp_path, mode="r")
                        temp_cache = temp_file.read()
                        temp_file.close()
                        temp_file = open(temp_path, mode="w")
                        temp_file.write(temp_cache+"\n"+content)
                        temp_file.close()
                        print("..succesfully appended content to the file: {0}".format(temp_path))
                    except:
                        print("...ERROR: couldnt append content to the file: {0}".format(temp_path))
                elif result == "override":
                    try:
                        print("...overriding the file with the content")
                        temp_file = open(temp_path, mode="w")
                        temp_file.write(temp_cache+"\n"+content)
                        temp_file.close()
                        print("...succesfully overridden the file: {0}".format(temp_path))
                    except:
                        print("...ERROR: couldnt override the content of the file: {0}".format(temp_path))
            else:
                try:
                    print("...writing content to the file")
                    temp_file = open(temp_path, mode="w")
                    temp_file.write(temp_cache+"\n"+content)
                    temp_file.close()
                    print("...succesfully written conten into the file: {0}".format(temp_path))
                except:
                    print("...ERROR: couldnt write content to the file: {0}".format(temp_path))

"""
a function to save the given content into the file given, in case it doesnt exist
it will create one, in case it does exist itll override its original string
###
path - (string) the path of the file the content should be saved into
content - (string) thje content to be saved
"""            
def savefile(path, content):
    if os.path.exists(path):
        try:
            print("...writig content into the file")
            temp_file = open(path, mode= "w")
            temp_file.write(content)
            temp_file.close()
            print("...succesfully written content into the file: {0}".format(path))
        except:
            print("...ERROR: failed to write content into the file: {0}".format(path))
    else:
        print("...creating file")
        jtwin.createfile(path)
        if os.path.exists(path):
            print("...created file succesfully")
            print("...writing content into the file")
            try:
                temp_file = open(path, mode="w")
                temp_file.write(content)
                temp_file.close()
                print("...succesfully written content into file: {0}".format(path))
            except:
                print("...ERROR: failed to write content into file: {0}".format(path))
        else:
            print("...ERROR: failed to create file: {0}".format(path))
            return 0
        
    

"""
the bease class of an further executable Ms Powershell Python Script, giving the
advantage of a preformatted dictionary with the given arguments and the interface
functionality of a parent class.
Users of this class simply have the child class inherit from it, call the super-
constructer, configure the help string and append to the run method to make the
script work
"""
class PowerShellScript():
    """    
    args - (dict/string-string) the arguments passed by the call within the
                                Powershell, organizd with the paremeter name
                                being the key of the value tuple
    help - (string) the string that is displayed, when callng the help option of 
                    the given script. Has to be written in the child class
    """
    def __init__(self, arg):
        # sets up the arguments of the script
        self.args = {}
        self.add_arguments(arg)
        # sets up the help string for the Script, that is displayed
        self.help = ""
        
    def build(self):
        """
        has to be called whenever the script is used directly from the Microsoft
        PowerShell, as it is intializing the arguments passed to the script through
        the system variable sys.argv
        ###
        RETURNS (void)
        """
        self._calc_arguments()
        
    def add_arguments(self, arg):
        """
        has to be called whenever th script is used from within the JTShell 
        environment, adds the parameters, which would normally be provided directly
        by the system variable.
        ###
        arg - (string) the string passed onto the shell
        ###
        RETURNS (void)
        """
        # dividing the given string into the the list of arguments and the given
        # values of these parameters, by breaking the string by every appearance
        # of the '-' key and making an exception at the "" separation
        
        # the toggle wether inside an separated string
        in_separation = False
        # the temporary key, value pair of the current argument
        temp_argument_tuples = []
        # the actual temporary string
        temp_string = ""
        # first step: dividing the string into strings of key/value pairs with whitespaces
        for character in arg:
            # toggeling the separation condition
            if character == '"':
                if in_separation:
                    in_separation = False
                else:
                    in_separation = True
            # breaking the temporary string in case the keycharacter "-" appears
            if character=="-" and not(in_separation):
                temp_argument_tuples.append(temp_string)
                temp_string = ""
            # adding the character to the temporary string
            temp_string += character
        temp_argument_tuples.append(temp_string)
        temp_argument_tuples.remove("")
        
        # second step: itering through the tempory list and then appending the
        # argiuments to the arguments dictionary of the class
        for string in temp_argument_tuples:
            temp_string = jtstr.divide_by_custom(string, " ")[0]
            if '"' in string:            
                self.args[temp_string] = string.replace(temp_string+" ","").replace('"',"")
            else:
                self.args[temp_string] = string.replace(temp_string+" ","")
                
        
    def _check_arg(self, arg_string, expected_answers):
        """
        returns wether the given agument has been passed by the call and wether
        the assigned value matches the expected anwnsers
        ###
        arg_string - (string) the string of the argument to chek for
        expected_awnsers - (list/string) the list containing all the accepted
                                         values for the parameter to check
        ###
        RETURNS (bool)
        """
        if not(expected_answers == "all"):
            return (arg_string in self.args.keys() and self.args[arg_string] in expected_answers)
        else:
            return (arg_string in self.args.keys())
        
    def _calc_arguments(self):
        """
        the method to properly create the "self.arguments" variable of the 
        class, therefor using the additional arguments provided by the
        call of the powershell to put those into an dictionary with the
        parameter name being the key.
        ###
        RETURNS (void)
        """
        temp_tuple = []
        for parameter in sys.argv[1:]:
            if not(len(temp_tuple) == 2):
                temp_tuple.append(parameter)
            if len(temp_tuple) == 2:
                self.args[temp_tuple[0]] = temp_tuple[1]
                temp_tuple = []
                
    def display_help(self):
        """
        the method to simply print the help string, that should be written 
        within every child class of the object.
        ###
        RETURNS (void)
        """
        print(self.help)
        
    def run(self):
        """
        the main method of the script to run in. the whole process should be
        added in here. When writing child classes of this class, the 'run'-method
        version of the parent class should be called using the 'super'-syntax
        ###
        RETURNS (void)
        """
        if ("-help" in self.args.keys()):
            if self.args["-help"] in ["disp","diplay","show","true"]:
                self.display_help()
    
    

"""
a class representing a Table, that can be used in the Microsoft PowerShell
Environment. As parameters this class expects lists, which will then be the individual
lines of the table
###
headline - (list/string) the list containing the headers for the different columns
                         the following lists, representing the lines, are expected
                         to inherit just as many entries as this first list in
                         order to be formatted correctly
"""        
class PowerShellTable():        
    """
    max_characters - (int) the width of the PowerShell window meassured in characters
    """
    def __init__(self, headline,*argv):
        self.max_characters = 170
        self.headline = headline
        self.lines = argv
        
    def add_line(self, line):
        """
        adds a line to the table
        ###
        line - (list/string) the list with the columns of the line
        ###
        RETURNS (void)        
        """
        self.lines.append(line)        
        
    def get_string(self, columnlength=False):
        """
        retuns the Table as a string, perfectly formatted to fit into the PowerShell
        environment
        ###
        RETURNS (string)
        """
        # setting up the list for the for loops, the list being iterable with 
        # integers representing the indexes for the different columns of the table
        columns = range(0, len(self.headline))
        result = ""
        # getting the columnlength either as the given parameter or through 
        # calculating it with the assigned function 'self._cacl_columnlength'
        columnlength_list = []        
        if not(columnlength == False):
            columnlength_list = columnlength
        else:
            columnlength_list = self._calc_columnlength()
        # starting to write the headlines into the string with a for loop and
        # the assigned column lengths
        for column in columns:
            result += self.headline[column]
            result += " "*(columnlength_list[column]-len(self.headline[column]))
        # writing the seperating lines into the string
        for column in columns:
            result += len(self.headline[column]) * "-"
            result += " " * (columnlength_list[column]-len(self.headline[column]))
        # itering through every line and writing the single columns individually
        # like before
        for line in self.lines:
            for column in columns:
                result += line[column]
                result += " " * (columnlength_list[column]-len(line[column]))
            result + "\n"
        # returning the resulting string
        return "\n"+result
        
    def _calc_columnlength(self):
        """
        calculates the column length in characters dependent on the longest entry
        in the said column and then returns a listof intergers, representing
        the calculated lengths
        ###
        RETURNS (list/int)        
        """        
        temp_list = []
        temp_max_length = 0
        for column in range(0,len(self.headline)-1):
            # now the code that is executed on every single column
            # setting the max length to the length of the headline first to have
            # a reference to begin with 
            temp_max_length = len(self.headline[column]) + 1
            # going through every line and therefor every item in the chosen column
            # and compare it with the reference length in case theres a greater one
            # replacing the temporary variable for the max length
            for line in self.lines:
                if len(line[column]) > temp_max_length:
                    temp_max_length = len(line[column]) + 1
            # checking for the last column to assign the left over space instead
            # of the calculated value to make it fit the window
            if column == (len(self.headline)-1):
                # making a summation of the already given column lengths to get
                # the difference to the maximum window width
                temp_sum = 0
                for length in temp_list:
                    temp_sum += length
                temp_max_length = self.max_characters - temp_sum
            # finally adding the max length for the chosen column to the final list
            temp_list.append(temp_max_length)
            temp_max_length = 0
        temp_list.append(self.max_characters-temp_list[len(temp_list)-1])
        # returning the resulting list, that should have as many entries as the
        # number of columns
        return temp_list