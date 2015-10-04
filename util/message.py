__author__ = 'Jonas'
import JTShell.util.colors as colors


class Message:
    """
    a class representing a certain kind of message used within the source code of the Shell, taking the two arguments
    'typ' and 'string', typ being the type of message, the actual string message is to be represented as, being either
    warning, error, result, process or output, all having different symbols and colors.
    The class can be used to store those different kind of Message until they are needed in string format, at this
    point the str() function can be simply used on any Message class
    :argument typ: (string) the type of message
    :argument string: (string) the original string message passed to the class
    :var type: (string) the type of message
    :var string: (string) the original string message passed to the class
    :var message: (string) the finished string already containing the colors and symbols of the corresponding type
    """
    def __init__(self, typ, string):
        # creating the class variables
        self.type = typ
        self.string = string
        self.message = ""
        # creating the message string with the colors and symbols according
        if typ == "warning":
            self.message = colors.yellow("[!] " + str(self.string))
        elif typ == "error":
            self.message = colors.red("[!] " + str(self.string))
        elif typ == "process":
            self.message = colors.white("[*] " + str(self.string))
        elif typ == "result":
            self.message = colors.green("[+] " + str(self.string))
        elif typ == "output":
            self.message = colors.white(str(self.string))

    def __str__(self):
        """
        defines behaviour, when the str() function is used on the object, returning the fully processed and converted
        message string as the representation of the Message class, fullfilling its purpose
        :return: (string) the message string, containing the added colors and symbols
        """
        return self.message



