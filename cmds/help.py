__author__ = 'Jonas'
from importlib import import_module
from JTShell.lib.JTLib.JTOS.JTCombinedOs import Directory
from JTShell.util.terminal import helplist
import os.path
import util.colors as colors

help = {"desc": ("prints a list of all available commands for the terminal, or detailed information for one specific "
                 "command"),
        "module": ("gives specific information about the usage and the parameteres of the given command")}


def run(process, module=""):
    shell = process.shell
    folder = Directory(os.path.dirname(os.path.abspath(__file__)))
    files = folder.get_files()
    if module != "":
        if module + ".py" in files:
            string = ""
            mod = import_module(shell.source + "." + module)
            string += "\n" + colors.white(mod.help["desc"]) + "\n"
            help_dictionary = {}
            for name in mod.help.keys():
                if name != "desc":
                    help_dictionary[name] = mod.help[name]
            return string + "\n" + helplist(help_dictionary, color="green")

    else:
        help_dictionary = {}
        for file in files:
            file_split = file.split(".")
            if file_split[1] == "py":
                mod = import_module(shell.source + "." + file_split[0])
                help_dictionary[file_split[0]] = mod.help["desc"]
        return helplist(help_dictionary, color="green")