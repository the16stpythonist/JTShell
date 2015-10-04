# -*- coding: utf-8 -*-
"""
Created on Fri May 29 10:01:38 2015

@author: Jonas
"""
import JTLib.JTCrypt.JTDataTypes as datatypes
import PSUtil as psutil
import os

"""
the powershell command to convert a given string format of nearly any DataType
into another given DataType
"""
class ConvertDatatypeScript(psutil.PowerShellScript):

    def __init__(self, arg):
        psutil.PowerShellScript.__init__(self, arg)
        helptable = psutil.PowerShellTable(["parameter","description"], ["-mode","script supports interactive mode "],
                                           ["-intype","the datatype of the input string"],
                                           ["-outtype","the datatype to be converted into"],
                                           ["-save","the path to the file in which the result should be saved"],
                                           ["-str","the string to be convertes. !no whitespace"],
                                           ["-scr","the path to the file, from which to read the data to convert"])
        self.help = ("python script that is used to convert datatypes between each other\n"+helptable.get_string())
        
    def run(self):
        """
        the method to actually contain the functionality and that has to be
        ###
        RETURNS (void)
        """
        psutil.PowerShellScript.run(self)
        # the used variables
        input_type = ""
        output_type = ""
        output_format = ""
        source = ""
        result = ""
        # checking for the interactive mode option, meaning the parameters are
        # going to be asked
        if ("-mode" in self.args.keys()):
            if (self.args["-mode"] in ["interactive","interact","ask"]):
                input_format = psutil.ask_for("input data from file or string?", "> ", ["file","string","str"])
                if input_format == "file":
                    temp_path = ""
                    while(not(os.path.exists(temp_path) and os.path.isfile(temp_path))):
                        temp_path = input("path: ")
                    temp_file = open(temp_path, mode="r")
                    source = temp_file.read().replace("\n", " ")
                    temp_file.close()
                elif input_format in ["string","str"]:
                    source = psutil.ask_for("String to be converted:","> ","all")
                input_type = psutil.ask_for("DataType of the input string\n(hexa,bin,decimal,unknown)",
                                            "> ", ["bin","binary","hexa","hexadecimal","decimal","decim","unknown","false","False"])
                output_type = psutil.ask_for("DataType to be converted into\n(hexa,bin,decimal)",
                                             "> ", ["bin","binary","hexa","hexadecimal","decimal","decim"])
        # programm tree for processing the call through normal call
        else:
            if ("-intype" in self.args.keys() and self.args["-intype"] in ["bin","binary","hexa","hexadecimal","decimal","decim","unknown","false","False"]):
                input_type = self.args["-intype"]
            else:
                input_type = "unknown"
            if ("-outtype" in self.args.keys() and self.args["-intype"] in ["bin","binary","hexa","hexadecimal","decimal","decim"]):
                output_type = self.args["-outtype"]
            else:
                print("...ERROR: An output type must be given")
                return 0
            if ("-str" in self.args.keys()):
                source = self.args["-str"]
            elif ("-src" in self.args.keys()):
                temp_path = self.args["-src"]
                if os.path.exists(temp_path) and os.path.isfile(temp_path):
                    temp_file = open(temp_path, mode="r")
                    source = temp_file.read().replace("\n", " ")
                    temp_file.close()
                else:
                    print("...ERROR: given file couldnt be opened")
                    return 0
            else:
                print("...ERROR: An input string must be given")
                return 0
        # the actual process
        print("...converting input of the type '{0}' into the type '{1}'".format(input_type, output_type))
        hexa = ["hexa","hexadecimal"]
        bina = ["bin","binary"]
        decim = ["decim","decimal"]
        # checking for the different combinations with a tree of if conditions
        print("...starting operation")
        if output_type in decim:
            if input_type in bina:
                source = datatypes.BinaryArray(source)
                result = datatypes.DecimalArray(source)
            elif input_type in hexa:
                source = datatypes.HexadecimalArray(source)
                result = datatypes.DecimalArray(source)
        elif output_type in bina:
            if input_type in decim:
                source = datatypes.DecimalArray(source)
                result = datatypes.BinaryArray(source)
            elif input_type in hexa:
                source = datatypes.HexadecimalArray(source)
                result = datatypes.BinaryArray(source)
        elif output_type in hexa:
            if input_type in decim:
                source = datatypes.DecimalArray(source)
                result = datatypes.HexadecimalArray(source)
            elif input_type in bina:
                source = datatypes.BinaryArray(source)
                result = datatypes.HexadecimalArray(source)
        print("...conversion complete")
        # printing the final result
        final_string = result.get_string()+"\n"
        print("...printing results:\n")
        print(final_string)
        # options to save the content in a file, therefor calling the predefined
        # utils options
        if self._check_arg("-mode",["interactive","interact","ask"]):
            psutil.ask_savefile(final_string)
        elif self._check_arg("-save","all"):
            psutil.savefile(self.args["-save"],final_string)


            
        
