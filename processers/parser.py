__author__ = 'Jonas'
from JTShell.util.error import SyntaxError
from JTShell.util.token import O, FUNC, PARAM
from JTShell.processers.processer import Processer


class Parser(Processer):
    """
    the Parser object being the first process in executing a shell command, that is issued by the user. The object has
    to be created only once and can then be reused by just passing the command strings to be parsed to the parse method
    of the object collecting the output after. the parsing process basicly does nothing else, than translating the
    complicated input string into a list of so called tokens, which themself represent one part of the command passed,
    differentiated into operators and functions, while the operator tokens are mere constants, the function tokens, are
    objects, containing the fucntion name, as well as parameter objects.
    :var id: (int) the static id of the generated object, as it is possible that there may be multiple parses objects
                   in use
    :var name: (string) the name of the class combined with their very own id
    :var logger: (Logger) the logging object of the shell program
    :var writer: (Writer) the writer object of the shell program
    :parameter logger: (Logger) the logging object of the shell program
    :parameter writer: (Writer) the writer object of the shell program
    """
    id = 0

    def __init__(self, shell):
        Processer.__init__(self, shell)
        self._write("process", "created new ShellParser object with the internal id: {0}".format(self.id))
        self.name = "Parser" + str(self.id)
        self.id += 1

    def parse(self, command):
        """
        the main method to parse any given command, meaning replacing the complicated string with an easily processable
        tokenlist
        :param command: (string) the command that has been passed to the parser
        :return: (list) the translated tokenlist
        """
        self._write("process", "attempting to parse command '{0}'".format(command))
        # actually parsing the single parts of the command with the _parse method, which then returns a raw tokenlist
        tokenlist = self._parse(command)
        # adding the parameter tokens to the function tokens, thus removing them from the tokenlist
        tokenlist = self._assemble(tokenlist, command)
        # returning the final parsed token list
        self._write("result", "successfully parsed the string")
        return tokenlist

    def _parse(self, command):
        """
        a method which actually does the real parsing within the parser class, when passed a subcommand, meaning the
        pure command within the most inner bracket, it'll translate this command into a token list, which is much easier
        to be further processed by the program
        :param command: (string) the command passed to the parser
        :return: (list) the token list
        """
        # clusterfuck of if conditions, just hamster yourself through
        self._write("process", "parsing the command '{0}'...".format(command))
        token_list = []
        temp_string = ""
        quotation_mark = False
        for character in command + " ":
            if quotation_mark is True:
                if character == '''"''':
                    quotation_mark = False
                temp_string += character
            elif quotation_mark is False and (character != " " and character not in ["(", ")"]):
                if character == '''"''' and quotation_mark is False:
                    quotation_mark = True
                # as long as there isnt a whitespace in the row of characters, which is syntacticly defined as the
                # separation condition, the characters are added up to form a argument within temp_string
                temp_string += character
            elif quotation_mark is False and (character == " " or character in ["(", ")"]):
                if len(temp_string) >= 1:
                    # if the whitespace/ separation then occurs one has to assume the argument now is complete, now trying
                    # to figure out, what syntactical piece the assembled string resembles, first checking if it is
                    # a fixed operator, which will then be added to the token list as the corresponding token constant
                    if temp_string == ">":
                        token_list.append(O.PIPE)
                    elif temp_string == ";":
                        token_list.append(O.WAIT)
                    elif temp_string == "&":
                        token_list.append(O.BACKGROUND)
                    elif temp_string == "#":
                        token_list.append(O.NEW)
                    elif temp_string == "&&":
                        token_list.append(O.AND)
                    elif temp_string == "||":
                        token_list.append(O.OR)
                    else:
                        # if it isnt an operator it has to be either a parameter or a function call, whereas a parameter
                        if "--" in temp_string:
                            # whereas a parameter has to contain a specific syntax("--","=") that the parser is able to
                            # check for and when found the parameter object is added to the token list
                            token_list.append(PARAM(temp_string))
                        elif temp_string[0] == '''"''' and temp_string[-1] == '''"''':
                            # then in case it is an required parameter, that is marked by simply being after the
                            # function call in quotation marks
                            token_list.append(PARAM(temp_string))
                        else:
                            # the last option of a string is to be either a function call or input mistake, assuming the
                            # input is correct the function call is now as well added to the token list
                            token_list.append(FUNC(temp_string))
                    # however the outcome of the if statements the temp_list has to be cleared for the next argument
                    temp_string = ""
                if character is "(":
                    token_list.append(O.OPEN)
                elif character is ")":
                    token_list.append(O.CLOSE)
        return token_list

    def _assemble(self, tokenlist, command):
        """
        a method that should be used on the tokenlist after being generated by the _parse method, generating a new
        tokenlist, containing only function tokens, but not parameters, as they are being added to their
        corresponding functions. In case there is a syntactical problem with the positioning of the parameters, this
        method will return the name of the parameter, whose problem was detected first, so an error message can be
        generated with the return of this method
        :param tokenlist: (list) the raw list of tokens, generated by the _parse method
        :return: (list) the tokenlist, not containing any parameters, but only function tokens
        """
        # going through the token list, adding its content to a new list, but rather tha adding the parameters to the
        # list itself, they are added to their corresponding function call, this way also checking wether there has been
        # a mistake with loose parameters, not belonging to a function
        in_functioncall = False
        new_tokenlist = []
        for token in tokenlist:
            if not(isinstance(token, FUNC)) and not(isinstance(token, PARAM)):
                # adding any operator to the new list, also terminating the in_functioncall statement, as an operator
                # separates function calls
                new_tokenlist.append(token)
                in_functioncall = False
            elif isinstance(token, FUNC):
                # adding the function to the new list and signaling the program, that the following is to be added to
                # the function call, meaning the function call was the last statement added to the list
                new_tokenlist.append(token)
                in_functioncall = True
            elif isinstance(token, PARAM):
                if in_functioncall:
                    # a new parameter is added to the last entry of the tokenlist, which according to the usage of the
                    # in_functioncall variable has to be a function token
                    new_tokenlist[-1].add_parameter(token)
                else:
                    # in case a parameter is located without a function call raises an exception
                    self._write("error", "Command '{0}' couldn't be".format(command) +
                                "processed due to the parameter {0} not being linked to a function call". format(token.name))
                    raise SyntaxError("Parameter '{0}' cant be processed without being linked to a".format(token.name) +
                                      "function call. Please try appending the parameter directly after the function")
        return new_tokenlist
