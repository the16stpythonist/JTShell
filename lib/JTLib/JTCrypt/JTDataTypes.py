# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 18:05:37 2015

@author: Jonas
"""
import JTLib.JTUtility.JTString as JTString


def identify_DataType(data):
    """
    analyzes the DataType of the given string "data"
    data - (string) the string to be analyzed
    ###
    RETURNS (string)
    """
    # at the beginning the given string could be of any type
    could_binary = True
    could_decimal = True
    could_hexa = True
    could_ascii = True
    # checking for conditions, that exclude the single data types
    for char in data:
        if char in "23456789":
            could_binary = False
        elif char in "aAbBcCdDeEfF":
            could_binary = False
            could_decimal = False
        elif char in "abBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ!%&()=?":
            could_binary = False
            could_decimal = False
            could_hexa = False
    # returning the data type, depending on which data type hasnt been excluded      
    if could_binary:
        return "Binary"
    elif could_decimal:
        return "Decimal"
    elif could_hexa:
        return "Hexadecimal"
    elif could_ascii:
        return "Ascii"
        
        
def decim(value):
    """
    Converts multiple methods of inputs into an Object of the type DecimalArray
    ###    
    value - (int) the integer, which is to be converted into a DecimalArray object
                  with a single item
            (str) in case there are no whitespaces the string will be checked
                  for the inherited DataType, which will then be converted to Decimal,
                  in case of whitespaces the substring will be divided and convertded
                  individually, causing multiple items in the DecimalArray
            (DataTypeArray) a DataTypeArray containing other DataTypes will be converted into
                            a DecimalArray
            (list) a list containing either strings, integers, or DataType objects
                   can also be converted into DecimalArray, whereas it is important,
                   that all items are of the same type
    ###           
    RETURNS (DecimalArray)
    """
    # checking for parameter type
    if type(value) is int:
        return DecimalArray([value])  
    elif type(value) is str:
        # identifying the type of the data described by the string
        val_datatype = identify_DataType(value)
        if not(" " in value):
            if val_datatype == "Binary":
                return DecimalArray([Binary(value)])
            elif val_datatype == "Decimal":
                return DecimalArray([value])
            elif val_datatype == "Hexadecimal":
                return DecimalArray([Hexadecimal(value)])
            elif val_datatype == "Ascii":
                return DecimalArray([Ascii(value)])
        else:
            if val_datatype == "Binary":
                return DecimalArray(BinaryArray(value))
            elif val_datatype == "Decimal":
                return DecimalArray(value)
            elif val_datatype == "Hexadecimal":
                return DecimalArray(HexadecimalArray(value))
            elif val_datatype == "Ascii":
                return DecimalArray(AsciiArray(value))
    elif type(value) is list:
        # assuming every item of the list belongs to the same type,
        # because checking each would be highly inefficient
        if type(value[1]) is str:
            new_string = ""
            for substring in value:
                new_string += substring
                new_string += " "
            str_type = identify_DataType(value)
            if str_type == "Binary":
                return DecimalArray(BinaryArray(value))
            elif str_type == "Decimal":
                return DecimalArray(value)
            elif str_type == "Hexadecimal":
                return DecimalArray(HexadecimalArray(value))
            elif str_type == "Ascii":
                return DecimalArray(AsciiArray(value))
        elif type(value[1]) is int:
            return DecimalArray(value)
        elif isinstance(value[1], DataType):
            return DecimalArray(value)
    elif isinstance(value, DataTypeArray):
        return DecimalArray(value)
          
          
def hexa(value):
    """
    Converts multiple methods of inputs into an Object of the type HexadecimalArray
    ###
    value - (int) the integer, which is to be converted into a HecadecimalArray object
                  with a single item
            (str) in case there are no whitespaces the string will be checked
                  for the inherited DataType, which will then be converted to Hexadecimal,
                  in case of whitespaces the substring will be divided and convertded
                  individually, causing multiple items in the HexadecimalArray
            (DataTypeArray) a DataTypeArray containing other DataTypes will be converted into
                            a HexadecimalArray
            (list) a list containing either strings, integers, or DataType objects
                   can also be converted into DecimalArray, whereas it is important,
                   that all items are of the same type
    ###          
    RETURNS (hexadecimalArray)
    """
    # checking for parameter type
    if type(value) is int:
        return Hexadecimal(value)  
    elif type(value) is str:
        # identifying the type of the data described by the string
        val_datatype = identify_DataType(value)
        if not(" " in value):
            if val_datatype == "Binary":
                return HexadecimalArray([Binary(value)])
            elif val_datatype == "Decimal":
                return HexadecimalArray([Decimal(value)])
            elif val_datatype == "Hexadecimal":
                return HexadecimalArray([value])
            elif val_datatype == "Ascii":
                return HexadecimalArray([Ascii(value)])
        else:
            if val_datatype == "Binary":
                return HexadecimalArray(BinaryArray(value))
            elif val_datatype == "Decimal":
                return HexadecimalArray(DecimalArray(value))
            elif val_datatype == "Hexadecimal":
                return HexadecimalArray(value)
            elif val_datatype == "Ascii":
                return HexadecimalArray(AsciiArray(value))
    elif type(value) is list:
        # assuming every item of the list belongs to the same type,
        # because checking each would be highly inefficient
        if type(value[1]) is str:
            new_string = ""
            for substring in value:
                new_string += substring
                new_string += " "
            str_type = identify_DataType(value)
            if str_type == "Binary":
                return HexadecimalArray(BinaryArray(value))
            elif str_type == "Decimal":
                return HexadecimalArray(DecimalArray(value))
            elif str_type == "Hexadecimal":
                return HexadecimalArray(value)
            elif str_type == "Ascii":
                return HexadecimalArray(AsciiArray(value))
        elif type(value[1]) is int:
            return HexadecimalArray(value)
        elif isinstance(value[1], DataType):
            return HexadecimalArray(value)
    elif isinstance(value, DataTypeArray):
        return HexadecimalArray(value)            
                

def binar(value):
    """
    Converts multiple methods of inputs into an Object of the type BinaryArray
    ###    
    value - (int) the integer, which is to be converted into a BinaryArray object
                  with a single item
            (str) in case there are no whitespaces the string will be checked
                  for the inherited DataType, which will then be converted to Binary,
                  in case of whitespaces the substring will be divided and convertded
                  individually, causing multiple items in the BinaryArray
            (DataTypeArray) a DataTypeArray containing other DataTypes will be converted into
                            a BinaryArray
            (list) a list containing either strings, integers, or DataType objects
                   can also be converted into DecimalArray, whereas it is important,
                   that all items are of the same type
    ###             
    RETURNS (BinaryArray)
    """
    # checking for parameter type
    if type(value) is int:
        return BinaryArray([value])  
    elif type(value) is str:
        # identifying the type of the data described by the string
        val_datatype = identify_DataType(value)
        if not(" " in value):
            if val_datatype == "Binary":
                return BinaryArray([value])
            elif val_datatype == "Decimal":
                return BinaryArray([Decimal(value)])
            elif val_datatype == "Hexadecimal":
                return BinaryArray([Hexadecimal(value)])
            elif val_datatype == "Ascii":
                return BinaryArray([Ascii(value)])
        else:
            if val_datatype == "Binary":
                return BinaryArray(value)
            elif val_datatype == "Decimal":
                return BinaryArray(DecimalArray(value))
            elif val_datatype == "Hexadecimal":
                return BinaryArray(HexadecimalArray(value))
            elif val_datatype == "Ascii":
                return BinaryArray(AsciiArray(value))
    elif type(value) is list:
        # assuming every item of the list belongs to the same type,
        # because checking each would be highly inefficient
        if type(value[1]) is str:
            new_string = ""
            for substring in value:
                new_string += substring
                new_string += " "
            str_type = identify_DataType(value)
            if str_type == "Binary":
                return BinaryArray(value)
            elif str_type == "Decimal":
                return BinaryArray(DecimalArray(value))
            elif str_type == "Hexadecimal":
                return BinaryArray(HexadecimalArray(value))
            elif str_type == "Ascii":
                return BinaryArray(AsciiArray(value))
        elif type(value[1]) is int:
            return BinaryArray(value)
        elif isinstance(value[1], DataType):
            return BinaryArray(value)
    elif isinstance(value, DataTypeArray):
        return BinaryArray(value)
        
        
def asci2(value):
    """
    Converts multiple methods of inputs into an Object of the type AsciiArray
    ###    
    value - (int) the integer, which is to be converted into a AsciiArray object
                  with a single item
            (str) in case there are no whitespaces the string will be checked
                  for the inherited DataType, which will then be converted to Ascii,
                  in case of whitespaces the substring will be divided and convertded
                  individually, causing multiple items in the AsciiArray
            (DataTypeArray)
                  a DataTypeArray containing other DataTypes will be converted into
                  a AsciiArray
            (list)a list containing either strings, integers, or DataType objects
                  can also be converted into AsciiArray, whereas it is important,
                  that all items are of the same type
    ###              
    RETURNS (AsciiArray)
    """
    # checking for parameter type
    if type(value) is int:
        return AsciiArray([value])  
    elif type(value) is str:
        # identifying the type of the data described by the string
        val_datatype = identify_DataType(value)
        if not(" " in value):
            if val_datatype == "Binary":
                return AsciiArray([Binary(value)])
            elif val_datatype == "Decimal":
                return AsciiArray([Decimal(value)])
            elif val_datatype == "Hexadecimal":
                return AsciiArray([Hexadecimal(value)])
            elif val_datatype == "Ascii":
                return AsciiArray([value])
        else:
            if val_datatype == "Binary":
                return AsciiArray(BinaryArray(value))
            elif val_datatype == "Decimal":
                return AsciiArray(DecimalArray(value))
            elif val_datatype == "Hexadecimal":
                return AsciiArray(HexadecimalArray(value))
            elif val_datatype == "Ascii":
                return AsciiArray(value)
    elif type(value) is list:
        # assuming every item of the list belongs to the same type,
        # because checking each would be highly inefficient
        if type(value[1]) is str:
            new_string = ""
            for substring in value:
                new_string += substring
                new_string += " "
            str_type = identify_DataType(value)
            if str_type == "Binary":
                return AsciiArray(BinaryArray(value))
            elif str_type == "Decimal":
                return AsciiArray(Decimal(value))
            elif str_type == "Hexadecimal":
                return AsciiArray(HexadecimalArray(value))
            elif str_type == "Ascii":
                return AsciiArray(value)
        elif type(value[1]) is int:
            return AsciiArray(value)
        elif isinstance(value[1], DataType):
            return AsciiArray(value)
    elif isinstance(value, DataTypeArray):
        return AsciiArray(value)


"""
a class, which resembles the abstract base class for any data type
"""
class DataType():
    """
    stringvalue - (string) the string format of the given Datatype
    decimalvalue - (int) a list containing the decimal equivalents of the 
                         single substrings of data within the stringvalue
    """
    def __init__(self):
        # setting up the 
        self.stringvalue = ""
        self.decimalvalue = 0
        
    def get_decimalvalue(self):
        """
        returning the decimalvalue
        ###
        RETURNS (int)
        """
        return self.decimalvalue
        
    def get_string(self):
        """
        returning the string of the value
        ###
        RETURNS (string)
        """
        return self.stringvalue
    
    

"""
a class, representing a ascii datatype
###
value - (string) must be one character ascii string
        (int) only a few decimlas can actually be converted to ascii
        (DataType) the type of data to be converted to ascii
