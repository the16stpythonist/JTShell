__author__ = 'Jonas'
from JTShell.util.message import Message
import time


class Processer:
    """
    the base class for all objects, that are involved with the command execution process of the Shell, implementing the
    connection with the logger and writer objects of the program, if needed/enabled, that can both be accessed through
    calling the inherited _write method, which will write the message into both objects
    :var logger: (Logger) the logging object of the shell program
    :var writer: (Writer) the writer object of the shell program
    :var name: (string) the name of the class combined with their very own id
    :parameter shell: (Shell) the shell object from wich the Processer object was created in, so the object can acces
                              the writer and logger objects of the shell
    """
    def __init__(self, shell):
        self.shell = shell
        self.name = ""

    def _write(self, typ, message):
        """
        a method, which will pass any given message to the logger and writer objects, if given, which in thier turn
        will then process those messages further, writing them into log files or displaying it to the user.
        the passed string argument "type" defines the appearance of the message and is divided into "error", "process",
        "output", "warning".
        :param message: (string) the message to be displayed
        :param typ: (string) the type of message given
        :return: (void)
        """
        if self.shell.writer is not None:
            self.shell.writer.write(Message(typ, "{0}: ".format(self.name) + message))
        if self.shell.logger is not None:
            self.shell.logger.write(Message(typ, "{0}: ".format(self.name) + message))