__author__ = 'Jonas'
from threading import Thread
from JTShell.util.message import Message
from JTShell.util.error import ProcessError
from importlib import import_module
import time


class Process(Thread):
    """
    a Thread representing a process, which is then started as a separated program, but within the same python executable
    environment. It can be decided whether the process is going to be executed in the foreground or in the background,
    meaning whether the Thread is ran parallel to the main shell or as a mere function within delaying the main flow
    :parameter shell: (Shell) the top level shell object creating the process being passed as a reference
    :parameter func: (FUNC) the function token, of the issued function call to be executed as
    :parameter layer: (string) whether it is a foreground or background process
    :parameter processname: (string) in case the program wants a specific process name

    :var status: (string) the status of the process (preparing, running, terminated)
    :var output: (?) the output of the actual executed function
    :var shell: (Shell) reference of the shell object, which executed the construction of the process
    :var functioncall: (FUNC) the function token, of the issued call to be executed
    :var layer: (string) whether it is a foreground or background process
    :var name: (string) the name of the process
    :var id: (int) the id of the process, aka which number of process it is
    """
    id_count = 0

    def __init__(self, shell, func, layer="fg", processname=None, processdescription=None, pipe=None):
        # initializing the Thread super class
        Thread.__init__(self)
        # creating the status variable and set it to preparing
        self.status = "preparing"
        self.output = None
        self.pipe = pipe
        self.exit_status = None
        self.exception = None
        # setting the logger and writer objects
        self.shell = shell
        # setting the actual functioncall variable as the given FUNC-object token, which inherits all the information
        # needed to execute the function, but only the function
        self.functioncall = func
        # setting the layer, that has either been passed to the constructor or that is preset to foreground
        self.layer = ""
        if layer == "fg" or layer == "foreground":
            self.layer = "foreground"
        elif layer == "bg" or layer == "background":
            self.layer = "background"
        else:
            self.layer = "foreground"
        # setting the processname, in case there is a specific one given, if there isn't just using the name of the
        # given functioncall
        self.name = ""
        if processname is None:
            self.name = self.functioncall.name
        else:
            self.name = str(processname)
        # appending to the process id after the object has been successfully constructed
        self.id = self.id_count
        self.id_count += 1
        # now running the Thread/Process depending on the layer, in which it is supposed to be started, in the fg
        # the run method is simply called, so that the Thread isn' actually started in the background, but delays the
        # foreground shell

    def run(self):
        """
        actually starts the main Thread functionality, which then doesnt enter a loop but only starts the run
         of
        the chosen function module, by turning the function token into a dictionary, then unpacking it as the run
        method functions parameter arguments
        :return: (void)
        """
        # locally importing the module to the corresponding name of the passed functioncall to be executed
        # importing the module/function from the source folder inherited from the master shell
        module = import_module(self.shell.source + "." + self.functioncall.name)
        self.status = "running"
        # assuming, as to this point of execution the tokenlist has passed through the analyzer process, there are no
        # syntactical errors present in the function and its parameters, thus simply executing the run method of the
        # imported module with the fix parameter "shell" and the given additional parameters by first turning the passed
        # fucntion token into a dictionary and unpacking them into the function call
        try:
            if self.pipe is None:
                self.output = module.run(self, **self.functioncall.get_dict())
            else:
                self.output = module.run(self, pipe=self.pipe, **self.functioncall.get_dict())
            self.exit_status = True
        except ProcessError as e:
            self.output = e.message
            self.exit_status = False
        self.status = "terminated"

    def is_foreground(self):
        """
        a method simply returning a boolean value whether the process is executed in the foreground layer or not,
        foreground meaning, the process that is currently being executed by the main shell interface
        :return: (bool)
        """
        if self.layer == "foreground":
            return True
        else:
            return False

    def is_background(self):
        """
        a method simply returning a boolean value whether the process is executed in the background layer or not,
        background meaning being executed as a parallel Thread, that isn't influencing the default shell routine
        :return: (bool)
        """
        if self.layer == "background":
            return True
        else:
            return False

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
            self.writer.write(Message(typ, "{0}: ".format(self.name) + message))
        if self.shell.logger is not None:
            self.logger.write(Message(typ, "{0}: ".format(self.name) + message), time.time())


class ProcessList(Thread):
    """
    the object, basicly to be seen as an abstracted list, containing references and information to every currently
    running or terminated process, that has been started inside the main shell environment, to be used as an easy access
    point when handling operations of requesting or manipulating data of processes
    """
    def __init__(self):
        super(ProcessList, self).__init__()
        # the dictionary containing the process objects to their corresponding ids:
        self.dict_id = {}
        # the dictionary containing the process objects to their corresponding processnames:
        self.dict_name = {}

    def run(self):
        """
        the main loop of the thread, implementing the garbage collection functionality after about 20 seconds
        :return:
        """
        while True:
            time.sleep(20)
            for process in self.dict_id.items():
                if process.status == "terminated":
                    time.sleep(1)
                    del self.dict_id[process.id]
                    del self.dict_name[process.name]

    def add_process(self, process):
        """
        adding the process to the list, through adding the process to the internal dictionaries
        :param process:
        :return:
        """
        # then adding the process to the id/ name dictionaries
        self.dict_id[process.id] = process
        self.dict_name[process.name] = process

    def __len__(self):
        """
        defines, that when the len() function is used on the object, it'll return the amount of processes currently
        stored in the process list
        :return: (int)
        """
        return len(self.dict_name.items())

    def __getitem__(self, item):
        """
        defines the behaviour when the processlist[item] is used on the object. In case it is an integer used as item,
        it is supposedly meant to act as id of the searched process, that will then be returned. In case it is an
        string used as item, is is supposed to be the name of the process, returning the according process object
        from the dictionary
        :param item: (string),(int) the id or the name of the process object wanting to be returned
        :return:(process) the corresponding Process object
        """
        # checking the type of the item that is checked for, in case it is an integer, then the item is supposed to
        # resemble the id of the process
        if type(item) is int:
            return self.dict_id[item]
        # in case its an string though, the item is supposed to be the name of the process
        elif type(item) is str:
            return self.dict_name[item]