"""
class Ascii(DataType):
    """
    stringvalue - (string) the string format of the given Datatype
    decimalvalue - (int) a list containing the decimal equivalents of the 
                         single substrings of data within the stringvalue
    """
    def __init__(self, value):
        # initializing the super constructor
        DataType.__init__(self)
        # checking the Type of the parameter
        if type(value) is int:
            self.decimalvalue = value
            self.stringvalue = chr(value)
        elif type(value) is str:
            if len(value) == 1:
                self.decimalvalue = ord(value)
                self.stringvalue = value
        elif isinstance(value, DataType):
            self.decimalvalue = value.decimalvalue
            self.stringvalue = ord(self.decimalvalue)
        


"""
a class, representing a decimal datatype
###
value - (string) the string of an integer, strings of other DataTypes wont be accepted
        (int) the integer to be represented as Decimal object
        (DataType) the DataType object to be converted to decimal
"""
class Decimal(DataType):
    """
    stringvalue - (string) the string format of the given Datatype
    decimalvalue - (int) a list containing the decimal equivalents of the 
                              single substrings of data within the stringvalue
    """
    def __init__(self, value):
        # initializing the super constructor
        DataType.__init__(self)
        # checking the Type of the parameter
        if type(value) is int:
            self.decimalvalue = value
            
        elif type(value) is str:
            self.decimalvalue = int(value)
                    
        elif isinstance(value, DataType):
            self.decimalvalue = value.decimalvalue
        # creating the stringvalue
        self.__calcstringvalue()
        
        
    def __calcstringvalue(self):
        """
        Creating the stringvalue attribute with the data given within the
        decimalvalue attribute
        ###
        RETURNS (void)
        """
        #creates a string with the decimal value
        self.stringvalue = str(self.decimalvalue)
        

            
"""
a class, representing a hexadecimal datatype
###
value - (string) the string of a hexadecimal number, other DataTypes arent accpeted
        (int) the number to be converted into the HexaDecimal object
        (DataType) the type of data to be converted to hexadecimal
