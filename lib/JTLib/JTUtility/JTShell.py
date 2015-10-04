# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 19:22:30 2015
@author: Jonas
###
File to be executed by the Microsoft PowerShell Environment and that then
executes the python cmd.Cmd-Custom Shell with a set of predefined commands,
representing Functions and Scripts, that are easily extendable by the user
"""
import sys, os, cmd
import convert_datatype


class PythonShell(cmd.Cmd):
    # the intro text for the specific JTShell
    intro = ("\nWelcome to the JTShell v.01, a simple command line based program\n"
             "developed by Jonas Teufel\naimed at providing a vast list of commands\n"
             "adding complex python based functionality to everyday usage\n"
             "Type '?' or 'help' for a list of commands\n")
    # the prompt to be used every turn, using the standard python prompt
    prompt = '> '
    
    def do_convert_datatype(self, arg):
        "converts any given datatype to the assigned datatype"
        script = convert_datatype.Script(arg)
        script.run()
        
    def do_exit(self, arg):
        "exits out of the custom shell"
        sys.exit()
        
if __name__ == "__main__":
    PythonShell().cmdloop()