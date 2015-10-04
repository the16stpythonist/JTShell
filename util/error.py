__author__ = 'Jonas'
from util.message import Message


class Error(Exception):
    """
    the base class for every following error to be defined, this has to be used instead of exceptions, as exceptions
    within the parser for example would terminate the whole program instead of just the progress
    """
    def __init__(self):
        self.message = None

class SyntaxError(Exception):
    """
    the exception given, when dealing with syntax errors within the user input, which may be the error most often
    occuring within a shell program
    :var message: (Message) the message which should be printed when handling the error
    :parameter message: (Message) the message which should be printed when handling the error
    """
    def __init__(self, message):
        self.message = Message("error", message)


class ProcessError(Error):

    def __init__(self, string):
        self.message = Message("error", string)