"""
class Hexadecimal(DataType):
    """
    stringvalue - (string) the string format of the given Datatype
    decimalvalue - (int) a list containing the decimal equivalents of the 
                              single substrings of data within the string
    """ 
    h_to_d = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7,
              "8":8, "9":9, "A":10, "B":11, "C":12, "D":13, "E":14, "F":15,
              "a":10, "b":11, "c":12, "d":13, "e":14, "f":15}
    d_to_h = {0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7",
              8:"8", 9:"9", 10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
              
    def __init__(self, value):
        # initializing the super constructor
        DataType.__init__(self)
        # checking the type of the parameter
        if type(value) is str:
            temp_value = value
            if "0x" in temp_value:
                temp_value = temp_value.replace("0x","")
            if "\\x" in temp_value:
                temp_value = temp_value.replace("\\x","")
            self.stringvalue = temp_value
            self.decimalvalue = self.__calcdecimal(temp_value)
        elif type(value) is int:
            self.stringvalue = self.__calchexa(value)
            self.decimalvalue = value
        elif isinstance(value, DataType):
            self.stringvalue = self.__calchexa(value.decimalvalue)
            self.decimalvalue = value.decimalvalue
        
            
    def __calcdecimal(self, hexa):
        """
        converts the given string "hexa", inheriting a hexadecimal data type,
        into a decimal integer type
        ###
        hexa - (string) the string format of the hexadecimal data 
        ###
        RETURNS (int)
        """
        new_decimal = 0
        index = len(hexa)-1
        for character in hexa:
            new_decimal += Hexadecimal.h_to_d[character]*(pow(16, index))
            index -= 1
        # returning the new decimal value
        return new_decimal
        
    def __calchexa(self, decimal):
        """
        converts the given integer "decimal" into a string, inheriting
        hecadecimal type data
        ###
        decimal - (int) the decimal value
        ###
        RETURNS (string)
        """
        new_hexa = ""
        leftover = 0
        temp_value = decimal
        while temp_value != 0:
            # updating the temporary data
            leftover = temp_value % 16
            temp_value = JTString.round_down(temp_value / 16)
            # creating the hexadecimal digits
            new_hexa = Hexadecimal.d_to_h[leftover] + new_hexa
        # returning the new hexadecimal value
        return new_hexa
    
        
"""
a class, representing a binary datatype
###
value - (string) the string of a Binary, only allowed to consist of 1 and 0
        (int) the decimal value to be converted into binary
        (DataType) the type of data to be converted to binary
