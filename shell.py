__author__ = 'Jonas'
import os
import sys
import inspect
PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from JTShell.processers.parser import Parser
from JTShell.processers.analyzer import Analyzer
from JTShell.processers.executer import Executer
from JTShell.processes import ProcessList
from JTShell.util.message import Message
import JTShell.util.error as error
import JTShell.util.colors as colors


class Shell:
    """
    the actual Shell object, able to run user issued string commands with a customizable syntax concerning operators
    and brackets use, fully coded in python, having up to no dependencies. Command line functions can be created by
    simply adding a python module with the functions name to the chosen folder and having a run function within the
    module, that will then be executed as the actual process within the shell.
    :var logger: (logger) the logger object, that saves all of the shells activities inside a log file
    :var prompt: (string) the command prompt to be displayed with the input collection method
    :var processlist: (ProcessList) the object managing all currently running processes
    :var parser: (Parser) the parser, converting the parameter objects into token lists
    :var analyzer: (Analyzer) the analyzer, raising exceptions in case there are any syntactical mistakes
    :var executer: (Executer) the executer, applying the syntax and executing the functions as processes
    :var supershell: (Shell) the top level shell, from that the current shell has been created
    :parameter supershell: (Shell) the top level shell, from that the current shell has been created
    """
    def __init__(self, commandfolder, supershell=None):
        # tests
        self.logger = None
        self.writer = None
        self.prompt = "\n JTShell > "
        self.source = commandfolder
        # setting up the process list, that will be managing all ongoing processes within the shell, whenever the shell
        # is closed, very ascociated process is closed aswell
        self.processlist = ProcessList()

        # creating the prcessors objects, that will be in charge of executing any issued command correctly
        # the parser, which will convert the given string commands into a token list
        self.parser = Parser(self)
        # the analyzer, which will check the issued commands for any syntactical mistakes
        self.analyzer = Analyzer(self)
        # and finally the executer, that will ultimately start the command functions as new processes
        self.executer = Executer(self)

        # the parent shell, from which every subshell originates
        self.supershell = supershell

    def run(self):
        """
        the main method of the shell running the infinite loop, continuesly prompting for a command, then attempting to
        execute the issued command
        :return: (void)
        """
        # opening the infinite loop inside of a try statement, so that the SystemExit Exception can be caught
        try:
            while True:
                # first fetching the user input
                print(colors.magenta(colors.bold(self.prompt)), end="")
                command = input()

                if command == "exit":
                    if self.supershell is None:
                        sys.exit()
                    else:
                        break
                # skipping the whole procedure in case the command prompt is empty
                if command != "" and command != " ":
                    # then converting the command into a token list via the parse method
                    tokenlist = self.parser.parse(command)
                    # checking for any potential errors
                    try:
                        self.analyzer.analyze(tokenlist, command)
                        # in case the analyzer didnt raise any errors attempting to execute the tokenlist
                        last_process = self.executer.execute(tokenlist)
                        while not(last_process.status == "terminated"):
                            pass
                        if last_process.is_foreground():
                            print(Message("result", last_process.output).message)
                    except error.SyntaxError as e:
                        print(e.message.message)
        except SystemExit as e:
            pass
