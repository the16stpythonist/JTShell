# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:26:08 2015
@author: Jonas
###
A module providing a two sided functionality to create basic python documentations.
The first side being the analytic processing of the written code and the representation
of python syntax with DocumentedObjects. The second side being the usage of said 
objects to create Documentation-Files in various formats such as .tex, .txt, .pdf etc.

The module offers mid-level functionality, while also providing a fairly simple, yet
relativly potent syntax, which is mainly based on indendation to stay close to the 
underlying programming style of python.

The syntax is best decribed with the small Example within the 'JTDocumentation_Example.txt'
file, but can also be descriped quickly:

Documented packages should have an '__init__.py' file, at least containing a
python-Docustring with the description of said package and even in case no description
will be needed there should be at least an empty docustring present.
Documented files should also have a Docustring at the beginning providing the user
with a quick overview of the main purpose of the specified module. Classes should 
have a Docustring right on top of there deklaration, containing firstly a quick 
description and then, seperated by a so called separation condition ('###', put in a seperate
line in bewteen), a list with the parameters of the constructor. On the next level on indendation,
meaning the same level of indent as the constructor and right beneath the class name there has to
be a docustring contianing the class variables, they will be syntax-wise treated as Parameters.
The constructor of the class itself doesn't need a docustring, every following method after has to
have a docustring on the next layer of indendation(on the layer of the source code),which has to 
contain at least a description and a definition of the returned datatype: RETURNS (Type), seperated
by a separation condition. Optional is the list of function parameters in between.
Functions will be handled like methods.

Parameters are build as followed: name - (Type) Parameterdescription. The type can be
a single string or a nested list/dict/tuple defined by separating it with the string '/'.
If the description is getting too long for the file, than it can be shifted to the next line,
although it must have the exact same indendation than the first part. There is also the
posibility of defining more than one datatype per Parameter, they again have to be placed
beneath the first description and must have the exact same indent. It is furthermore
possible to mark predefined/optional parameters within the documentation, they'll have to
be made visible by placing a '~' inside the type-brackets and in front of the actual type
"""
from JTLib.JTUtility.JTString import * 
import JTLib.JTOS.JTCombinedOs as jtos
import os
import time
import io


"""
A class representing a stored source code structure of JTDocumentation Parameter Syntax,
providing information about name, multiple type and descriptions and the possibilities
too create appropriate outputs of types and to translate into part of a latex 'tabular'
list environment. This class also supports various getter-methods and the indexing functions.
###
lines - (string) the substring, which should only contain the lines by which the
                 Parameter is described 
"""
class DocumentedParameter():
    """
    name - (string) the name of the parameter described by this very object
    type_description - (list/tuple/string-string) a list containing various tuples,
                                                  every one describing one pair of 
                                                  type of the parameter and the 
                                                  matching description
    """
    def __init__(self, lines):
        self._string = divide_by_custom(lines, "\n")
        self.name = ""
        self.type_description = []
        # getting the default indent, which describes the distance between the start
        # and the beginning of the type definition, leaving out the name 
        self.default_indent = ""
        for character in self._string[0]:
            if not(character == "("):
                self.default_indent += " "
            else:
                break
        # getting the name
        self.name = get_substring_before(self._string[0], "-").replace(" ", "")
        # getting the type and the matching description
        self._calc_datatype_and_description()        
        
    def close(self):
        """
        Terminates all important variables of the class. This method musnt be 
        called and rather represents a safety messure to make sure the memory isnt
        getting wasted.
        ###
        RETURNS (void)
        """   
        del self.type_description
        del self._string         

    def get_latex(self):
        """
        creates and returns the entry of the 'tabular' latex list environment
        ###
        RETURNS (string)
        """
        main_string = ""
        # going through the list of types and their descriptions
        index = 0
        for val in self.type_description:
            if index == 0:
                main_string += latex_compatible(self.name)+"&"+self._calc_latex_datatype(val[0])+"&"+latex_compatible(val[1])+"\\\\\n"
            else:
                main_string += "    &"+self._calc_latex_datatype(val[0])+"&"+latex_compatible(val[1])+"\\\\\n"
            index += 1
        return main_string
    
    def get_name(self):
        """
        returns the name of the of the parameter
        ###
        RETURNS (string)
        """
        return self.name
        
    def get_type_description(self):
        """
        returns the list of tuples containing the diferent variations of
        types and their matching descriptions
        ###
        RETURNS (list/tuple/string-string)
        """
        return self.type_description
        
    def _calc_latex_datatype(self, datatype):
        """
        converts the JTDocumentation DataType syntax into a fancy latex compatible
        string which will then be used in the documentation string
        ###
        RETURNS (string)
        """
        main_string = ""
        # checking for a top level list, dict or tuple
        if "/" in datatype:
            temp_list = divide_by_custom(datatype.replace("~",""), "/")
            substring = ""
            for index in range(0,len(temp_list)):
                substring = temp_list[index]
                if substring == "list":
                    main_string += "["
                elif substring == "dict":
                    main_string += "\{"+temp_list[index+1].replace("-",":")+"\}"
                    index+=1
                elif substring == "tuple":
                    main_string += "("+temp_list[index+1].replace("-",",")+")"
                    index+=1
                else:
                    main_string += substring
                index+=1
            if "[" in main_string:
                main_string += "]"
        else:
            main_string = datatype
        if "~" in datatype:
            main_string = "~ " + main_string
        # returning the result
        return main_string
       
    def _calc_datatype_and_description(self):
        """
        a method to create a tuple of the datatype and the matching description of
        the parameter, which will then be put and saved into the local class list
        variable 'self.type_description'
        ###
        RETURNS (void)
        """
        descr = ""
        typ = ""
        for line_index in range(0,len(self._string)):
            if line_index == 0:
                typ = get_substring_between(self._string[line_index],"(",")")
                descr = cut(self._string[line_index], len(self.default_indent)+len(typ)+2, len(self._string[line_index]) - 1)
            if len(get_indendation(self._string[line_index])) > len(self.default_indent):
                descr += " " + remove_indendation(self._string[line_index])
            elif len(get_indendation(self._string[line_index])) == len(self.default_indent):
                self.type_description.append((typ,descr))
                typ = get_substring_between(self._string[line_index],"(",")")
                descr = cut(self._string[line_index], len(self.default_indent)+len(typ)+3, len(self._string[line_index]) - 1)
        self.type_description.append((typ,descr))
        
    def __len__(self):
        """
        modified behaviour when the len() function is called on this object.
        returns the length of the list of the different types for the parameter
        ###
        RETURNS (int)
        """
        return len(self.type_description)
        
    def __getitem__(self, key):
        """
        modified behaviour when the index is used on this object.
        returns the item to the corresponding key given
        ###
        RETURNS (tuple/string-string)
        """
        return self.type_description[key]
        
    def __iter__(self):
        """
        modified behaviour when itering trhough this object.
        ###
        RETURNS (?)
        """
        return iter(self.type_description)        
        

"""
A class representing a stored source code structure of JTDocumentation method, providing
information about methodname, parameters and their specifications, a description
of said methods functionality and the type of the potentional returned value. This class also
provides functions to create a predefined layout in latex source code. 
###
lines - (string) the string which should mainly only contain the string by which
                 the whole methdod/function is described
        (list/string) a list of the individual lines of the defined source code