"""
class Binary(DataType):
    """
    stringvalue - (string) the string format of the given Datatype
    decimalvalue - (int) a list containing the decimal equivalents of the 
                              single substrings of data within the string
    """         
    def __init__(self, value):
        # initializing the super constructor
        DataType.__init__(self)
        # checking the Type of the parameter
        if type(value) is str:
            self.stringvalue = value
            self.decimalvalue = self.__calcdecimal(value)
        elif type(value) is int:
            self.stringvalue = self.__calcbinary(value)
            self.decimalvalue = value
        elif isinstance(value, DataType):
            self.stringvalue = self.__calcbinary(value.decimalvalue)
            self.decimalvalue = value.decimalvalue
            
        
    def __calcdecimal(self, binary):
        """
        converts the given string "binary", inheriting a hexadecimal data type,
        into a decimal integer type
        ###
        binary - (string) the string format of the binary data  
        ###
        RETURNS (int)
        """
        new_decimal = 0
        index = len(binary) - 1
        for digit in binary:
            new_decimal += int(digit) * (2**index)
            index -= 1
        return new_decimal
        
    def __calcbinary(self, decimal):
        """
        converts the given integer "decimal" into a string, inheriting
        binary type data
        ###
        decimal - (int) the decimal value
        ###
        RETURNS (string)
        """
        new_binary = ""
        leftover = 0
        temp_value = decimal
        while temp_value != 0:
            # updating the temporary data
            leftover = temp_value % 2
            temp_value = JTString.round_down(temp_value / 2)
            # creating the binary digits
            new_binary = str(leftover) + new_binary
        # returning the new binary value
        return new_binary
        
    def invert(self):
        """
        inverts the data, meaning replacing all 1 with 0 and therefor also replacing
        all 0 with 1
        ###
        RETURNS (void)
        """
        new_string = self.stringvalue.replace("1","#")
        new_string = new_string.replace("0","1")
        new_string = new_string.replace("#", "0")
        self.stringvalue = new_string
        self.__calcdecimal(self.stringvalue)
 
"""
a abstract base class for accumilations of data types such as lists
"""       
class DataTypeArray():
    """
    decimalarray - (list/int) a list with the decimal value of the data
    stringvalue - (string) the string format of the whole thing
    valuearray - (list/DataType) a list of the individual data
    stringarray - (list/string) a list of the string format of each ind. data
    """
    def __init__(self):
        self.valuearray = []
        self.stringvalue = ""
        self.decimalarray = []
        self.stringarray = []
        
    def _calcstringvalue(self):
        """
        creates the string of the object with the existing data of the string array
        ###        
        RETURNS (void)
        """
        for substring in self.stringarray:
            self.stringvalue += substring
            self.stringvalue += " "
            
    def get_valuelist(self):
        """
        returns a list containing the objects of the specific DataType
        ###        
        RETURNS (list/DataType)
        """
        return self.valuearray
        
    def get_decimallist(self):
        """
        returns a list of the integer values of the individual DataType
        ###        
        RETURNS (list/int)
        """
        return self.decimalarray
        
    def get_stringlist(self):
        """
        retuns a list of the string format of the individual DataType 
        ###        
        RETURNS (list/string)
        """
        return self.stringarray
        
    def get_string(self):
        """
        returns a atring of the data cluster, where every piece of data is
        seperated by a whitespace
        ###        
        RETURNS (string)        
        """
        return self.stringvalue
        
    def get_value(self, index, typ="value"):
        """
        returns a specific value at the position of the given "index"
        the type of list at which this value is gotten from is dependant of the
        "typ" given.
        ###
        index - (int) the index to get the value from
        typ - (string): value    = gets the instance of the DataType object
                        decimal  = gets the decimal value of the listed item
                        string   = gets the string value of the listed item
        ###                
        RETURNS (DataType),(string),(int)
        """
        # checking for wich type of list is requested to get from
        if (typ == "value" or typ == "val"):
            return self.valuearray[index]
        elif (typ == "decimal" or typ == "int" or typ == "integer"):
            return self.decimalarray[index]
        elif (typ == "string" or typ == "str"):
            return self.stringarray[index]
            
"""
a class representing a cluster/array of decimal values
###
value - (string) a single string to be converted as the oonly item in the array
        (list/int) a list of decimal inregers ti convert
        (list/DataType) a list of other DataTypes to convert based in their decimal
                        equivalents
        (DataTypeArray) the cluster of Data 
