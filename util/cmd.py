__author__ = 'Jonas'


def shellprint(process, message):
    """
    The "print" function altered to work in the JTShell environment, only executing a print function in case the passed
    process object is in the foreground
    :param process: (Process) the process object of the process executing the function
    :param message: (Message) the message to be printed
    :return: (bool) whether it was printed or not
    """
    if process.is_foreground():
        print(str(message))
        return True
    else:
        return False