"""        
class DocumentedMethod():
    """
    name            - (string) definded name of the method
    _type           - (string) wether the object describes a "function" or a "method"
    description     - (string) the description string written beneath the functionname
    return_type     - (string) the return type of the method
    parameters      - (list/DocumentedParameter) a list, containing the DocumentedParameter objects
                                                 for all expected parameters of the functioncall
    default indendation - (int) the amount of whitespaces, that are needed for 
                                the indendation of the docustring, mainly needed for 
                                interal algorithm choices
    """
    def __init__(self, lines):
        self.name = ""
        self._type = ""
        self.description = ""
        self.parameters = []
        self.return_type = ""
        self.default_indendation = 0
        # setting up the strings depending on the parameter type
        if type(lines) is str:
            string = lines
            string = divide_by_custom(string, "\n")
            string_nowhitespace = lines.replace(" ", "")
            string_nowhitespace = divide_by_custom(string_nowhitespace, "\n")
        elif type(lines)is list:
            string = lines
            string_nowhitespace = []
            for line in string:
                string_nowhitespace.append(line.replace(" ",""))
        # getting the amount of separation conditions
        self._amount_separ_cond = 0
        for line in string_nowhitespace:
            if line == "###":
                self._amount_separ_cond += 1
        # getting the default indendation
        self.default_indendation = self._calc_indendation(string[1])
        self._default_indendation_str = " " * self.default_indendation
        # getting the name
        self._calc_name_type(string_nowhitespace)
        # getting the description
        self._calc_description(string_nowhitespace, string)
        # getting the parameters
        self._calc_parameters(string_nowhitespace, string)
        # getting the return type
        self._calc_returntype(string_nowhitespace)
       
       
    def close(self):
        """
        Terminates all important variables of the class. This method musnt be 
        called and rather represents a safety messure to make sure the memory isnt
        getting wasted.
        ###
        RETURNS (void)
        """
        del self.description
        # terminating the sub Documentation Objects
        for param_obj in self.parameters:
            param_obj.close()
         
    def get_latex(self, language):
        """
        creates and returns the latex compatible string of the method, mainly 
        missing a headline and consisting of the description of the method, 
        followed by the list of expected parameters and the returned type.
        ###
        language - (string) the language in which the keywords of the string 
                            should be created in
        ###
        RETURNS (string)
        """
        # adding the bold description keyword to the main string
        main_string = ""
        if language == "english":
            main_string += "\\textbf{Description}, "
        elif language == "german":
            main_string += "\\textbf{Beschreibung}, "
        # adding the actual description to the string
        main_string += latex_compatible(self.description)
        # adding the parameter table to the string
        if not(self.parameters == []):
            main_string += "\\begin{table}[H]\n\\flushleft\n\\begin{tabular}{p{4cm}p{5cm}p{7,8cm}}\n"
            main_string += "\\toprule\n"
            if language == "english":
                main_string += "Parameter & Datatype & Description \\\\\n"
            elif language == "german":
                main_string += "Parameter & Datentyp & Beschreibung \\\\\n"
            main_string += "\\midrule\n"
            for param in self.parameters:
                main_string += param.get_latex()
            main_string += "\\bottomrule\n\\end{tabular}\n\\end{table}\n\\newline\n"
        # returning the resilted string
        return main_string
        
         
    def get_name(self):
        """
        returns the name of the defined method
        ###
        RETURNS (string)
        """            
        return self.name
        
    def get_description(self):
        """
        returns the description of the method
        ###
        RETURNS (string)
        """
        return self.description
    
    def get_returntype(self):
        """
        returns the type of data, which the method returns
        ###
        RETURNS (string)
        """
        return self.return_type
        
    def get_parameters(self):
        """
        returns a list with 'DocumentedParameter' objects which define the
        parameters of the function
        ###
        RETURNS (list/DocumentedParameters)
        """
        return self.parameters
    
    def _calc_latex_datatype(self, datatype):
        """
        converts the JTDocumentation DataType syntax into a fancy latex compatible
        string
        ###
        RETURNS (string)
        """
        main_string = ""
        # checking for a top level list, dict or tuple
        if "/" in datatype:
            temp_list = divide_by_custom(datatype.replace("~",""), "/")
            substring = ""
            for index in range(0, len(temp_list)):
                substring = temp_list[index]
                if substring == "list":
                    main_string += "["
                elif substring == "dict":
                    main_string += "{"+temp_list[index+1].replace("-",":")+"}"
                    index+=1
                elif substring == "tuple":
                    main_string += "("+temp_list[index+1].replace("-",",")+")"
                    index+=1
                else:
                    main_string += substring
                index+=1
            if "[" in temp_list:
                main_string += ",...]"
        else:
            main_string = datatype
        if "~" in datatype:
            main_string = "~ " + main_string
        # returning the result
        return main_string    
    
    def _calc_name_type(self, no_whitespace):
        """
        a method to distinguish the name of the method and wether it is a method
        or an function and writes it into the 'self.name' and 'self.type' class variable
        ###
        no_whitespace - (list/string) a list with the lines of the method/function
                                      but without whitespace inbetween the characters
        ###
        RETURNS (void)
        """
        for line in no_whitespace:
            if cut(line, 0, 2) == "def":
                for char_index in range(3, len(line)-1):
                    if not(line[char_index] == "("):
                        self.name += line[char_index]
                    else:
                        break
                if "self," in line or "self" in line:
                    self._type == "method"
                else:
                    self._type == "function"
                break
            
    def _calc_description(self, no_whitespace, string):
        """
        a method to determine the description and writing it into the 'self.description'
        class variable
        ###
        no_whitespace - (list/string) a list with the lines of the method/function
                                      but without whitespace inbetween the characters
        string - (list/string) a list with the lines of the method/function
        ###
        RETURNS (void)
        """
        cond = False 
        for line_index in range(0, len(string)):
 
            if no_whitespace[line_index] == "###":
                cond = False
                break
            if cond == True:
                self.description += string[line_index] + "\n"
            if no_whitespace[line_index] == '"""':
                cond = True
        self.description = self.description.replace(self._default_indendation_str,"")
        
    def _calc_parameters(self, no_whitespace, string):
        """
        calculates the parameters and writes them as DocumentedParameters into
        the list of parameters
        ###
        no_whitespace - (list/string) a list with the lines of the method/function
                                      but without whitespace inbetween the characters
        string - (list/string) a list with the lines of the method/function
        ###
        RETURNS (int)
        """
        if self._amount_separ_cond == 2:
            cond = False
            temp_parameterstring = ""
            for line_index in range(0, len(string)):
                if cond == True and not(no_whitespace[line_index] == "###"):
                    if temp_parameterstring == "":
                        temp_parameterstring += string[line_index]
                    else:
                        if self._calc_indendation(string[line_index]) > self.default_indendation:
                            temp_parameterstring += "\n"+string[line_index]
                            
                        else:
                            self.parameters.append(DocumentedParameter(temp_parameterstring))
                            temp_parameterstring = string[line_index]
                if no_whitespace[line_index] == "###" and cond == False:
                    cond = True
                elif no_whitespace[line_index] == "###" and cond == True:
                    cond = False
                    break
            self.parameters.append(DocumentedParameter(temp_parameterstring))
                
    def _calc_returntype(self, no_whitespace):
        """
        calculates the return type of the given method and assigns it to the
        class variable self.return_type
        ###
        no_whitespace - (list/string) a list with the lines of the method/function
                                      but without whitespace inbetween the characters
        ###
        RETURNS (void)
        """
        borders = self._amount_separ_cond
        # looping until the destination has been found, which in turn is
        # dependant on the borders value
        for line in no_whitespace:
            if borders == 0 and (cut(line,0,6) == "RETURNS"):
                self.return_type = cut(line, 8, len(line) - 2)
            if line == "###":
                borders -= 1
            
    def _calc_indendation(self, string):
        """
        calculates the default indendation of the docustring
        ###
        string - (list/string) the list of the individual lines of the method
        ###
        RETURNS (int)
        """
        number_whitespace = 0
        if type(string) is list:
            for character in string[0]:
                if character is " ":
                    number_whitespace += 1
                else:
                    break
        elif type(string) is str:
            for character in string:
                if character is " ":
                    number_whitespace += 1
                else:
                    break
        return number_whitespace
                
                