"""
class DecimalArray(DataTypeArray):
    """
    decimalarray - (list/int) a list with the decimal value of the data
    stringvalue - (string) the string format of the whole thing
    valuearray - (list/DataType) a list of the individual data
    stringarray - (list/string) a list of the string format of each ind. data
    """
    def __init__(self, value):
        # Initializing the super constructor
        DataTypeArray.__init__(self)
        # checking the type of the parameter
        
        # value is string
        if type(value) is str:
            temp_list = JTString.divide_by_whitespace(value)
            for substring in temp_list:
                self.stringarray.append(substring)
                self.decimalarray.append(int(substring))
                self.valuearray.append(Decimal(substring))
        
        # value is list
        elif type(value) is list:
            # list consists of integers
            if type(value[0]) is int:
                for subvalue in value:
                    self.stringarray.append(str(subvalue))
                    self.decimalarray.append(subvalue)
                    self.valuearray.append(Decimal(value))
            # list consists of DataTypes
            elif isinstance(value[0], DataType):
                for datatype in value:
                    self.decimalarray.append(datatype.get_decimalvalue())
                for integer in self.decimalarray:
                    self.valuearray.append(Decimal(integer))
                    self.stringarray.append(str(integer))
        
        # value is DataType Array
        elif isinstance(value, DataTypeArray):
            self.decimalarray = value.decimalarray
            for integer in self.decimalarray:
                self.valuearray.append(Decimal(integer))
                self.stringarray.append(str(integer))
                
        # creating the stringvalue attribute
        self._calcstringvalue()

    def append(self, value):
        """
        Appends the given value to the array
        ###
        value - (int) the decimal format of the data type,
                (DataType) the object instance of the DataType to be added\converted
                (string) the string format of the DataType
        ###
        RETURNS (void)
        """
        # checking for the type
        if type(value) is str:
            self.decimalarray.append(int(value))
            self.valuearray.append(Decimal(value))
            self.stringarray.append(value)
        elif type(value) is int:
            self.decimalarray.append(value)
            self.valuearray.append(Decimal(value))
            self.stringarray.append(str(value))
        elif isinstance(value, DataType):
            self.decimalarray.append(value.get_decimalvalue())
            self.stringarray.append(value.get_string())
            self.valuearray.append(Decimal(value.get_decimalvalue()))
            
    def _calcstringvalue(self):
        """
        creates the string of the object with the existing data of the string array
        ###        
        RETURNS (void)
        """
        DataTypeArray._calcstringvalue(self)
        

"""
a class representing a cluster/array of hexadecimal values
###
value - (string) a single string to be converted as the oonly item in the array
        (list/int) a list of decimal inregers ti convert
        (list/DataType) a list of other DataTypes to convert based in their decimal
                        equivalents
        (DataTypeArray) the cluster of Data 
