__author__ = 'Jonas'
import re


class O:
    """
    A static class acting as the storage namespace for the operator tokens used to parse and execute the command issued
    by the user, those tokens include AND, OR, BACKGROUND, NONE, WAIT, OPEN, CLOSE
    """
    PIPE = ">"
    AND = "&&"
    BACKGROUND = "&"
    NEW = "#"
    OR = "||"
    WAIT = ";"
    NONE = ""
    OPEN = "("
    CLOSE = ")"


class FUNC:
    """
    a class representing the Function token
    """
    def __init__(self, string):
        self.name = string
        self.parameters = []

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def get_dict(self):
        dictionary = {}
        for parameter in self.parameters:
            dictionary[parameter.name] = parameter.content
        return dictionary


class PARAM:
    """
    pass
    """
    def __init__(self, string):
        self.name = ""
        self.content = ""
        if not(string[0] == '''"''') and not(string[-1] == '''"'''):
            # as the parameter has to have a pretty strict sysntax it is easily slicable
            _string = string.replace("--","")
            switch = False
            for character in _string:
                if character == "=" or character is ":":
                    switch = True
                else:
                    if switch is False:
                        self.name += character
                    else:
                        self.content += character
            # finally converting the parameter to its according type
            self.content = self._convert_parametertype(self.content)
        else:
            self.name = "std"
            self.content = self._convert_parametertype(string[1:-1])

    def _convert_parametertype(self, str_content):
        """
        the method converting the string only content of the parameter to eventually different datatypes using given
        syntax, which is, that every string only containing digits will be counted as an float number, a content string,
        that starts and ends with a quotation mark is counted as an string, and there is also the possibility of passing
        a list, by using the standard python syntax for creating lists. It has to be said though, that more complex
        parameters such as Dictionaries, other classes or even other functions are not possible to be processed
        :param str_content: (string) the string format of the value of the parameter
        :return: (?) whatever datatype it has been converted into
        """
        # the easiest thing to be checked first, wether the string resembles the boolean datatype, being either False
        # or True
        if str_content == "true" or str_content == "True":
            return True
        elif str_content == "false" or str_content == "False":
            return False
        # next checking whether a string was actually intended or not, by checking if the passed string is within quotes
        if str_content[0] == '''"''' and str_content[-1] == '''"''':
            return str_content[1:-1]
        # now checking whether the string can be habdled as a number by attempting to convert it inside a try statement
        try:
            return float(str_content)
        except:
            # now checking wether it can be handled as a list, by searching for the "[]" python syntax for lists
            if str_content[0] == "[" and str_content[-1] == "]":
                # removing the two strings and then splitting the string with the , syntax in case it isnt currently
                # inside a string of the List
                inside_string = False
                content_list = []
                temp_string = ""
                for character in str_content[1:-1]:
                    if character == ",":
                        if not inside_string:
                            content_list.append(self._convert_parametertype(temp_string))
                            temp_string = ""
                    else:
                        if character == '''"''':
                            if inside_string:
                                inside_string = False
                            else:
                                inside_string = True
                        else:
                            temp_string += character
                content_list.append(self._convert_parametertype(temp_string))
                return content_list
            # in cas no of the previously described syntax matches the parameter string itll have to be handled as a
            # simple string
            else:
                return str_content