"""
A class representing a stored source code structure of JTDocumentation class, providing
information about the description of a class, the parameters the constructor expects, 
the class variables used, the different methods and their own specifications.This class also 
provides functions to create a predefined layout in latex source code. 
###
lines - (string) the complete string of the source code of the class 
        (list/string) the individual lines of the source code
"""            
class DocumentedClass():
    """
    name - (string) the name of the class to document
    heredity - (list/string) a list of classnames from which the class inherits
    description - (string) the description of the class as a whole
    methods - (list/DocumentedMethod) a list of Methods of the class
    parameters - (list/DocumentedParameters) a list of parameters the constructor of the
                                             class expects
    variables - (list/DocumentedParameters) a list of the class variables of said class
    """
    def __init__(self, lines):
        # the class variables
        self.name = ""
        self.heredity = []
        self.description = ""
        self.methods = []
        self.parameters = []
        self.variables = []
        self._linelist = []
        self._linelist_nowhitespace = []
        # setting up the string lists depending on the parameter type
        if type(lines) is str:
            self._linelist = lines
            self._linelist = divide_by_custom(self._linelist, "\n")
            self._linelist_nowhitespace = lines.replace(" ", "")
            self._linelist_nowhitespace = divide_by_custom(self._linelist_nowhitespace, "\n")
        elif type(lines)is list:
            self._linelist = lines
            self._linelist_nowhitespace = []
            for line in string:
                self._linelist_nowhitespace.append(line.replace(" ",""))
        # hotfix
        if self._linelist_nowhitespace[0] == '"""' and self._linelist_nowhitespace[1] == '' and self._linelist_nowhitespace[2] == '"""':
            self._linelist = self._linelist[2:len(self._linelist)]
            self._linelist_nowhitespace = self._linelist_nowhitespace[2:len(self._linelist_nowhitespace)]
        # getting the name of the class
        self._calc_name()
        # getting the heredity of the class
        self._calc_herdity()
        # getiing the description of the class
        self._calc_description()
        # getting the parameters of the class
        self._calc_parameters()
        # getting the class variables of said class
        self._calc_variables()
        # getting the methods of the class
        self._calc_methods()
        
    def close(self):
        """
        Terminates all important variables of the class. This method musnt be 
        called and rather represents a safety messure to make sure the memory isnt
        getting wasted.
        ###
        RETURNS (void)
        """        
        # deleting the performance heavy variables
        del self.name
        del self.description
        del self._linelist
        del self._linelist_nowhitespace
        # terminating the sub Documentation Objects
        for param_obj in self.parameters:
            param_obj.close()
        for varia_obj in self.variables:
            varia_obj.close()
        for method_obj in self.methods:
            method_obj.close()
        
    def get_latex(self, language, color_list):
        """
        creates and returns the string format of the class, which is used to create
        a latex Documentation of the class, combining Description, Parameters, Variables
        and the latex-strings of all functions
        ###
        language - (string) the language of the important keywords/syntax
        ###
        RETURNS (string)
        """
        # seting up the main string
        main_string = "\\newpage\n"    
        # adding the headline and Description to the string
        main_string += "\n\\subsubsection{\\textcolor{"+color_list[2]+"}{"+latex_compatible(self.name)+"}}\n"
        if language == "english":
            main_string += "\\textbf{inherits from: }"
            for her in self.heredity:
                main_string += her+", "
            main_string += "\\\\\n"
            main_string += "\\textbf{Description, } "
        elif language == "german":
            main_string += "\\textbf{erbt von: }"
            for her in self.heredity:
                main_string += her+", "
            main_string += "\\\\\n"
            main_string += "\\textbf{Beschreibung, } "
        main_string += latex_compatible(self.description)+"\\\\\n"
        # adding the parameters 
        if not(self.parameters == []):
            main_string += "\\begin{table}[H]\n\\flushleft\n\\begin{tabular}{p{4cm}p{5cm}p{7,8cm}}\n"
            main_string += "\\toprule\n"
            if language == "english":
                main_string += "Parameter & Datatype & Description \\\\\n"
            elif language == "german":
                main_string += "Parameter & Datentyp & Beschreibung \\\\\n"
            main_string += "\\midrule\n"
            for param in self.parameters:
                main_string += param.get_latex()
            main_string += "\\bottomrule\n\\end{tabular}\n\\end{table}\n\\newline\n"
        # adding the variables
        main_string += "\\begin{table}[H]\n\\flushleft\n\\begin{tabular}{p{4cm}p{5cm}p{7,8cm}}\n"
        main_string += "\\toprule\n"
        if language == "english":
            main_string += "Variable & Datatype & Description \\\\\n"
        elif language == "german":
            main_string += "Variable & Datentyp & Beschreibung \\\\\n"
        main_string += "\\midrule\n"
        for var in self.variables:
            main_string += var.get_latex()
        main_string += "\\bottomrule\n\\end{tabular}\n\\end{table}\n\\newline\n"
        # adding all the methods
        for method in self.methods:
            main_string += "\n\\begin{large}\n\\begin{flushleft}\n\\textcolor{"+color_list[3]+"}{"+method.return_type+" } "+latex_compatible(method.get_name())+"\n\\end{flushleft}\n\\end{large}\n\\newline\n"
            main_string += method.get_latex(language)
        # returning the resulting main_string
        return main_string
        
    def get_name(self):
        """
        returns the name of the documented class
        ###
        RETURNS (string)
        """        
        return self.name
        
    def get_description(self):
        """
        returns the description of the documented class
        ###
        RETURNS (string)
        """
        return self.description
        
    def get_heredity(self):
        """
        returns the heredity of the documented class in form of list of classnames
        ###
        RETURNS (list/string)
        """
        return self.heredity

    def get_variables(self):
        """
        returns the local variales of the documented class as DocumentedParameters
        ###
        RETURNS (list/DocumentedParameter)
        """
        return self.variables
        
    def get_parameters(self):
        """
        returns the parameters of the constructor of the documented class
        as DocumentedParameters
        ###
        RETURNS (list/DocumentedParameter)
        """
        return self.parameters
        
    def get_methods(self):
        """
        returns the methods of the documentd class as a list of DocumentedMethods
        ###
        RETURNS (list/DocumentedMethod)
        """
        return self.methods

    def _calc_name(self):
        """
        calculates the name of the class and writes it into the 
        "self.name" local variable
        ###
        RETURNS (void)
        """
        # searching for the line in which the "class" statement appears and
        # then extrcating the defined name of said class
        for line in self._linelist:
            if cut(line, 0, 4) == "class":
                for ind in range(6, len(line)):
                    if not(line[ind] == "("):
                        self.name += line[ind]
                    else:
                        break
                break
                   
                   
    def _calc_herdity(self):
        """
        calculates the heredity of the given class and puts the parent classes
        into the local variable list "self.heredity"
        ! Requires the self.name variable to be calculated beforehand
        ###
        RETURNS (void)
        """
        # searching for the line with the "class" statement and the clasname 
        heredity_string = ""
        for line in self._linelist_nowhitespace:
            if cut(line, 0, 4) == "class" and self.name in line:
                heredity_string = get_substring_between(line, "(",")")
        # turning the heredity string into the list of the diferent parent classes
        if "," in heredity_string:
            self.heredity = divide_by_custom(heredity_string.replace(" ",""), ",")
        else:
            self.heredity.append(heredity_string.replace(" ",""))
            
            
    def _calc_parameters(self):
        """
        calculates the parameters which the class expects upon initialization and
        puts the DocumntedParameter objects into the öist of the loacal variable 
        "self.parameters"
        ###
        RETURNS (void)
        """
        # extracts the first docustring
        first_docustring = ""
        cond = False
        for line_index in range(0, len(self._linelist)):
            if self._calc_indendation(self._linelist[line_index]) == "" and self._linelist_nowhitespace[line_index] == '"""' and cond == True:
                cond = False
                break
            
            if cond == True:
                if first_docustring == "":
                    first_docustring += self._linelist[line_index]
                else:
                    first_docustring += "\n" + self._linelist[line_index]
                    
            if self._calc_indendation(self._linelist[line_index]) == "" and self._linelist_nowhitespace[line_index] == '"""' and cond == False:
                cond = True
        first_docustring = '"""\n' + first_docustring + '\n"""'

        # with no separation condition inside the string, there are no parameters
        # with one there hav to be parameters calculated
        if "###" in first_docustring:
            
            parameters_string = divide_by_custom(get_substring_between(first_docustring, "###\n", '"""'), "\n")          
            # extracting the parameters from the string
            temp_parameterstring = ""
            param_indent = self._calc_indendation(parameters_string[0])
            for line in parameters_string:
                if temp_parameterstring == "":
                    temp_parameterstring += line
                else:
                    if self._calc_indendation(line) > param_indent:
                        temp_parameterstring += "\n" + line
                    else:
                        self.parameters.append(DocumentedParameter(temp_parameterstring))
                        temp_parameterstring = line
            # doing the last append of the temporary buffer
            self.parameters.append(DocumentedParameter(temp_parameterstring))
            
            
        
    def _calc_description(self):
        """
        calculates the description of the class and writes it into the
        "self.description" local variable
        ###
        RETURNS (void)
        """
        # searching for the first docustring to appear, and exiting the search
        # after the iteration hit the first separation condition or the next docustring
        cond = False 
        for line_index in range(0, len(self._linelist)):
            if self._calc_indendation(self._linelist[line_index]) == "" and (self._linelist_nowhitespace[line_index] == "###" or self._linelist_nowhitespace[line_index] == '"""') and not(line_index == 0):
                cond = False
                break
            if cond == True:
                if self.description == "":
                    self.description += self._linelist[line_index]
                else:
                    self.description += "\n" + self._linelist[line_index]
            if self._calc_indendation(self._linelist[line_index]) == "" and self._linelist_nowhitespace[line_index] == '"""':
                cond = True
            
    def _calc_indendation(self, string):
        """
        calculates the indendation level of the given string
        ###
        string - (string) the string to be analyzed for the indent
        ###
        RETURNS (string)
        """
        # adds to the indent variable until the first text appears
        indendation = ""
        for character in string:
            if character == " ":
                indendation += character
            else:
                break
        # returning the calculated value
        return indendation

        
    def _calc_variables(self):
        """
        calculates the variables of the class and writes them as 
        DocumentedParameter-Objects into the local variable list "self.variables"
        ###
        RETURNS (void)
        """
        # starting the search after the classname
        start_index = 0
        for line_index in range(0,len(self._linelist_nowhitespace)):
            if cut(self._linelist_nowhitespace[line_index], 0, 4) == "class":
                start_index = line_index
                break
        # getting the sublist between the docustring borders
        variables_list  = get_sublist_between(self._linelist, '"""', '"""', start_index, whitespace=False)
        # extracting the parameters from the string
        temp_parameterstring = ""
        param_indent = self._calc_indendation(variables_list[0])
        for line in variables_list:
            if temp_parameterstring == "":
                temp_parameterstring += line
            else:
                if self._calc_indendation(line) > param_indent:
                    temp_parameterstring += "\n"+line
                else:
                    self.variables.append(DocumentedParameter(temp_parameterstring))
                    temp_parameterstring = line
        # doing the last append of the temporary buffer
        self.variables.append(DocumentedParameter(temp_parameterstring))
        
    def _calc_methods(self):
        """
        calculates the methods in the class string, passes the string to 
        DocumentedMethod objects and then puts them into the local list variable
        "self.methods"
        ###
        RETURNS (void)
        """
        # the variable of the default indent of a method
        method_indendation = ""
        # searching for the index of the constructor and then for when the next method
        start_index = 0   
        for line_index in range(0,len(self._linelist_nowhitespace)):
            if self._linelist_nowhitespace[line_index][0:11] == "def__init__":
                start_index = line_index
                method_indendation = self._calc_indendation(self._linelist[line_index])
                break
        # now searching for the next method start
        for line_index in range(start_index+1,len(self._linelist_nowhitespace)):
            if self._linelist[line_index][0:len(method_indendation)+3] == method_indendation + "def":
                start_index = line_index
                break
        # now doing the actual loop and adding to the methods list
        temp_method = ""
        for line_index in range(start_index-1,len(self._linelist)):
            if self._linelist[line_index][0:len(method_indendation)+3] == method_indendation + "def" and not(line_index == start_index) :
                self.methods.append(DocumentedMethod(temp_method))
                temp_method = self._linelist[line_index]
            else:
                if not(self._linelist_nowhitespace[line_index] == ""):
                    if temp_method == "":
                        temp_method += self._linelist[line_index]
                    else:
                        temp_method += "\n" + self._linelist[line_index]
        # doing the last append of the temporary buffer
        self.methods.append(DocumentedMethod(temp_method))
                                