"""
class HexadecimalArray(DataTypeArray):
    """
    decimalarray - (list/int) a list with the decimal value of the data
    stringvalue - (string) the string format of the whole thing
    valuearray - (list/DataType) a list of the individual data
    stringarray - (list/string) a list of the string format of each ind. data
    """
    def __init__(self, value):
        # Initializing the super constructor
        DataTypeArray.__init__(self)
        # checking the type of the parameter
        
        # value is string
        if type(value) is str:
            temp_list = JTString.divide_by_whitespace(value)
            for substring in temp_list:
                self.valuearray.append(Hexadecimal(substring))
            for subhexa in self.valuearray:
                self.decimalarray.append(subhexa.get_decimalvalue())
                self.stringarray.append(subhexa.get_string())
        
        # value is list
        elif type(value) is list:
            # list consists of integers
            if type(value[0]) is int:
                for subvalue in value:
                    self.decimalarray.append(subvalue)
                    self.valuearray.append(Hexadecimal(subvalue))
                for subhexa in self.valuearray:
                    self.stringarray.append(subhexa.get_string())
            # list consists of DataTypes
            elif isinstance(value[0], DataType):
                for datatype in value:
                    self.decimalarray.append(datatype.get_decimalvalue())
                for integer in self.decimalarray:
                    self.valuearray.append(Hexadecimal(integer))
                for subvalue in self.valuearray:
                    self.stringarray.append(subvalue.get_string())
        
        # value is DataType Array
        elif isinstance(value, DataTypeArray):
            self.decimalarray = value.decimalarray
            for integer in self.decimalarray:
                self.valuearray.append(Hexadecimal(integer))
            for subvalue in self.valuearray:
                self.stringarray.append(subvalue.get_string())
                
        # creating the stringvalue attribute
        self._calcstringvalue()
    
    def append(self, value):
        """
        Appends the given value to the array
        ###
        value - (int) the decimal format of the data type,
                (DataType) the object instance of the DataType to be added\converted
                (string) the string format of the DataType
        ###
        RETURNS (void)
        """
        # checking for the type
        if type(value) is str:
            self.valuearray.append(Hexadecimal(value))
            self.decimalarray.append(self.valuearray[-1].get_decimalvalue())
            self.stringarray.append(value)
        elif type(value) is int:
            self.decimalarray.append(value)
            self.valuearray.append(Hexadecimal(value))
            self.stringarray.append(str(value))
        elif isinstance(value, DataType):
            self.decimalarray.append(value.get_decimalvalue())
            self.stringarray.append(value.get_string())
            self.valuearray.append(Hexadecimal(value.get_decimalvalue()))
            
    def _calcstringvalue(self):
        """
        creates the string of the object with the existing data of the string array
        ###        
        RETURNS (void)
        """
        DataTypeArray._calcstringvalue(self)
                

                        
"""
a class representing a cluster/array of hexadecimal values
###
value - (string) a single string to be converted as the oonly item in the array
        (list/int) a list of decimal inregers ti convert
        (list/DataType) a list of other DataTypes to convert based in their decimal
                        equivalents
        (DataTypeArray) the cluster of Data 
