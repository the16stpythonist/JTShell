__author__ = 'Jonas'
from JTShell.processers.processer import Processer
from JTShell.util.token import FUNC
from JTShell.processes import ProcessList
from JTShell.util.message import Message
from JTShell.processes import Process
from JTShell.lib.JTLib.JTUtility.JTList import replace_sublist


class Executer(Processer):
    """
    the Executer being the last and main object in the process of executing a issued shell command. The object has to
    be created only once and can then be reused as many times as the program is running, thus also enabeling the use
    of multiple Executer objects, if necessary. The execution process always executes the most inner bracket of the
    given tokenlist first, adding the created Process object to the processlist object of the main shell object for
    universal access.
    :var id: (int) the static id of the generated object, as it is possible that there may be multiple parses objects
                   in use
    :var name: (string) the name of the class combined with their very own id
    :var shell: (Shell) a reference to the original shell instance
    :parameter shell: (Shell) a reference to the original shell instance
    """
    id = 0
    def __init__(self, shell):
        Processer.__init__(self, shell)
        self.name = "Executer" + str(self.id)
        self.processlist = shell.processlist
        self.id += 1

    def execute(self, tlist):
        """
        the main method to finally execute the issued command, that has first been converted into a token list, then
        checked for any possible syntactical errors. the passed token list is executed by always going from left to
        right only in the most inner bracket of the command, adding the therefor started processes to the process list
        object, that has also been passed by passing a reference to the origninal shell instance itself.
        :param tlist: (list) the tokenlist of the command to be executed
        :return: (Process) the reference to the process object, that was last in the chain of execution
        """
        tokenlist = tlist
        inner_tokenlist = []
        prev_process = None
        # repeating the process of grabbing the most inner bracket, executing it and replacing the sub sequence of the
        # very inner bracket with the resulting last process, that was executed by the bracket as long as there are
        # brackets in the tokenlist to be handled
        while "(" in tokenlist or ")" in tokenlist:
            inner_tokenlist = self._get_innerbracket(tokenlist)
            prev_process = self._execute_innerbracket(inner_tokenlist)
            tokenlist = replace_sublist(tokenlist, ["("] + inner_tokenlist + [")"], prev_process)
        # in case there is still a command left even in case there are no brackets in the tokenlist, itl just execute
        # the remaining command and save the last process executed, so that the output can be fetched
        if len(tokenlist) > 0:
            prev_process = self._execute_innerbracket(tokenlist)
        return prev_process


    def _get_innerbracket(self, tokenlist):
        """
        when passed the tokenlist of the command to be executed, this method will simply return the sub-tokenlist of the
        most inner bracket (without the actual bracket tokens), so that this can be easily processed further
        :param tokenlist: (list) the full token list of the issued command
        :return: (list) the sub tokenlist of the most inner bracket
        """
        # as the tokenlist has passed through the analyzer without issueing a exception at this point, any potential
        # errors or input mistakes can be left unhandled
        sub_list = []
        # firstly itering through the whole list, mapping the index of the most inner opening bracket
        current_layer = 0
        index = 0
        layer_innerbracket = 0
        index_innerbracket = 0
        for token in tokenlist:
            # updating the layer of brackets
            if token == "(":
                current_layer += 1
            elif token == ")":
                current_layer -= 1
            # updating the index of the inner bracket, by checking if the current layer is deeper than the inner bracket
            if current_layer > layer_innerbracket:
                layer_innerbracket = current_layer
                index_innerbracket = index
            index += 1
        # now returning
        for i in range(index_innerbracket + 1, len(tokenlist)):
            if tokenlist[i] == ")":
                break
            else:
                sub_list.append(tokenlist[i])
        return sub_list

    def _execute_innerbracket(self, inner_tokenlist):
        """
        the main stage of the execution process, able to execute all syntax properly with the condition that there are
        no brackets within the statement to be executed, returning the process that was last executed in the bracket
        :param inner_tokenlist: (list) the sub tokenlist of the most inner bracket within the main list
        :return: (Process) the last process that has been executed
        """
        # going through the inner tokenlist and executing the syntax in chronological order, as there are no brackets to
        # be executed in advance since this is the most inner layer already
        tlist = inner_tokenlist
        prev_process = None
        index = 0
        while index < len(tlist):
            token = tlist[index]
            # first making the difference between syntax elements and function calls
            if not isinstance(tlist[index], FUNC):
                if token == "&":
                    # in case it is the background operator, starting the following function call in the background
                    prev_process = Process(self.shell, tlist[index + 1], layer="bg")
                    prev_process.start()
                    self.processlist.add_process(prev_process)
                    index += 1
                elif token == "&&":
                    if isinstance(tlist[index + 1], FUNC):
                        while not prev_process.status == "terminated":
                            pass
                        if prev_process.exit_status:
                            # in case the exit status of the previous command was true, executing the second one
                            prev_process = Process(self.shell, tlist[index + 1])
                            prev_process.start()
                            self.processlist.add_process(prev_process)
                            index += 1
                        elif not prev_process.exit_status:
                            # in case the exit status of previous command was false, not executing it, by jumping index
                            index += 1
                elif token == "||":
                    if isinstance(tlist[index + 1], FUNC):
                        while not prev_process.status == "terminated":
                            pass
                        if not prev_process.exit_status:
                            print(2)
                            # in case the exit status of the previous command was true, executing the second one
                            prev_process = Process(self.shell, tlist[index + 1])
                            prev_process.start()
                            self.processlist.add_process(prev_process)
                            index += 1
                        elif prev_process.exit_status:
                            # in case the exit status of previous command was false, not executing it, by jumping index
                            index += 1
                elif token == ">":
                    if isinstance(tlist[index + 1], FUNC) and prev_process.exit_status:
                        prev_process = Process(self.shell, tlist[index + 1], pipe=prev_process.output)
                        prev_process.start()
                        self.processlist.add_process(prev_process)
                        index += 1
                elif token == ";":
                    if isinstance(tlist[index + 1], FUNC):
                        while not prev_process.exit_status:
                            pass
                        if prev_process.is_foreground():
                            print(Message("result", prev_process.output).message)
                elif isinstance(token, Process):
                    prev_process = token
            elif isinstance(token, FUNC):
                prev_process = Process(self.shell, token)
                prev_process.start()
                self.processlist.add_process(prev_process)
            index += 1
        return prev_process