"""
A class representing a stored source code structure of JTDocumentation file, providing information
about the Description of the module, defined in the first few lines, the imported modules, the functions
and the classes with their indiviual specifications. This class also 
provides functions to create a predefined layout in latex source code.
###
filepath - (string) the string which should mainly only contain the string by which
                    the whole methdod/function is described
"""            
class DocumentedFile():
    """
    name - (string) the name of the documented file
    description - (string) the description of the documented file
    author - (string) the author of the file 
    classes - (list/DocumentedClass) the classes within the file
    functions - (list/DocumentedMethod) the functions within the file
    filepath - (string) the filepath for the file
    imports - (list/string) the names of the imported modules
    _file - (open/r) the readable file object
    _linelist - (list/string) the list of lines of the file
    """
    def __init__(self, filepath):
        # setting up the local variables
        self.name = ""
        self.imports = []
        self.description = ""
        self.author = ""
        self.classes = []
        self._classes = {}
        self.functions = []
        self._functions = {}
        self.file = None
        self._linelist = []
        self._last_import = 0
        self.filepath = filepath
        # setting up the file environment and the string
        self.file = io.open(filepath, mode="r")
        temp_string = self.file.read()
        print(filepath)
        print(temp_string)
        self._linelist = divide_by_custom(temp_string, "\n")
        self._linelist_nowhite = []
        for line in self._linelist:
            self._linelist_nowhite.append(line.replace(" ", ""))
        # calculating the name of the file
        self._calc_name()
        # calculating the description and the author of the file
        self._calc_description_author()
        # calculating the imports
        self._calc_imports()
        # calculating the classes and the funtions in the file
        self._calc_classes_functions()          
         
    def close(self):
        """
        is used to close the file and delete all variables. Has to be called
        at the end of each objects lifecycle, although the garbage collection
        should work with terminating said object calling this method seperatly
        is a safety messure
        ###
        RETURNS (void)
        """   
        # closing the file object
        self.file.close()
        # deleting all performance heavy local variables
        del self.description
        del self._linelist
        del self.file
        # terminating all sub Documentation-Objects
        for class_obj in self.classes:
            class_obj.close()
        for func_obj in self.functions:
            func_obj.close()

    def get_latex(self, language, color_list):
        """
        creates and returns the string format of the file, which is used to create
        a latex Documentation of the module, combining description, imports, functions
        and classes within
        ###
        language - (string) the language of the important keywords/syntax
        ###
        RETURNS (string)
        """
        # seting up the main string
        main_string = ""
        # adding the section headline
        main_string += "\n\\subsection{\\textcolor{"+color_list[1]+"}{"+latex_compatible(self.name)+"}}\n"
        if language == "english":
            main_string += "\\textbf{imported modules: }"
            for imp in self.imports:
                main_string += imp+", "
            main_string += "\\\\\n"
            main_string += "\\textbf{Description, } "
        elif language == "german":
            main_string += "\\textbf{Importierte Module: }"
            for imp in self.imports:
                main_string += imp+", "
            main_string += "\\\\\n"
            main_string += "\\textbf{Beschreibung, } "
        main_string += latex_compatible(self.description)+"\\\\\n"
        # adding the functions
        for function in self.functions:
            main_string += "\n\\subsubsection{\\textcolor{"+color_list[2]+"}{"+function.return_type+" } "+latex_compatible(function.name)+"}\n"
            main_string += function.get_latex(language)
        # adding the classes
        for clas in self.classes:
            main_string += clas.get_latex(language, color_list)
        # returng the string
        return main_string+"\n"
        

    def get_name(self):
        """
        returns the name of the documented File
        ###
        RETURNS (string)
        """
        return self.name
        
    def get_author(self):
        """
        returns the author of the documented file, in case there is one given.
        optional
        ###
        RETURNS (string)
        """
        return self.author
        
    def get_description(self):
        """
        returns the description of the documented file.
        the file includes linebreaks as they were made in the original file
        ###
        RETURNS (string)
        """
        return self.description
        
    def get_filepath(self):
        """
        returns the filepath of the documented file.
        ###
        RETURNS (string)
        """
        return self.filepath
        
    def get_classes(self):
        """
        returns a list with DocumentedClass objects of the documented file
        ###
        RETURNS (list/DocumnetedClass)
        """
        return self.classes
        
    def get_class(self, name):
        """
        returns the DocumentedClass objcte with the name given
        ###
        RETURNS (DocumentedClass)
        """
        return self._classes[name]
        
    def get_functions(self):
        """
        returns a list with DocumentedMethod objects of the documented file
        ###
        RETURNS (list/DocumentedMethod)
        """
        if name in self._classes.values:
            return self.functions
        
    def get_function(self, name):
        """
        returns the the DocumentedMethod object with the name given
        ###        
        RETURNS (DocumentedMethod)
        """
        if name in self._functions.values:
            return self._functions[name]
         
    def _calc_name(self):
        """
        calculates the name of the documented file and writes it without the suffix
        into the "self.name" local variable
        ###
        RETURNS (void)
        """
        # searching for the name of the file in the filepath
        directory_list = divide_by_custom(self.filepath, "\\")
        file_buffer = divide_by_custom(directory_list[-1], ".")
        self.name = file_buffer[0]
        # deleting the buffer variables 
        del directory_list
        del file_buffer
        
    def _calc_description_author(self):
        """
        calculates the description of the documented file and writes it into
        the "self.description" variable.
        if there is none, writes an empty string.
        calculates the author of the file and writes it into the "self.author"
        if there is none, writes an empty string.
        ###
        RETURNS (void)
        """
        cond_sepa = False
        cond_docu = False
        # searching for the separation condition within the first docustring
        for line_index in range(0, len(self._linelist)):
            # checking wether inside a docustring or not
            if self._linelist_nowhite[line_index] == '"""' and cond_docu == False:
                cond_docu = True
            elif self._linelist_nowhite[line_index] == '"""' and cond_docu == True:
                cond_docu = False
                break
            # defining the author string
            if cut(self._linelist_nowhite[line_index],0,7) == "@author:" and cond_docu == True and cond_sepa == False:
                self.author = cut(self._linelist_nowhite[line_index],8,len(self._linelist_nowhite[line_index]) - 1)
            # adding to the description variable
            if cond_sepa and cond_docu:
                if self.description == "":
                    self.description += self._linelist[line_index]
                else:
                    self.description += "\n" + self._linelist[line_index]
            # checking for the separation condition
            if cond_docu == True and self._linelist_nowhite[line_index] == "###":
                cond_sepa = True
        
    def _calc_imports(self):
        """
        calculates the imported packages and puts their names as strings
        into the local list variable "self.imports"
        ###
        RETURNS (void)
        """
        cond_docu = False
        # searches for the keywords "import" and "from"
        for line_index in range(0, len(self._linelist)):
            # checking wether inside a docustring or not
            if self._linelist_nowhite[line_index] == '"""' and cond_docu == False:
                cond_docu = True
            elif self._linelist_nowhite[line_index] == '"""' and cond_docu == True:
                cond_docu = False
            # checking for keywords
            if not(cond_docu) and cut(self._linelist[line_index],0,6) == "import ":
                self._last_import = line_index
                if " as " in self._linelist[line_index]:
                    self.imports.append(get_substring_between(self._linelist[line_index], "import ", " as").replace(" ",""))
                else:
                    self.imports.append(get_substring_between(self._linelist[line_index]+";", "import ", ";").replace(" ",""))
            if not(cond_docu) and cut(self._linelist[line_index],0,3) == "from":
                self._last_import = line_index                
                self.imports.append(get_substring_between(self._linelist[line_index], "from ", " import").replace(" ",""))
            
    def _calc_classes_functions(self):
        """
        calculates the functions and classes of the file and puts them as
        DocumentedMethod;DocumentedClass into the local list variables
        "self.classes" and "self.functions"
        ###
        RETURNS (void)
        """
        # since a file header is reqiuired for every file, removing the first docustring
        # to appear from the main loop range, as that would be the header
        start_index = 0    
        buffer = 0
        temp_string = ""
        for line_index in range(0,len(self._linelist)):
            temp_string = self._linelist[line_index]
            # breaking after the docustring is done
            if buffer == 2:
                start_index = line_index
                break
            if cut(temp_string,0,2) == '"""':
                buffer += 1
        if not(self.imports == []):
            start_index = self._last_import + 1
        # going for the main loop with the adjusted starting index
        # resetting the local variables for reuse
        buffer = ""
        # the type of string currently stored in the buffer
        b_type = ""
        docu_cond = 0
        temp_string = ""
        temp_nowhite = ""
        for line_index in range(start_index, len(self._linelist)):
            # creates the temporary strings for each iteration of the loop
            temp_string = self._linelist[line_index]
            temp_nowhite = temp_string.replace(" ","")
            # in case there is an unindented docustring 
            if temp_string[0:3] == '"""':
                # but only in case it is the opening docustring
                if docu_cond == 2:
                    docu_cond = 1
                else:
                    docu_cond += 1
                # in case it is the opening docustring and an not empty buffer
                if not(buffer == "") and docu_cond == 1:
                    if b_type == "f":
                        self.functions.append(DocumentedMethod(buffer))
                        buffer = temp_string+"\n"
                        b_type = "c"
                    elif b_type == "c":
                        self.classes.append(DocumentedClass(buffer))
                        buffer = temp_string+"\n"
                        b_type = "c"
                # changing the type of the buffer string to class aka "c"
                b_type = "c"
            # in case there is an unindented method deklaration
            elif temp_string[0:3] == "def":
                # in case there is no empty buffer
                if not(buffer == ""):
                    if b_type == "f":
                        self.functions.append(DocumentedMethod(buffer))
                        buffer = temp_string+"\n"
                        b_type = "f"
                    elif b_type == "c":
                        self.classes.append(DocumentedClass(buffer))
                        buffer = temp_string+"\n"
                        b_type = "f"
                # changing the type of the buffersting to function aka "f"
                b_type = "f"
            # if the line of the file isnt an empty line, adds the line to the buffer
            if not(temp_nowhite == ""):
                if buffer == "":
                    buffer += temp_string
                else:
                    buffer += "\n"+temp_string
        # processing the buffer string wich has been left over 
        if not(buffer == ""):
            if b_type == "f":
                self.functions.append(DocumentedMethod(buffer))
            elif b_type == "c":
                self.classes.append(DocumentedClass(buffer))
        del temp_string
        del buffer
        # creating the dictionaries _functions and _classes
        for class_obj in self.classes:
            self._classes[class_obj.get_name()] = class_obj
        for function_obj in self.functions:
            self._functions[function_obj.get_name()] = function_obj
        
        
        
        
