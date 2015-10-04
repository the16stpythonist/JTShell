# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 18:33:02 2015
@author: Jonas
###
A module providing functions to ease the handling of python string manipulation 
expanding the wide variaty of base python functions with less general, but more 
specific fucntionalities.
"""
import os


def cut(string, index_start, index_end):
    """
    a function to provide better functionality than the standard python index
    based string slicing. implenting the start and end index to be both included
    at the same time although making the usage of the len() function in combination 
    with the index slicing more difficult.
    ###
    string - (string) the main string to be sliced
    index_start - (int) the index to start at
    index_end -   (int) the index to end at
    ###
    RETURNS (string)
    """
    return string[index_start:index_end + 1]
    

def divide_by_custom(string, custom):
    """
    Divides the main string "string" into a list of substrings, wheres the
    the substrings are divided by the custom string break, whereas the custom string
    will not appear in the list, onlyfunctionaing as separation
    ###
    string - (string) the mainstring to be divided into substrings
    custom - (string) the string to be used as break condition 
    ###
    RETURNS (list/string)
    """
    # checking for the length of the custom string
    if len(string) >= 1:
        if len(custom) == 1:
            # enabeling the last substring                
            if str(string[-1]) != custom:
                nstring = string + custom
            else:
                nstring = string
            # creating the list to return
            dividedlist = []
            # looping through the mainstring and searching for the break condition
            tempstring = ""
            for character in nstring:
                # break -> add substring to the list
                if str(character) == custom:
                    dividedlist.append(tempstring)
                    tempstring = ""
                else:
                    tempstring += character
            # returning the list
            return dividedlist
        
        else:
            # the procedere for longer strings
            # checking if it is even necessary to search for the substring
            if custom in string:
                tempstring = ""
                dividedlist = []
                # replacing the custom string with a single charcter, that is very
                # unlikely to appear "°"
                mstring = string.replace(custom, "°")
                for character in mstring:
                    # break -> add substring to the list
                    if str(character) == "°":
                        dividedlist.append(tempstring)
                        tempstring = ""
                    else:
                        tempstring += character
                dividedlist.append(tempstring)
                return dividedlist


def divide_by_whitespace(string):
    """
    An extended call of the 'divide_by_custom' function in the same module, dividing
    the given string by whitespace in between the characters
    ###
    string - (string) the main string to be divided into substrings
    ###
    RETURNS (list/string)
    """     
    # calls the divide_by_custom method, with custom=" "
    return divide_by_custom(string, " ")
    
    
def get_substring_before(mainstring, before):
    """
    returns the substring before the first occurance of the given
    substring "before"
    ###
    mainstring - (string) the string to be searched in
    before - (string) the break condition for the search
    ###
    RETURNS (string)    
    """
    # checking if the breakcondition is even in there 
    if before in mainstring:
        return mainstring[0:mainstring.find(before)]
    else:
        return mainstring
    
def get_sublist_between(mainlist, item_start, item_end, ind_start=0, whitespace=True):
    """
    returns the sublist in bewteen the two given items
    ###
    mainlist - (list/?) the list from which the sublist is going to be extracted
    item_start - (?) the item, where to start the sublist
    item_end - (?) the item, where to end the sublist
    ind_start (int|default=0) the index, where to start the search
    whitespace - (bool|default=True) only for string lists!
                                     wether whitespace should be acounted or not
    ###
    RETURNS (list/?) 
    """
    if whitespace == False and type(mainlist[0]) is str:
        nowhite_list = []
        for item in mainlist:
            nowhite_list.append(item.replace(" ",""))
        return cut(mainlist, nowhite_list.index(item_start, ind_start) + 1, nowhite_list.index(item_end, nowhite_list.index(item_start, ind_start) + 1) - 1)
    else:
        return cut(mainlist, mainlist.index(item_start,ind_start) + 1, mainlist.index(item_end, mainlist.index(item_start,ind_start) + 1) - 1)
        
    
    
    
def get_substring_between(mainstring, str_start, str_end):
    """
    returns the substring in between the two given substrings, but only considering
    the first appearance of both break conditions
    ###
    mainstring - (string) the string to search in 
    str_start  - (string) the string at which to start
    str_end    - (string) the string at which to end
    ###
    RETURNS (string)
    """
    return cut(mainstring, mainstring.find(str_start) + 1 + len(str_start) - 1, mainstring.find(str_end, mainstring.find(str_start) + 1) - 1)
    
    
def round_down(floatnum):
    """
    returns the integer of the given float, but always rounds down. 
    Shouldnt be called, as this is a ineffektiv solution and can easily attract
    Exceptions.
    ###
    floatnum - (float),(double) the number to be rounded
    ###
    RETURNS (int)
    """
    return int(get_substring_before(str(floatnum), "."))
    
def remove_indendation(mainstring):
    """
    returns the string given without the indendation in front
    ###
    mainstring - (string) the string the function should be used on
    ###
    RETURNS (string)
    """
    # determining the indendation of the string and removing it
    return mainstring.replace(get_indendation(mainstring), "")
        
    
def get_indendation(mainstring):
    """
    returns the indendation in front of the string
    ###
    mainstring - (string) the string the function should be used on
    ###
    RETURNS (string)
    """
    # getting the whitespaces in front of the string and breaking, when the first
    # character appears
    indent_string = ""
    for character in mainstring:
        if character == " ":
            indent_string += character
        else:
            break
    # returning the calculated value
    return indent_string
    
def latex_compatible(string):
    """
    makes the given string parameter compatible for latex use, mainly replacing
    line breaks with latex linebreak tags
    ###
    string - (string) the string to be converted
    ###
    RETURNS (string)
    """
    temp_string = string
    temp_string = temp_string.replace("\n\n", "\\\\\n")
    temp_string = temp_string.replace("_","\\_")
    temp_string = temp_string.replace("%","\\%")
    temp_string = temp_string.replace("$","\\$")
    temp_string = temp_string.replace("&","\\&")
    temp_string = temp_string.replace("#","\\#")
    # returning the resulting string
    return temp_string
    
def count_chars(string, char):
    """
    counts the number of appearances of the given character inside the given 
    main string
    ###
    string - (string) the main string to search in
    char - (string) the character to count
    ###
    RETURNS (int)
    """
    amount = 0
    for substr in string:
        if substr == char:
            amount += 1
    # returning the counted amount
    return amount
    

    
            
                