"""
class BinaryArray(DataTypeArray):
    """
    decimalarray - (list/int) a list with the decimal value of the data
    stringvalue - (string) the string format of the whole thing
    valuearray - (list/DataType) a list of the individual data
    stringarray - (list/string) a list of the string format of each ind. data
    """
    def __init__(self, value):
        # Initializing the super constructor
        DataTypeArray.__init__(self)
        # checking the type of the parameter
        
        # value is string
        if type(value) is str:
            temp_list = JTString.divide_by_whitespace(value)
            for substring in temp_list:
                self.valuearray.append(Binary(substring))
            for subbinary in self.valuearray:
                self.decimalarray.append(subbinary.get_decimalvalue())
                self.stringarray.append(subbinary.get_string())
        
        # value is list
        elif type(value) is list:
            # list consists of integers
            if type(value[0]) is int:
                for subvalue in value:
                    self.decimalarray.append(subvalue)
                    self.valuearray.append(Binary(subvalue))
                for subbinary in self.valuearray:
                    self.stringarray.append(subbinary.get_string())
            # list consists of DataTypes
            elif isinstance(value[0], DataType):
                for datatype in value:
                    self.decimalarray.append(datatype.get_decimalvalue())
                for integer in self.decimalarray:
                    self.valuearray.append(Binary(integer))
                for subvalue in self.valuearray:
                    self.stringarray.append(subvalue.get_string())
        
        # value is DataType Array
        elif isinstance(value, DataTypeArray):
            self.decimalarray = value.decimalarray
            for integer in self.decimalarray:
                self.valuearray.append(Binary(integer))
            for subvalue in self.valuearray:
                self.stringarray.append(subvalue.get_string())
                
        # creating the stringvalue attribute
        self._calcstringvalue()        
    
    def append(self, value):
        """
        Appends the given value to the array
        ###
        value - (int) the decimal format of the data type,
                (DataType) the object instance of the DataType to be added\converted
                (string) the string format of the DataType
        ###
        RETURNS (void)
        """
        # checking for the type
        if type(value) is str:
            self.valuearray.append(Binary(value))
            self.decimalarray.append(self.valuearray[-1].get_decimalvalue())
            self.stringarray.append(value)
        elif type(value) is int:
            self.decimalarray.append(value)
            self.valuearray.append(Binary(value))
            self.stringarray.append(str(value))
        elif isinstance(value, DataType):
            self.decimalarray.append(value.get_decimalvalue())
            self.stringarray.append(value.get_string())
            self.valuearray.append(Binary(value.get_decimalvalue()))
            
    def _calcstringvalue(self):
        """
        creates the string of the object with the existing data of the string array
        ###        
        RETURNS (void)
        """
        DataTypeArray._calcstringvalue(self)
        
"""
a class representing a cluster/array of ascii values
###
value - (string) a single string to be converted as the oonly item in the array
        (list/int) a list of decimal inregers ti convert
        (list/DataType) a list of other DataTypes to convert based in their decimal
                        equivalents
        (DataTypeArray) the cluster of Data 