"""
A class representing a stored source code structure of JTDocumentation package, providing information
about the files within the pacakge itself, the description within the '__init__.py' file 
and a recursive list of subdirectories and their python files. This class also 
provides functions to create a predefined layout in latex source code.
###
directorypath - (string) the filepath of the package to be documented
"""  
class DocumentedPackage():
    """
    name - (string) the name of the package
    path - (string) the absolute path of the directory/package
    description - (string) the description of the package, which was put into
                           the docustring within the "__init__.py" of the package
    pyfiles - (list/DocumentedFile) the list of the DocumentedFile objects
                                    of all executable ".py" files in the package
    subpackages - (list/DocumentedPackage) the list of all sub directories in the
                                           package and their coresponding objects 
    _filelist - (list/string) a list with filenames inside the directory
    """
    def __init__(self, directorypath):
        # setting up the local variabls
        self.path = directorypath
        self._filelist = []
        self.description = ""
        self.pyfiles = []
        self.subpackages = []
        self.name = ""
        # creating the list of files in the dircecotry
        self._filelist = os.listdir(self.path)
        # calculating the name of the package
        self._calc_name()
        # calculating the files in the package
        self._calc_pyfiles()
        # calculating the subpackages in the package
        self._calc_subpackages()
        # calculating the description of the package 
        self._calc_description()
        
    def close(self):
        """
        is used to close all the files in the package and delete all variables. Has to be called
        at the end of each objects lifecycle, although the garbage collection
        should work with terminating said object calling this method seperatly
        is a safety messure
        ###
        RETURNS (void)
        """
        # closing all Documented type objects
        for item in self.pyfiles:
            item.close()
        for item in self.subpackages:
            item.close()
        # deleting the variables
        del self.description
        del self._filelist
        del self.pyfiles
        
    def get_latex(self, language, color_list, call_name):
        """
        creates and returns the string format of the file, which is used to create
        a latex Documentation of the module combining the latex strings of the python 
        files and the subpackages within the calling package.
        ###
        language - (string) the language of the important keywords/syntax
        color_list - (list\string) the list of the latex-basecolorstyle containing
                                   4 items describing the varoius colors from dark to light
        call_name - (string) as it is a rekursiv method, it needs the name of the parent
                             directory calling it
        ###
        RETURNS (string)
        """
        # creating the headline
        main_string = ""
        if not(call_name == ""):
            main_string += "\\section{\\textcolor{"+color_list[0]+"}{"+latex_compatible(call_name+"."+self.name)+"}}\n"
        else:
            main_string += "\\section{\\textcolor{"+color_list[0]+"}{"+latex_compatible(self.name)+"}}\n"
        # creating the description in case it isnt the toplevel package
        if not(call_name == ""):
            if language == "english":
                main_string += "\\textbf{Description, } "
            elif language == "german":
                main_string += "\\textbf{Beschreibung, } "
            main_string += latex_compatible(self.description)+"\\\\\n"
        # adding the file strings
        for file in self.pyfiles:
            if not(file.name == "__init__"):
                main_string += file.get_latex(language, color_list)                    
        # calling the subpackages recursive
        for package in self.subpackages:
            if not(package.name == "__pycache__"):
                if not(call_name == ""):
                    main_string += package.get_latex(language, color_list, call_name+"."+self.name)  
                else:
                    main_string += package.get_latex(language, color_list, self.name)  
        # returning the string
        return main_string+"\n"
                      
        
    def get_file(self, name):
        """
        returns the DocumentedFile object with the given name
        ###
        RETURNS (DocumentedFile)
        """        
        for item in self.pyfiles:
            if item.get_name() == name:
                return item
                
    def get_files(self):
        """
        returns the list of DocumentedFIle objects
        ###
        RETURNS (list/DocumentedFile)
        """
        return self.pyfiles
        
    def get_subdirs(self):
        """
        returns the list of DocumentedPackage objects
        ###
        RETURNS (list/DocumentedPackage)
        """
        return self.subpackages
                
    def get_subdir(self, name):
        """
        returns the DocumentedPackage object with the given name
        ###
        RETURNS (DocumentedPackage)
        """        
        for item in self.subpackages:
            if item.get_name() == name:
                return item  
                
    def get_name(self):
        """
        returns the name of the package
        ###
        RETURNS (string)
        """
        return self.name
        
    def get_path(self):
        """
        returns the path of the package
        ###
        RETURNS (string)
        """
        return self.path
        
    def get_description(self):
        """
        returns the description of the package. linebreakes included
        ###        
        RETURNS (string)
        """
        return self.description
        
        
    def _calc_subpackages(self):
        """
        calculates the subpackages within the package and saves them as
        DocumentedPackage objets into the local list "self.subpackages"
        ###
        RETURNS (void)
        """
        # going through the subfiles of the package and cheking for directory type
        for obj in self._filelist:
            if os.path.isdir(self.path+"\\"+obj):
                self.subpackages.append(DocumentedPackage(self.path+"\\"+obj))
    
    def _calc_pyfiles(self):
        """
        calculates the executable python files within the package and saves them as
        DocumentedFile objets into the local list "self.pyfiles"
        ###
        RETURNS (void)
        """
        # going through the subfiles of the package and seraching for file types
        temp_path = ""        
        for obj in self._filelist:
            temp_path = self.path+"\\"+obj
            if os.path.isfile(temp_path):
                if cut(temp_path, len(temp_path)-2, len(temp_path)) == "py":
                    self.pyfiles.append(DocumentedFile(temp_path))
                    
    def _calc_name(self):
        """
        caclulates the name of the package and puts it into the "self.name" variable
        ###
        RETURNS (void)
        """
        self.name = os.path.split(self.path)[1].replace("\\","")
        
    def _calc_description(self):
        """
        calculates the description written into the "__init__.py" file of the 
        package. Should be called after the "self.pyfiles" variable has been calculated
        ###
        RETURNS (void)
        """
        if "__init__.py" in self._filelist:
            self.description = self.get_file("__init__").get_description()
    

