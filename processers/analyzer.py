__author__ = 'Jonas'
import os
import importlib
import inspect

from JTShell.lib.JTLib.JTUtility.JTString import count_chars

from JTShell.util.error import SyntaxError as SynError
from JTShell.util.token import FUNC
from JTShell.processers.processer import Processer


class Analyzer(Processer):
    """
    the Analyzer object being the first process in executing a shell command, that is issued by the user. The object has
    to be created only once and can then be reused by just passing the command strings to be analyzed to the analyze
    method of the object, which will then raise multiple different SyntaxError, in case there would be a mistake within
    the user input. It is important, that when using the analyze method, the outgoing exceptions have to be catched and
    properly treated, in case one doesnt want to terminate the whole shell when making a input mistake.
    :var id: (int) the static id of the generated object, as it is possible that there may be multiple parses objects
                   in use
    :var name: (string) the name of the class combined with their very own id
    :var shell: (Shell) a reference to the original shell instance
    :parameter shell: (Shell) a reference to the original shell instance
    """
    id = 0

    def __init__(self, shell):
        Processer.__init__(self, shell)
        self.name = "Analyzer" + str(self.id)
        self.id += 1

    def analyze(self, tokenlist, command):
        """
        a method checking the basic syntax of the command issued by the user, raising exception in return. First
        checking if there are any syntactical mistakes concerning the placement of brackets within the command, then
        checking the validity of the given function calls and their expected parameters
        :param tokenlist: (list) the already parsed token list, resembling the issued command
        :param command: (string) the orignally issued command
        :return: (void) raises exceptions in case there is something wrong
        """
        self._write("process", "analyzing command {0}".format(command))
        # firstly checking whether there have been any mistakes with the placement of brackets, calling the method
        # _check_brackets, which will then raise an error in case there was a mistake
        self._check_brackets(tokenlist, command)
        # secondly checking whether there have been any calls for none existant commands or parameters, calling the
        # _check_functioncalls method, which will then raise an error in case there has been a mistake
        self._check_functioncalls(tokenlist, command)
        self._check_pipingcompatibility(tokenlist, command)
        self._check_backgroundchaining(tokenlist, command)

    def _check_brackets(self, tokenlist, command):
        """
        a method checking whether the brackets used in the given command are correctly set, or whether one has been placed
        mistakenly or has been forgotten.
        :param command: (string) the command that has been passed to the parser
        :return: (void) raising exceptions in case there is something wrong
        """
        # creating a new buffer string to, to which only the brackets within the command are added, as this is easier
        # to process and the other content of the original command isnt needed for this step anyways
        buffer_string = ""
        for token in tokenlist:
            if token is "(" or token is ")":
                buffer_string += token
        # first checking the most easy and common mistake: a different amount of opening and closing brackets
        if not(count_chars(buffer_string, "(") == count_chars(buffer_string, ")")):
            self._write("error", "Command '{0}' ".format(command) +
                        "couldn't be processed due to no matching amount of opening and closing brackets")
            raise SynError("There is a different amount of closing and opening brackets present in the issued " +
                           "command. Please try having a closing bracket for every opening one")
        # now checking for the uncommon mistake of brackets being the wrong way around, meaning ")("
        # therefor iterating through the string several times, always removing the right combination, in the end
        # checking whether a string has been left over or not
        bracket_count = count_chars(buffer_string, "(")
        for i in range(bracket_count):
            buffer_string = buffer_string.replace("()", "")
        if len(buffer_string) >= 1:
            self._write("error", "Command '{0}' ".format(command) +
                        "couldn't be processed due to brackets being placed the wrong way around")
            raise SynError("There are mixed bracket directions within the issued command. Please try putting the " +
                           "closing brackets after the opening ones")

    def _check_functioncalls(self, tokenlist, command):
        """
        a method first checking whether the given function names actually refer to a custom python module in the cmds
        sub folder, so that the function can be properly found and executed, then checking whether the given parameters
        are actually expected by their corresponding functions or not
        :param tokenlist: (list) the already parsed token list, resembling the issued command
        :param command: (string) the orignally issued command
        :return: (void) raises exceptions in case there is something wrong
        """
        # checking whether the called functions are actually available and have the right format to be executed,
        # therefor going through the "cmds" folder of the current working directory and first checking whether the
        # files actually exist
        for token in tokenlist:
            if isinstance(token, FUNC):
                if not(os.path.exists(os.getcwd() + "\\"+self.shell.source+"\\" + token.name + ".py")):
                    self._write("error", "Command '{0}' couldn't be ".format(command) +
                                "processed, because the the function '{0}' doesn't exist".format(token.name))
                    raise SynError("There is no function with the name '{0}'".format(token.name))
        # now checking if the functions called are properly implemented by attempting to import
        for token in tokenlist:
            if isinstance(token, FUNC):
                # importing the module without handling a possible exception since we already checked the existance of
                # those modules
                module = importlib.import_module(self.shell.source+"." + token.name)
                if not(inspect.isfunction(module.run)):
                    self._write("error", "Command '{0}' couldn't be executed, as the module of ".format(command)+
                                "the issued function '{0}' didn't implement a 'run' function".format(token.name))
                    raise SynError("There is no function with the name '{0}'".format(token.name))
                # now going through every given parameter of every passed function, checking whether they are actually
                # expected by the functions or not
                for parameter in token.parameters:
                    # function inspect.getargspec(func) mainly returns a slightly altered list of the expected arguments
                    # of a given function or method
                    if parameter.name not in inspect.getargspec(module.run)[0][1:]:
                        self._write("error", "Command '{0}' couldn't be executed, as the given ".format(command) +
                                    "parameter '{0}' is not in the list of expected arguments of ".format(parameter.name) +
                                    "the function '{0}'".format(token.name))
                        raise SynError("The parameter {0} is not expected by the function {1}".format(parameter.name, token.name))
                if "std" in inspect.getargspec(module.run)[0][1:] and "std" not in token.get_dict().keys():
                    self._write("error", "Command '{0}' couldn't be executed, as the given ".format(token.name) +
                                "expects a standard parameter")
                    raise SynError("The function {0} expects a standard parameter, that has not been given".format(token.name))


    def _check_pipingcompatibility(self, tokenlist, command):
        """
        checks whether the usage of the critical pipe operator was done correctly, therefor checking if the pipe
        operator was used on a function call in the first place, and secondly checks if the function call supports
        piping
        :param tokenlist: (list) the already parsed token list, resembling the issued command
        :param command: (string) the orignally issued command
        :return: (void) raises exceptions in case there is something wrong
        """
        # looping until hitting a piping operator, then checking whether the following token even is a function call
        # or not and in case it is checking if it supports the pipe parameter
        for index in range(len(tokenlist)):
            if tokenlist[index] is ">":
                if isinstance(tokenlist[index + 1], FUNC):
                    module = importlib.import_module(self.shell.source+"." + tokenlist[index + 1].name)
                    if "pipe" not in inspect.getargspec(module.run)[0][1:]:
                        self._write("error", "Command {0} couldn't be executed ".format(command) +
                                    "as the function '{0}' doesn't support the pipe operator.".format(tokenlist[index + 1].name))
                        raise SynError("The function '{0}' doesn't support the pipe operator".format(tokenlist[index + 1].name))
                else:
                    self._write("error", "Command {0} couldn't be executed ".format(command) +
                                "as the pipe operator cannot be used on non function syntax")
                    raise SynError("the pipe operator cannot be used on none function syntax")

    def _check_backgroundchaining(self, tokenlist, command):
        """
        checking whether the operator "&" for starting a background process is attempted to be used in a chaining
        operation "&&",">","||", which themselfes depend on the exit status of the previous process, that in turn
        cannot be given by a background process
        :param tokenlist: (list) the already parsed token list, resembling the issued command
        :param command: (string) the orignally issued command
        :return: (void) raises exceptions in case there is something wrong
        """
        for index in range(len(tokenlist)):
            if tokenlist[index] is "&":
                if isinstance(tokenlist[index + 1], FUNC):
                    if index+2 < len(tokenlist) and (tokenlist[index + 2] == "||" or tokenlist[index + 2] == "&&" or tokenlist[index + 2] == ">"):
                        self._write("error", "Command {0} couldn't be executed as a background ".format(command) +
                                    "process cannot be used in a chaining operation")
                        raise SynError("A background process cannot be used in a chaining operation")
            elif index+2 < len(tokenlist) and (tokenlist[index + 2] == "||" or tokenlist[index + 2] == "&&" or tokenlist[index + 2] == ">" or tokenlist[index + 2] == ";"):
                if not(isinstance(tokenlist[index - 1], FUNC)):
                    self._write("error","Command {0} couldn't be executed as a chaining operator ".format(command) +
                                "must follow on a function call, but nothing else")
                    raise SynError("A chaining operator can only be used after a function call")