"""
class AsciiArray(DataTypeArray):
    """ 
    decimalarray - (list/int) a list with the decimal value of the data
    stringvalue - (string) the string format of the whole thing
    valuearray - (list/DataType) a list of the individual data
    stringarray - (list/string) a list of the string format of each ind. data
    """
    def __init__(self, value):
        # Initializing the super constructor
        DataTypeArray.__init__(self)
        # checking the type of the parameter
        
        # value is string
        if type(value) is str:
            temp_list = value
            for substring in temp_list:
                self.valuearray.append(Ascii(substring))
            for subascii in self.valuearray:
                self.decimalarray.append(subascii.get_decimalvalue())
                self.stringarray.append(subascii.get_string())
        
        # value is list
        elif type(value) is list:
            # list consists of integers
            if type(value[0]) is int:
                for subvalue in value:
                    self.decimalarray.append(subvalue)
                    self.valuearray.append(Ascii(subvalue))
                for subascii in self.valuearray:
                    self.stringarray.append(subascii.get_string())
            # list consists of DataTypes
            elif isinstance(value[0], DataType):
                for datatype in value:
                    self.decimalarray.append(datatype.get_decimalvalue())
                for integer in self.decimalarray:
                    self.valuearray.append(Ascii(integer))
                for subvalue in self.valuearray:
                    self.stringarray.append(subvalue.get_string())
        
        # value is DataType Array
        elif isinstance(value, DataTypeArray):
            self.decimalarray = value.decimalarray
            for integer in self.decimalarray:
                self.valuearray.append(Binary(integer))
            for subvalue in self.valuearray:
                self.stringarray.append(subvalue.get_string())
                
        # creating the stringvalue attribute
        self._calcstringvalue()        
    
    def append(self, value):
        """
        Appends the given value to the array
        ###        
        value - (int) the decimal format of the data type,
                (DataType) the object instance of the DataType to be added\converted
                (string) the string format of the DataType
        ###
        RETURNS (void)
        """
        # checking for the type
        if type(value) is str:
            self.valuearray.append(Ascii(value))
            self.decimalarray.append(self.valuearray[-1].get_decimalvalue())
            self.stringarray.append(value)
        elif type(value) is int:
            self.decimalarray.append(value)
            self.valuearray.append(Ascii(value))
            self.stringarray.append(str(value))
        elif isinstance(value, DataType):
            self.decimalarray.append(value.get_decimalvalue())
            self.stringarray.append(value.get_string())
            self.valuearray.append(Ascii(value.get_decimalvalue()))
            
    def _calcstringvalue(self):
        """
        creates the string of the object with the existing data of the string array
        ###        
        RETURNS (void)
        """
        for substring in self.stringarray:
            self.stringvalue += substring
        
 

    
    
    
    
    
                   