"""
The base class for Writing Documentations, acting like an abstract class or interface 
providing the further classes with the necessary base functions, like the option to 
save and base class variables.
###
packagepath - (string) the path of the directory to be documented
language - (string) either "english" or "german"
"""
class Documentation():
    """
    package - (DocumentedPackage) the object of the package/library to be documented
    docu_string - (string) the whole Documentation in string form with platform 
                           specific syntax and linebreaks already included
    colors_dict - (dict/string-list/string) the dictionary giving every color key
                                            a list of "xcolor"-latex color strings
                                            going from dark at the beginning to lighter
                                            at the end
    _packagepath - (string) the path of the directory
    _language - (string) either "english" or "german" mainly being responsible for
                         package usage to enable use of german vocals 
    _bascolor - (string) either "black","purple","green","red","blue" determining the
                         basecolorstyle of the document
    _directory - (JTCombinedOs.Directory) the Directory object of the specified
                                          program/library, managing the filepath
                                          operation of the documentation
    _email - (string) the email of the creator of the Documentation and most likely
                      the Library itself
    """
    colors_dict = {}
    def __init__(self, packagepath, colorstyle ,language, email, author):
        # setting up class variables
        self._packagepath = packagepath
        self._language = language
        self._basecolor = colorstyle
        self._email = email
        self._author = author
        self._directory = jtos.Directory(packagepath)
        self.package = DocumentedPackage(self._packagepath)
        self.docu_string = ""
        
    def save(self, filetype="txt"):
        """
        saves the "self.docu_string" mainstring into the main package/directory
        of the program
        ###
        savepath - (string) the path where the Documentation-file should
                            be saved in
        filetype - (string) the type of file that should be created 
        ###
        RETURNS (void)
        """
        if filetype == "txt":
            self._directory.create_file(self.package.get_name()+"_Documentation.txt", content=self.docu_string)
        elif filetype == "tex":
            self._directory.create_file(self.package.get_name()+"_Documentation.tex", content=self.docu_string)


"""
the class to create latex Documentation strings
###
packagepath - (string) the path of the directory to be documented
"""
class Latex_Documentation(Documentation):
    """
    package - (DocumentedPackage) the object of the package/library to be documented
    docu_string - (string) the whole Documentation in string form with platform 
                           specific syntax and linebreaks already included
    colors_dict - (dict/string-list/string) the dictionary giving every color key
                                            a list of "xcolor"-latex color strings
                                            going from dark at the beginning to lighter
                                            at the end
    _packagepath - (string) the path of the directory
    _language - (string) either "english" or "german" mainly being responsible for
                         package usage to enable use of german vocals 
    _bascolor - (string) either "black","purple","green","red","blue" determining the
                         basecolorstyle of the document
    _packagepath - (string) the path of the directory
    _colorlist - (list/string) the actual list of different "xcolor"-latex color strings
                               having 4 different color strings beginning with the
                               darkest and ending with the brightest
    _email - (string) the email of the creator of the Documentation and most likely
                      the Library itself
    """
    colors_dict = {"green":["black", "OliveGreen", "PineGreen", "LimeGreen"],
                   "blue":["black", "MidnightBlue", "NavyBlue", "ProcessBlue"],
                   "red":["black", "Brickred", "Red", "RedOrange"],
                   "purple":["RoyalPurple", "Plum", "Mulberry", "Orchid"],
                   "black":["black","black","black","black"]}
    def __init__(self, packagepath, language="english", colorstyle="green", email="not given", author="not given"):
        # setting up class variables
        Documentation.__init__(self, packagepath, colorstyle, language, email, author)
        self._colorlist = self.colors_dict[self._basecolor]
        # creating the document header and the package imports
        self._calc_documentheader()
        # creating the frontpage
        self._calc_frontpage()
        # creating the introduction
        self._calc_introduction()
        # creating the file hierarchy
        self._calc_filehierachy()
        # creating the actual content
        self._calc_content()
        
    def save(self, filetype="pdf"):
        """
        saves the "self.docu_string" mainstring into the file defined by the
        savepath-filepath
        ###
        savepath - (string) the path where the Documentation-file should
                            be saved in
        filetype - (string) the type of file that should be created 
        ###
        RETURNS (void)
        """
        Documentation.save(self, filetype)
        if filetype == "pdf":
            pdf, info = texcaller.convert(self.docu_string, "LaTeX", "PDF", 5)
            print("### LATEX TO PDF CONVERSION INFORMATIONS ###\n"+info)
            self._directory.create_file(self.package.get_name()+"_Documentation.pdf", content=pdf)
        
    def _calc_documentheader(self):
        """
        adds the following latex packages to the final file: amsmath, amssymb, geometry,
        setspace, booktabs, float, xcolor, graphix, and optionaly the packages required for
        different languages. Sets the textdistance to 1.5 and begins the document
        ###
        RETURNS (void)
        """
        # creates the document header of the latex file
        self.docu_string += "% documentheader %\n"
        self.docu_string += "\\documentclass[a4paper,12pt,fleqn]{article}\n"
        # creates the imports of the latex file
        self.docu_string += "% package imports %\n"
        self.docu_string += "\\usepackage{amsmath}\n"
        self.docu_string += "\\usepackage{amssymb}\n"
        self.docu_string += "\\usepackage{geometry}\n"
        self.docu_string += "\\usepackage{setspace}\n"
        self.docu_string += "\\usepackage{booktabs}\n"
        self.docu_string += "\\usepackage{float}\n"
        self.docu_string += "\\usepackage[usenames,dvipsnames]{xcolor}\n"
        self.docu_string += "\\usepackage{graphicx}\n\n"
        if self._language == "german":
            self.docu_string += "\\usepackage[ngerman]{babel}\n"
            self.docu_string += "\\usepackage[ansinew]{inputenc}\n\n"
        # creates the geometry option of the document
        self.docu_string += "% geometry settings %\n"
        self.docu_string += "\\geometry{verbose,a4paper,tmargin=25mm,bmargin=25mm,lmargin=15mm,rmargin=15mm}\n"
        self.docu_string += "\\setstretch{1.433} % in percent\n\n"
        # creates the beginning tag of the actual document
        self.docu_string += "% opening the document %\n"
        self.docu_string += "\\begin{document}\n"
        
    def _calc_frontpage(self):
        """
        adds an acedamic styled frontpage with colored accents to the Document, 
        including informations about the date of creation, the name of the author 
        and the email of the creator.
        ###
        RETURNS (void)
        """
        self.docu_string += "\\vspace*{80mm}\n"
        # creating the caption
        self.docu_string += "\\begin{center}\n\\begin{Huge}\n"
        if self._language == "english":
            self.docu_string += "\\sf \\textcolor{"+self._colorlist[0]+"}{Python Documentation}\\footnotetext[0]{Documentation provided and created by JTDocumentationTool}\\\\\n"
        elif self._language == "german":
            self.docu_string += "\\sf \\textcolor{"+self._colorlist[0]+"}{Python Dokumentation}\\footnotetext[0]{Dokumentation erstellt durch das JTDocumentation Werkzeug}\\\\\n"
        self.docu_string += "\\end{Huge}\n\\begin{large}\n"
        # creating the subcaption
        self.docu_string += "\\sf \\textcolor{"+self._colorlist[1]+"}{"+self.package.get_name()+"}\\\\[9cm]\n"
        self.docu_string += "\\end{large}\n\\end{center}\n"
        self.docu_string += "\\begin{flushleft}\n\\begin{large}\n"
        # creating the details 
        if self._language == "english":
            self.docu_string += "Details of Creation\\\\\n"
            self.docu_string += "Date: "+time.asctime()+"\\\\\n"
            self.docu_string += "Author: "+self._author+"\\\\\n"
            self.docu_string += "E-Mail: "+self._email+"\\\\\n"
        elif self._language == "german":
            self.docu_string += "Erstellungsdetails\\\\\n"
            self.docu_string += "Datum: "+time.asctime()+"\\\\\n"
            self.docu_string += "Autor: "+self._author+"\\\\\n"
            self.docu_string += "E-Mail: "+self._email+"\\\\\n"
        self.docu_string += "\end{large}\n\end{flushleft}\n"
        self.docu_string += "\\newpage\n"
        
    def _calc_introduction(self):
        """
        adds the table of contents and the introduction with the description of the
        upper layer package to the document of the 
        package/progarm/library to the mainstring
        ###
        RETURNS (void)
        """
        # creating the table of contents
        self.docu_string += "\\tableofcontents\n\\newpage\n"
        # creating the headline with the darkest color in the _colorlist
        if self._language == "english":
            self.docu_string += "\n\\section{\\textcolor{"+self._colorlist[0]+"}{Introduction}}\n"
        elif self._language == "german":
            self.docu_string += "\n\\section{\\textcolor{"+self._colorlist[0]+"}{Einleitung}}\n"
        # inserting the description of the main package
        self.docu_string += latex_compatible(self.package.get_description())
        self.docu_string += "\\newpage\n"
        
    def _calc_filehierachy(self):
        """
        creates an hierachy of files and subpackages as an local variable and writes
        it on a separate page to the latex document string.
        recommended to call after the creation of the introduction as it creates
        no main headline, but a subheadline
        ###
        RETURNS (void)
        """
        # adds the subheadline to the document 
        if self._language == "english":
            self.docu_string += "\n\\subsection{\\textcolor{"+self._colorlist[1]+"}{File Hierarchy}}\n"
        elif self._language == "german":
            self.docu_string += "\n\\subsection{\\textcolor{"+self._colorlist[1]+"}{Datei Hierarchie}}\n"
        # adds the actual hierachy to the string
        self.docu_string += self._directory.get_hierarchy_latex()
        self.docu_string += "\\setstretch{1.433}\n"
        self.docu_string += "\\newpage\n"
        
    def _calc_content(self):
        """
        creates the actual content by calling the 'get_latex()' function of the
        top level pakage/library
        ###
        RETURNS (void)
        """
        self.docu_string += self.package.get_latex(self._language, self._colorlist, "")+"\n"
        self.docu_string += "\\end{document}\n"

        
                